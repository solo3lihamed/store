import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

def populate():
    products = [
        {
            'name': 'قميص عجيب',
            'description': 'قميص بألوان صارخة وتصميم غريب.',
            'price': 150.00,
            'category': 'clothes',
            'image': None 
        },
        {
            'name': 'بنطال واسع',
            'description': 'بنطال مريح جداً وعصري.',
            'price': 200.00,
            'category': 'clothes',
            'image': None
        },
        {
            'name': 'حذاء نيون',
            'description': 'حذاء يضيء في الظلام.',
            'price': 350.00,
            'category': 'shoes',
            'image': None
        },
        {
            'name': 'شبشب كلاسيك',
            'description': 'شبشب مريح للمنزل.',
            'price': 50.00,
            'category': 'shoes',
            'image': None
        }
    ]

    for p in products:
        Product.objects.create(**p)
        print(f"Created {p['name']}")

if __name__ == '__main__':
    populate()
