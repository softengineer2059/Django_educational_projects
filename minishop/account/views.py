from django.contrib.auth import update_session_auth_hash
from django.core.files.storage import default_storage
from django.contrib import messages
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.views.generic import ListView, FormView, View, DeleteView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login
from django.db.models import Sum
from django.urls import reverse_lazy
from cart.models import Cart
from .models import User_avatar
from magazine.models import *
from .forms import *
from django.forms import formset_factory, modelformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class Account(LoginRequiredMixin, ListView):
    model = User_avatar
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_items_counts'] = Cart.objects.filter(user=self.request.user).aggregate(total=Sum('quantity'))['total']
        context['current_user'] = self.request.user
        return context


class Login(LoginView):

    form_class = LoginForm
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('main')


class Logout(LogoutView):

    next_page = "main"


class Register(FormView):

    form_class = UserRegister
    success_url = reverse_lazy('main')
    template_name = "register.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
        # buyers_group = Group.objects.get(name='buyers')
        # user.groups.add(buyers_group)


@login_required
def change_base_info(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    else:
        form = UserUpdateForm(instance=request.user)
    return redirect('profile')


class ChangePasswordView(PermissionRequiredMixin, LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        current_password = request.POST.get('current_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if not request.user.check_password(current_password):
            messages.error(request, 'Не правильно введен текущий пароль')
            return redirect('profile')

        elif new_password1 != new_password2:
            messages.error(request, 'Пароли введеные в поле 1 и 2 не совпадают')

        elif len(new_password1) < 8:
            messages.error(request, 'Пароль должен содержать не менее 8 символов')
            return redirect('profile')

        else:
            request.user.set_password(new_password1)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Пароль успешно изменен!')

        return redirect('profile')


def upload_avatar_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Получаем новое изображение
        new_image = request.FILES['image']

        # Удаляем старую аватарку, если она существует
        try:
            old_avatar = User_avatar.objects.get(user=request.user)
            if old_avatar.img:
                # Удаляем файл из файловой системы
                default_storage.delete(old_avatar.img.path)
            # Удаляем запись из базы данных
            old_avatar.delete()
        except User_avatar.DoesNotExist:
            pass  # У пользователя не было аватарки

        # Создаем новую запись с новым изображением
        User_avatar.objects.create(user=request.user, img=new_image)

        return redirect('profile')

    return redirect('profile')  # Если не POST-запрос или нет файла


@login_required
def become_vendor(request):
    # Проверяем, не является ли пользователь уже продавцом
    if hasattr(request.user, 'vendor'):
        return redirect('vendor_dashboard')

    WarehouseFormSet = formset_factory(VendorWarehouseForm, extra=1, min_num=1, validate_min=True)

    if request.method == 'POST':
        vendor_form = VendorRegistrationForm(request.POST, request.FILES)
        warehouse_formset = WarehouseFormSet(request.POST, prefix='warehouse')

        if vendor_form.is_valid() and warehouse_formset.is_valid():
            # Сохраняем основную информацию продавца
            vendor = vendor_form.save(commit=False)
            vendor.user = request.user
            vendor.is_approved = False  # Требует модерации
            vendor.save()

            # Сохраняем склады
            for form in warehouse_formset:
                if form.cleaned_data:
                    warehouse = form.save(commit=False)
                    warehouse.vendor = vendor
                    warehouse.save()

            messages.success(
                request,
                'Заявка на регистрацию отправлена! Ожидайте подтверждения администратора.'
            )
            return redirect('vendor_dashboard')

    else:
        vendor_form = VendorRegistrationForm()
        warehouse_formset = WarehouseFormSet(prefix='warehouse')

    context = {
        'vendor_form': vendor_form,
        'warehouse_formset': warehouse_formset,
        'step_titles': ['Основная информация', 'Склады', 'Доставка'],
    }

    return render(request, 'become_vendor.html', context)


class Edit_vendor_base_info(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Vendor
    form_class = VendorRegistrationForm  # Используем вашу кастомную форму
    success_url = reverse_lazy('vendor_dashboard')
    template_name = "edit_vendor_info.html"
    permission_required = 'account.change_vendor'

    def handle_no_permission(self):
        return super().handle_no_permission()

    def get_object(self, queryset=None):
        # Получаем Vendor для текущего пользователя
        return self.request.user.vendor

    def form_valid(self, form):
        form.instance.is_approved = False

        # Получаем текущий объект до сохранения
        current_vendor = self.get_object()
        old_logo = current_vendor.logo

        # Сохраняем форму
        response = super().form_valid(form)

        # Если лого было изменено и старое лого существует - удаляем его
        if (old_logo and
                old_logo != self.object.logo and
                old_logo.name):
            try:
                default_storage.delete(old_logo.path)
            except Exception:
                # Игнорируем ошибки при удалении файла
                pass

        return response


@login_required
def vendor_dashboard(request):
    if not hasattr(request.user, 'vendor'):
        return redirect('become_vendor')

    vendor = request.user.vendor
    vendor_with_delivery = Vendor.objects.select_related(
        'vendordeliverysettings'
    ).prefetch_related(
        'vendordeliverysettings__region_prices'
    ).get(pk=vendor.pk)

    context = {
        'vendor': vendor_with_delivery,
        'product_count': Product.objects.filter(vendor=vendor).count(),
    }

    return render(request, 'vendor_profile.html', context)


def vendor_delivery_settings(request):
    RegionDeliveryPriceFormSet = modelformset_factory(
        RegionDeliveryPrice,
        form=RegionDeliveryPriceForm,
        extra=1,  # Одна пустая форма для добавления
        can_delete=True
    )
    vendor_settings, created = VendorDeliverySettings.objects.get_or_create(
        vendor=request.user.vendor
    )
    if request.method == 'POST':
        settings_form = VendorDeliverySettingsForm(request.POST, instance=vendor_settings)
        formset = RegionDeliveryPriceFormSet(request.POST, queryset=RegionDeliveryPrice.objects.filter(
            vendor_settings=vendor_settings))

        if settings_form.is_valid() and formset.is_valid():
            settings_form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.vendor_settings = vendor_settings
                instance.save()
            # Удаляем отмеченные для удаления
            for obj in formset.deleted_objects:
                obj.delete()
            return redirect('vendor_dashboard')
    else:
        settings_form = VendorDeliverySettingsForm(instance=vendor_settings)
        formset = RegionDeliveryPriceFormSet(
            queryset=RegionDeliveryPrice.objects.filter(vendor_settings=vendor_settings))

    return render(request, 'edit_deliverysettings.html', {
        'settings_form': settings_form,
        'formset': formset
    })


@login_required
def change_vendorwarehouse_info(request, warehouse_id=None):
    """
    Создание или редактирование склада продавца
    warehouse_id - если None, создается новый склад, иначе редактируется существующий
    """
    # Получаем объект Vendor для текущего пользователя
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        messages.error(request, 'Профиль продавца не найден.')
        return redirect('vendor_dashboard')

    # Получаем или создаем объект склада
    if warehouse_id:
        try:
            warehouse = get_object_or_404(VendorWarehouse, id=warehouse_id, vendor=vendor)
        except VendorWarehouse.DoesNotExist:
            warehouse = None
    else:
        warehouse = None

    if request.method == "POST":
        form = VendorWarehouseForm(request.POST, instance=warehouse)
        if form.is_valid():
            warehouse = form.save(commit=False)
            warehouse.vendor = vendor  # Используем объект Vendor, а не User

            # Если это основной склад, снимаем флаг с других складов
            if warehouse.is_default:
                VendorWarehouse.objects.filter(vendor=vendor, is_default=True).update(is_default=False)

            warehouse.save()

            messages.success(request, 'Склад успешно сохранен!')
            return redirect('vendor_dashboard')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = VendorWarehouseForm(instance=warehouse)

    context = {
        'form': form,
        'warehouse': warehouse,
        'is_edit': warehouse_id is not None
    }
    return render(request, "edit_warehouse.html", context)


class Delete_Warehouse(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):

    model = VendorWarehouse
    success_url = reverse_lazy('vendor_dashboard')
    permission_required = 'account.delete_vendorwarehouse'

    def handle_no_permission(self):
        return super().handle_no_permission()


"""При удалении пользователя удаляется запись в связанной таблице User_avatar
что вызывает данную функцию которая удаляет файлы аватарок из папки media
pre_delete предпочтительней post_delete так-как файл удаляется перед удалением записи в бд"""
@receiver(pre_delete, sender=User_avatar)
def delete_avatar_file(sender, instance, **kwargs):
    if instance.img:
        instance.img.delete(save=False)


@receiver(pre_delete, sender=Vendor)
def delete_vendor_logo(sender, instance, **kwargs):
    if instance.logo:
        instance.logo.delete(save=False)


class Vendor_product(ListView):

    model = Product
    template_name = 'vendor_shop.html'
    context_object_name = 'goods'
    paginate_by = 4

    def get_queryset(self, **kwargs):
        try:
            vendor = Vendor.objects.get(id=self.kwargs['id'])
            queryset = Product.objects.filter(vendor=vendor)
            return queryset
        except Vendor.DoesNotExist:
            return Product.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = {}
        vendor = Vendor.objects.get(id=self.kwargs['id'])
        for i in Product.objects.values('id'):
            product_images = Product_image.objects.filter(product=i['id']).values_list('image', flat=True)
            images[i['id']] = list(product_images)
        context['images'] = images
        context['vendor'] = vendor
        context['product_count'] = Product.objects.filter(vendor=vendor).count()
        return context

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by)