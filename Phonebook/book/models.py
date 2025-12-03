from django.db import models


class departments(models.Model):

    department_name = models.CharField(max_length=200, verbose_name="Отделение")

    class Meta:
        verbose_name = "Отделение"
        verbose_name_plural = "Отделения"
        managed = True

    def __str__(self):
        return self.department_name


class personnel(models.Model):

    employee_full_name = models.CharField(max_length=400, verbose_name="ФИО")
    position = models.CharField(max_length=300, verbose_name="Должность")
    phone = models.CharField(max_length=300, verbose_name="Телефон")
    mail = models.CharField(max_length=300, verbose_name="Почта", blank=True, null=True)
    department = models.ForeignKey(departments, blank=True, null=True, verbose_name="Отделение", on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"


class admin_departments(models.Model):

    department_name = models.CharField(max_length=200, verbose_name="Отдел")

    class Meta:
        verbose_name = "Отдел"
        verbose_name_plural = "Отделения"
        managed = True

    def __str__(self):
        return self.department_name


class admin_personnel(models.Model):

    employee_full_name = models.CharField(max_length=400, verbose_name="ФИО")
    position = models.CharField(max_length=300, verbose_name="Должность")
    phone = models.CharField(max_length=300, verbose_name="Телефон")
    mail = models.CharField(max_length=300, verbose_name="Почта", blank=True, null=True,)
    department = models.ForeignKey(admin_departments, blank=True, null=True, verbose_name="Отдел", on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

