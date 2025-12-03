from django.db import models
from django.core.validators import FileExtensionValidator
from magazine.models import Product
from django.contrib.auth.models import User




class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.CharField(blank=True, verbose_name='комментарий')
    grade = models.SmallIntegerField(blank=False, verbose_name='оценка')
    created_at = models.DateTimeField(auto_now_add=True)


class Comment_images(models.Model):
    comment = models.ForeignKey(Comments, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='comment_images/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])])


class Comment_likes(models.Model):
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(verbose_name='Количество лайков')
    dislikes = models.IntegerField(verbose_name='Количество дизлайков')