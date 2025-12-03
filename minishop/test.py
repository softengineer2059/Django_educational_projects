"""import sqlite3
import random
import string

# Connect to the SQLite database
conn = sqlite3.connect('goods.db')
c = conn.cursor()

# Define product categories
categories = ['Электроника', 'Одежда', 'Домашний декор', 'Спорт', 'Книги']

# Generate and insert random data
for i in range(20):
    product_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    regular_price = random.randint(50, 500)
    discounted_price = regular_price * 0.5
    stock_quantity = random.randint(10, 100)
    product_details = ''.join(random.choices(string.ascii_letters + string.digits, k=100))
    category = random.choice(categories)

    c.execute("INSERT INTO goods (product, regular_price, discounted_price, stock_quantity, product_details, category) VALUES (?, ?, ?, ?, ?, ?)",
              (product_name, regular_price, discounted_price, stock_quantity, product_details, category))

conn.commit()
conn.close()"""


from magazine.models import *
from django.db.models import Sum, Count


product_grade = comments.objects.values('product').annotate(total_grade=Sum('grade') / Count('grade'))
product_grade_count = comments.objects.values('product').annotate(count=Count('grade'))

print(product_grade)