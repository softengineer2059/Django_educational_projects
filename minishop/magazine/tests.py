from .models import *
from django.db.models import Sum, Count


product_grade = comments.objects.values('product').annotate(total_grade=Sum('grade') / Count('grade'), count=Count('grade'))
#product_grade_count = comments.objects.values('product').annotate(count=Count('grade'))

print(product_grade)