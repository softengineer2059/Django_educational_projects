from django.views.generic import View, ListView, DeleteView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, get_object_or_404, render
from django.db.models.signals import post_delete
from django.db.models import Sum, Count
from django.dispatch import receiver
import os
from comments.models import *
from .models import *
from account.models import *
from .forms import *
from .services import RecommendationService




class Main(ListView):

    model = Product
    template_name = 'shop.html'
    context_object_name = 'goods'
    paginate_by = 4

    # Использую для поиска
    def get_queryset(self):
        get_search = self.request.GET.get("search")
        get_category = self.request.GET.get("category")
        get_subcategory = self.request.GET.get("subcategory")
        get_ordering = self.request.GET.get('orderby', 'product_name')
        if get_search:
            queryset = Product.objects.filter(product_name__icontains=get_search).order_by(get_ordering)
        elif get_category and get_subcategory:
            queryset = Product.objects.filter(category=get_category, sub_category=get_subcategory).order_by(get_ordering)
        elif get_category:
            queryset = Product.objects.filter(category=get_category).order_by(get_ordering)
        else:
            queryset = Product.objects.order_by(get_ordering)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = {}
        for i in Product.objects.values('id'):
            product_images = Product_image.objects.filter(product=i['id']).values_list('image', flat=True)
            images[i['id']] = list(product_images)
        context['images'] = images
        context['product_grade'] = Comments.objects.values('product').annotate(total_grade=Sum('grade') / Count('grade'), count=Count('grade'))
        # Проверяем авторизацию и наличие Vendor
        context['vendor'] = None
        if self.request.user.is_authenticated:
            try:
                # Пытаемся получить Vendor для пользователя
                context['vendor'] = Vendor.objects.get(user=self.request.user)
            except Vendor.DoesNotExist:
                # Если Vendor не найден, оставляем None
                pass
        return context

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by)


class Product_detail(ListView):

    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'goods'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, id=self.kwargs['id'])

        user_comment = None
        if self.request.user.is_authenticated:
            user_comment = Comments.objects.filter(user=self.request.user, product=product).first()

        product_comments = Comments.objects.filter(product=product)
        comments_images = Comment_images.objects.filter(comment__in=product_comments)

        likes_dict = {}
        comment_likes_data = Comment_likes.objects.filter(comment__in=product_comments)
        # получаем словрь с {id каждого комментария: {лайки: количество; дизлайки: количество}}
        for like in comment_likes_data:
            if like.comment.id not in likes_dict:
                likes_dict[like.comment.id] = {'likes': 0, 'dislikes': 0}
            likes_dict[like.comment.id]['likes'] += like.likes
            likes_dict[like.comment.id]['dislikes'] += like.dislikes

        images = ["".join(u) for u in Product_image.objects.filter(product=product.id).values_list('image')]

        # Получаем всех пользователей, оставивших комментарии
        comment_users = [comment.user for comment in product_comments]
        # Получаем аватары для этих пользователей
        user_avatars = User_avatar.objects.filter(user__in=comment_users)
        # Создаем словарь {user_id: avatar_url} для удобного доступа
        avatars_dict = {avatar.user.id: avatar.img.url if avatar.img else '' for avatar in user_avatars}
        # Получаем рекомендации "с этим товаром покупают"
        related_recommendations = RecommendationService.get_recommendations_for_product(product, limit=4)

        context['avatars_dict'] = avatars_dict
        context['likes_count'] = Comment_likes.objects.filter(comment=self.kwargs['id']).aggregate(total=Sum('likes'))['total'] or 0
        context['dislikes_count'] = Comment_likes.objects.filter(comment=self.kwargs['id']).aggregate(total=Sum('dislikes'))['total'] or 0
        context['product_grade'] = Comments.objects.filter(product=self.kwargs['id']).aggregate(total=Sum('grade')/Count('grade'), count=Count('grade'))
        context['likes_dict'] = likes_dict
        context['product_comments'] = product_comments
        context['comments_images'] = comments_images
        context['user_has_comment'] = "True" if user_comment else "False"
        context['product_has_comments'] = 'True' if product_comments else 'False'
        context['images'] = images
        context['product'] = product
        context['related_recommendations'] = related_recommendations

        return context


#------------------------------------------Операции CRUD с продуктами--------------------------------------
class Create_and_Edit_ancestor(View): #От данного класса наследуются классы Create_product и Edit_product
    model = Product
    fields = ['product_name', 'product_details', 'regular_price', 'discounted_price', 'category', 'sub_category']
    success_url = reverse_lazy('main')
    template_name = "create_and_edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Product_category.objects.values('id', 'category_name')
        context['sub_categories'] = {i['id']: list(Product_subcategory.objects.filter(category_name=i['id']).values('id', 'subcategory_name'))for i in context['categories']}
        return context

    def form_valid(self, form):
        product = form.save(commit=False)
        product.category = Product_category.objects.get(id=self.request.POST.get("category"))
        product.sub_category = Product_subcategory.objects.get(id=self.request.POST.get("sub_category"))
        product.vendor = Vendor.objects.get(user=self.request.user)
        product.save()

        images = self.request.FILES.getlist('images')
        if images:
            for image in images:
                Product_image.objects.create(product=product, image=image)

        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['form_errors'] = form.errors
        context['status'] = f"Ошибка! Форма содержит ошибки: {form.errors}"
        print("FORM ERRORS:", form.errors)  # Для отладки в консоли
        return self.render_to_response(context)

    def handle_no_permission(self):
        return super().handle_no_permission()


class Create_product(PermissionRequiredMixin, LoginRequiredMixin, Create_and_Edit_ancestor, CreateView):

    permission_required = 'magazine.add_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_operation'] = 'Добавление товара'
        return context


class Edit_product(PermissionRequiredMixin, LoginRequiredMixin, Create_and_Edit_ancestor, UpdateView):

    permission_required = 'magazine.change_product'

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект продукта
        product = self.get_object()
        vendor = get_object_or_404(Vendor, user=request.user)

        # Проверка прав доступа
        if product.vendor != vendor and not request.user.is_staff:
            raise PermissionDenied("У вас нет прав для редактирования этого товара")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['editable_stuff'] = Product.objects.get(id=self.kwargs.get('pk'))
        context['editable_product_images'] = [u for u in Product_image.objects.filter(product=self.kwargs.get('pk')).values_list('id', 'image')]
        context['current_operation'] = 'Изменение товара'
        return context


class Delete_product(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):

    model = Product
    success_url = reverse_lazy('main')
    permission_required = 'magazine.delete_goods'

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект продукта
        product = self.get_object()
        vendor = get_object_or_404(Vendor, user=request.user)

        # Проверка прав доступа
        if product.vendor != vendor and not request.user.is_staff:
            raise PermissionDenied("У вас нет прав для редактирования этого товара")

        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return super().handle_no_permission()


class Delete_editable_product_image(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):

    model = Product_image
    permission_required = 'magazine.delete_goods'

    def handle_no_permission(self):
        return super().handle_no_permission()

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', '/')


#Этот декоратор связывает функцию delete_product_image с сигналом post_delete, который отправляется после удаления объекта модели product_image.
#sender: это модель, которая отправила сигнал (в данном случае product_image).
#instance: это экземпляр модели, который был удален. Он содержит все данные этого объекта, включая путь к изображению.
#**kwargs: это дополнительные аргументы, которые могут быть переданы сигналу, но в данном случае они не используются.
@receiver(post_delete, sender=Product_image)
def delete_product_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
#------------------------------------------/Операции CRUD с продуктами--------------------------------------

#------------------------------------------Операции CRUD с категориями--------------------------------------
class Category_list(ListView, LoginRequiredMixin, PermissionRequiredMixin):

    model = Product_category
    context_object_name = "data"
    template_name = 'category_list.html'
    permission_required = 'magazine.view_product_category'

    def handle_no_permission(self):
        return super().handle_no_permission()


class Delete_category(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = Product_category
    success_url = reverse_lazy('category_list')
    permission_required = 'magazine.delete_product_category'

    def handle_no_permission(self):
        return super().handle_no_permission()


@login_required
@permission_required('magazine.add_product_category', raise_exception=True)
def create_category(request):
    category_name = request.POST.get("category_name")
    if category_name:
        category = Product_category(category_name=category_name)
        category.save()
        return redirect('category_list')
    else:
        return redirect('category_list')


class Subcategory_list(ListView, LoginRequiredMixin, PermissionRequiredMixin):

    model = Product_subcategory
    context_object_name = "data"
    template_name = 'subcategory_list.html'
    permission_required = 'magazine.view_product_subcategory'

    def handle_no_permission(self):
        return super().handle_no_permission()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Product_category.objects.values('id', 'category_name')
        return context


class Delete_subcategory(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = Product_subcategory
    success_url = reverse_lazy('subcategory_list')
    permission_required = 'magazine.delete_product_subcategory'

    def handle_no_permission(self):
        return super().handle_no_permission()


@login_required
@permission_required('magazine.add_product_subcategory', raise_exception=True)
def create_subcategory(request):
    subcategory_name = request.POST.get("subcategory_name")
    category = Product_category.objects.get(id=int(request.POST.get("category")))
    if subcategory_name:
        subcategory = Product_subcategory(subcategory_name=subcategory_name, category_name=category)
        subcategory.save()
        return redirect('subcategory_list')
    else:
        return redirect('subcategory_list')
#------------------------------------------/Операции CRUD с категориями--------------------------------------