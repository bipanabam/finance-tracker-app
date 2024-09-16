import random
from faker import Faker
from django.core.management.base import BaseCommand
from tracker.models import User, Transaction, Category

class Command(BaseCommand):
    help = "Generates transactions for testing"

    def handle(self, *args, **options):
        fake = Faker()

        categories = [
            "Bills",
            "Food", 
            "Groceries",
            "Clothes",
            "Medical",
            "Housing",
            "Salary",
            "Social",
            "Transport",
            "Vacation",
            "Cat",
            "Bill Sharing",
        ]

        for category in categories:
            Category.objects.get_or_create(name=category)
        
        user = User.objects.filter(username='bipanabam').first()
        if not user:
            user = User.objects.create_superuser(username='bipanabam', password='test')

        categories = Category.objects.all()
        types = [x[0] for x in Transaction.TRANSACTION_TYPE_CHOICES]
        for i in range(20):
            Transaction.objects.create(
                category=random.choice(categories),
                user=user,
                amount=random.uniform(1, 2500),
                date=fake.date_between(start_date='-1y', end_date='today'),
                type=random.choice(types)
            )