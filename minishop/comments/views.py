from django.shortcuts import render, get_object_or_404, redirect
from magazine.models import Product
from .models import *
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import DeleteView
from django.dispatch import receiver
import os
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.db.models.signals import post_delete




@login_required
def add_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = CommentForm(request.POST)  # Передаем файлы в форму
        if form.is_valid():
            comment = form.save(commit=False)  # Не сохраняем сразу
            comment.user = request.user  # Устанавливаем пользователя
            comment.product = product  # Устанавливаем продукт
            images = request.FILES.getlist('image', default=None)
            comment.save()  # Сохраняем комментарий
            if images:
                for image in images:
                    Comment_images.objects.create(comment=comment, image=image)
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
#@permission_required('change_comments', raise_exception=True)
def edit_comment(request, comment_id):
    editable_comment = get_object_or_404(Comments, id=comment_id)
    editable_comment_images = [u for u in Comment_images.objects.filter(comment=comment_id).values_list('id', 'image')]
    current_url = request.META.get('HTTP_REFERER', '/')
    context = {"comment": editable_comment, "editable_comment_images": editable_comment_images}

    if editable_comment.user != request.user and not request.user.is_staff:
        return redirect(current_url)
    else:
        if request.method == "GET":
            return render(request, "edit_comment.html", context)
        elif request.method == "POST":
            editable_comment.text = request.POST.get("text")
            editable_comment.grade = request.POST.get("grade")
            editable_comment.save()
            images = request.FILES.getlist('image', default=None)
            if images:
                for image in images:
                    Comment_images.objects.create(comment=editable_comment, image=image)
            return redirect('')


class Remove_comment(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = Comments
    success_url = reverse_lazy('main')
    permission_required = 'magazine.delete_comments'

    def dispatch(self, request, *args, **kwargs):
        # Получаем комментарий по ID
        comment = get_object_or_404(Comments, id=self.kwargs['pk'])

        # Проверяем, является ли пользователь автором комментария или администратором
        if comment.user != request.user and not request.user.is_staff:
            return HttpResponseForbidden("У вас нет прав для удаления этого комментария.")

        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return super().handle_no_permission()


class Remove_editable_comment_image(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = Comment_images
    permission_required = 'magazine.delete_comment_images'

    def handle_no_permission(self):
        return super().handle_no_permission()

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', '/')


@receiver(post_delete, sender=Comment_images)
def delete_comment_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@login_required
def comment_add_like_dislike(request, comment_id, action):
    current_url = request.META.get('HTTP_REFERER', '/')

    comment_like, created = Comment_likes.objects.get_or_create(
        comment=Comments.objects.get(id=comment_id),
        user=request.user,
        defaults={'likes': 0, 'dislikes': 0}
    )

    if action == 'like':
        if comment_like.likes == 1:
            # Если лайк уже поставлен, убираем его
            comment_like.likes = 0
        else:
            # Убираем дизлайк, если он был
            comment_like.dislikes = 0
            comment_like.likes = 1

    elif action == 'dislike':
        if comment_like.dislikes == 1:
            # Если дизлайк уже поставлен, убираем его
            comment_like.dislikes = 0
        else:
            # Убираем лайк, если он был
            comment_like.likes = 0
            comment_like.dislikes = 1

    # Сохраняем изменения
    comment_like.save()

    return redirect(current_url)