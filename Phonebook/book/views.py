from .models import *
from .forms import *
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy


#------------------------------------------------------Отделения------------------------------------------------------

class Main(ListView):

    model = personnel
    template_name = 'departments_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = departments.objects.values_list('id', 'department_name')
        context['first_letter'] = sorted(set(i[0] for i in departments.objects.values_list('department_name', flat=True)))
        context['path'] = 'departments'
        context['search_key'] = "search_personnel"
        return context


class Departments(ListView):

    model = personnel
    template_name = 'dep_persons_list.html'
    context_object_name = 'data'
    department = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['department'] = departments.objects.get(id=self.department)
        context['department_id'] = self.department
        context['departments'] = departments.objects.values_list('id', 'department_name')
        context['first_letter'] = sorted(set(i[0] for i in departments.objects.values_list('department_name', flat=True)))
        context['search_key'] = "search_personnel"
        context['path'] = 'departments'
        return context

    def get_queryset(self):
        self.department = self.kwargs.get('pk')
        queryset = personnel.objects.filter(department=self.department)
        return queryset


class Create_dep_departments(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    model = departments
    fields = '__all__'
    permission_required = 'departments.add_departments'
    success_url = reverse_lazy('main')

    def handle_no_permission(self):
        return super().handle_no_permission()

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class Create_dep_personnel(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    model = personnel
    fields = '__all__'
    permission_required = 'personnel.add_personnel'
    success_url = reverse_lazy('main')

    def handle_no_permission(self):
        return super().handle_no_permission()

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class Delete_dep_departments(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = departments
    permission_required = 'departments.delete_departments'
    template_name = 'confirm_delete.html'

    def handle_no_permission(self):
        return super().handle_no_permission()

    def get_success_url(self):
        # Возвращаем на предыдущую страницу
        return self.request.META.get('HTTP_REFERER', reverse_lazy('main'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = "отделения"
        return context


class Delete_dep_personnel(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = personnel
    permission_required = 'personnel.delete_personnel'
    template_name = 'confirm_delete.html'

    def handle_no_permission(self):
        return super().handle_no_permission()

    def get_success_url(self):
        # Возвращаем на предыдущую страницу
        return self.request.META.get('HTTP_REFERER', reverse_lazy('main'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = "данных сотрудника"
        return context


class Edit_dep_personnel(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    model = personnel
    fields = "__all__"
    permission_required = 'personnel.change_personnel'
    template_name = 'edit_contact_modal.html'
    context_object_name = 'persons'

    def handle_no_permission(self):
        return super().handle_no_permission()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = departments.objects.values_list('id', 'department_name')
        context['current_personne'] = personnel.objects.get(id=self.kwargs.get('pk'))
        return context

    def get_success_url(self):
        # Возвращаем на предыдущую страницу
        return self.request.META.get('HTTP_REFERER', reverse_lazy('main'))

#------------------------------------------------------/Отделения------------------------------------------------------

class Search(ListView):

    template_name = 'dep_persons_list.html'
    context_object_name = 'data'

    def get_queryset(self):
        get_search = self.request.GET.get("search")
        base = self.kwargs.get('base')
        if base == 'personnel':
            queryset = (personnel.objects.filter(employee_full_name__icontains=get_search) | personnel.objects.filter(position__icontains=get_search) |
                    personnel.objects.filter(phone__icontains=get_search) | personnel.objects.filter(mail__icontains=get_search))
        elif base == 'admin_personnel':
            self.template_name = 'adm_persons_list.html'
            queryset = (admin_personnel.objects.filter(employee_full_name__icontains=get_search) | admin_personnel.objects.filter(
                position__icontains=get_search) | admin_personnel.objects.filter(phone__icontains=get_search) | admin_personnel.objects.filter(mail__icontains=get_search))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('base') == 'personnel':
            context['search_key'] = "search_personnel"
        else:
            context['search_key'] = "search_admin_personnel"
        return context
#------------------------------------------------------Управление------------------------------------------------------

class Administration(ListView):

    model = admin_personnel
    template_name = 'admin_departments_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = admin_departments.objects.values_list('id', 'department_name')
        context['first_letter'] = sorted(set(i[0] for i in admin_departments.objects.values_list('department_name', flat=True)))
        context['path'] = 'admin_departments'
        context['search_key'] = "search_admin_personnel"
        return context


class Admin_departments(ListView):

    model = admin_personnel
    template_name = 'adm_persons_list.html'
    context_object_name = 'data'
    department = ''

    def get_context_data(self, **kwarg):
        context = super().get_context_data(**kwarg)
        context['department'] = admin_departments.objects.get(id=self.department)
        context['departments'] = admin_departments.objects.values_list('id', 'department_name')
        context['first_letter'] = sorted(set(i[0] for i in admin_departments.objects.values_list('department_name', flat=True)))
        context['search_key'] = "search_admin_personnel"
        context['path'] = 'admin_departments'
        return context

    def get_queryset(self):
        self.department = self.kwargs.get('pk')
        queryset = admin_personnel.objects.filter(department=self.department)
        return queryset


class Create_adm_departments(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    model = admin_departments
    fields = '__all__'
    permission_required = 'admin_departments.add_admin_departments'
    success_url = reverse_lazy('administration')

    def handle_no_permission(self):
        return super().handle_no_permission()

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class Create_adm_personnel(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    model = admin_personnel
    fields = '__all__'
    permission_required = 'admin_personnel.add_admin_personnel'
    success_url = reverse_lazy('administration')

    def handle_no_permission(self):
        return super().handle_no_permission()

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class Delete_adm_departments(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = admin_departments
    permission_required = 'admin_departments.delete_admin_departments'
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('administration')

    def handle_no_permission(self):
        return super().handle_no_permission()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = "отдела"
        return context


class Delete_adm_personnel(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = admin_personnel
    permission_required = 'admin_personnel.delete_admin_personnel'
    template_name = 'confirm_delete.html'

    def handle_no_permission(self):
        return super().handle_no_permission()

    def get_success_url(self):
        # Возвращаем на предыдущую страницу
        return self.request.META.get('HTTP_REFERER', reverse_lazy('main'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = "данных сотрудника"
        return context


class Edit_adm_personnel(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    model = admin_personnel
    fields = "__all__"
    permission_required = 'admin_personnel.change_admin_personnel'
    template_name = 'edit_contact_modal.html'
    context_object_name = 'persons'

    def handle_no_permission(self):
        return super().handle_no_permission()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = admin_departments.objects.values_list('id', 'department_name')
        context['current_personne'] = admin_personnel.objects.get(id=self.kwargs.get('pk'))
        return context

    def get_success_url(self):
        # Возвращаем на предыдущую страницу
        return self.request.META.get('HTTP_REFERER', reverse_lazy('administration'))

#------------------------------------------------------/Управление------------------------------------------------------


#------------------------------------------/Аккаунт--------------------------------------
class Login(LoginView):

    form_class = LoginForm
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('main')


class Logout(LogoutView):

    next_page = "main"
#------------------------------------------/Аккаунт--------------------------------------