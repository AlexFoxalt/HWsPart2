from django.test import TestCase

# Create your tests here.

from datetime import date
from faker import Faker

f = Faker('EN')


x = date.today()
y = f.date_between(start_date='today', end_date='+30y')

print(x)
print(y)
print((x - y).days)
