import random
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.budgets.models import Budget
from apps.categories.models import Category
from apps.expenses.models import Expense


class Command(BaseCommand):
    help = "Generate test data for Expense Tracker"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("🧩 Generating test data..."))

        # Очистим старые данные (по желанию)
        Expense.objects.all().delete()
        Category.objects.all().delete()
        Budget.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        # Создаём тестовых пользователей
        users = []
        usernames = [
            "alice",
            "bob",
            "charlie",
            "dave",
            "eve",
            "frank",
            "grace",
            "heidi",
            "ivan",
            "judy",
            "mallory",
            "niaj",
            "oscar",
            "peggy",
            "trent",
            "victor",
            "walter",
            "xavier",
            "yvonne",
            "zara",
        ]
        for name in usernames:
            user = User.objects.create_user(
                username=name, password="1234", email=f"{name}@example.com"
            )
            users.append(user)
        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(users)} users."))

        # Создаём категории
        category_names = ["Food", "Transport", "Entertainment", "Bills", "Shopping"]
        categories = []
        for user in users:
            for cat_name in category_names:
                cat = Category.objects.create(
                    name=f"{cat_name} ({user.username})", users=user
                )
                categories.append(cat)
        self.stdout.write(
            self.style.SUCCESS(f"✅ Created {len(categories)} categories.")
        )

        # Создаём расходы
        expenses = []
        for user in users:
            user_cats = Category.objects.filter(users=user)
            for _ in range(15):
                cat = random.choice(user_cats)
                amount = Decimal(random.uniform(5, 150)).quantize(Decimal("0.01"))
                days_ago = random.randint(1, 60)
                exp_date = date.today() - timedelta(days=days_ago)

                expense = Expense.objects.create(
                    descrption=f"Expense for {cat.name}",
                    users=user,
                    categories=cat,
                    amount=amount,
                    date=exp_date,
                )
                expenses.append(expense)
        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(expenses)} expenses."))

        # Создаём бюджеты
        budgets = []
        for user in users:
            for month_offset in range(3):  # последние 3 месяца
                month_date = date.today().replace(day=1) - timedelta(
                    days=30 * month_offset
                )
                limit = Decimal(random.uniform(500, 2000)).quantize(Decimal("0.01"))
                budget = Budget.objects.create(
                    users=user, monthly_limit=limit, month=month_date
                )
                budgets.append(budget)
        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(budgets)} budgets."))

        self.stdout.write(self.style.SUCCESS("🎉 Test data generated successfully!"))
