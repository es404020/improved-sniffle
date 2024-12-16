from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from datetime import date

from expenses.models import User, Expense

class UserModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com'
        }

    def test_user_creation(self):
        user = User.objects.create(**self.user_data)
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.email, self.user_data['email'])

    def test_user_str_method(self):
        user = User.objects.create(**self.user_data)
        self.assertEqual(str(user), self.user_data['username'])

class ExpenseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='expenseuser', 
            email='expense@example.com'
        )
        self.expense_data = {
            'user': self.user,
            'title': 'Lunch',
            'amount': Decimal('25.50'),
            'date': date.today(),
            'category': 'Food'
        }

    def test_expense_creation(self):
        expense = Expense.objects.create(**self.expense_data)
        self.assertEqual(expense.user, self.user)
        self.assertEqual(expense.title, self.expense_data['title'])
        self.assertEqual(expense.amount, self.expense_data['amount'])
        self.assertEqual(expense.category, self.expense_data['category'])

    def test_expense_str_method(self):
        expense = Expense.objects.create(**self.expense_data)
        expected_str = f"{self.expense_data['title']} - {self.expense_data['amount']}"
        self.assertEqual(str(expense), expected_str)

class UserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'apiuser',
            'email': 'api@example.com'
        }
        self.user_url = reverse('user-list')

    def test_create_user(self):
        response = self.client.post(self.user_url, self.user_data, format='json')
        
     
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], f'User successfully created with id 1')
      
        
    
        self.assertTrue(User.objects.filter(username=self.user_data['username']).exists())

    def test_list_users(self):
     
        User.objects.create(username='user1', email='user1@example.com')
        User.objects.create(username='user2', email='user2@example.com')
        
        response = self.client.get(self.user_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class ExpenseAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username='expenseapiuser', 
            email='expenseapi@example.com'
        )
        self.expense_url = reverse('expense-list')
        self.expense_data = {
            'user': self.user.id,
            'title': 'Dinner',
            'amount': '30.75',
            'date': str(date.today()),
            'category': 'Food'
        }

    def test_create_expense(self):
        response = self.client.post(self.expense_url, self.expense_data, format='json')
        
       
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
     
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], f'Expense successfully created with id 1')
       
        
     
        self.assertTrue(Expense.objects.filter(
            user=self.user, 
            title=self.expense_data['title']
        ).exists())

    def test_create_expense_invalid_amount(self):
       
        invalid_expense_data = self.expense_data.copy()
        invalid_expense_data['amount'] = '-10.00'
        
        response = self.client.post(self.expense_url, invalid_expense_data, format='json')
        
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_expenses(self):
   
        Expense.objects.create(
            user=self.user,
            title='Lunch',
            amount=Decimal('25.50'),
            date=date.today(),
            category='Food'
        )
        Expense.objects.create(
            user=self.user,
            title='Transport',
            amount=Decimal('15.00'),
            date=date.today(),
            category='Travel'
        )
        
        response = self.client.get(self.expense_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class CategorySummaryAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username='summaryuser', 
            email='summary@example.com'
        )
        
     
        Expense.objects.create(
            user=self.user,
            title='Lunch',
            amount=Decimal('25.50'),
            date=date(2024, 1, 15),
            category='Food'
        )
        Expense.objects.create(
            user=self.user,
            title='Dinner',
            amount=Decimal('35.75'),
            date=date(2024, 1, 20),
            category='Food'
        )
        Expense.objects.create(
            user=self.user,
            title='Transport',
            amount=Decimal('50.00'),
            date=date(2024, 1, 10),
            category='Travel'
        )

    def test_category_summary(self):
        url = reverse('expense-category-summary', kwargs={
            'user_id': self.user.id, 
            'year': 2024, 
            'month': 1
        })
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        summary_dict = {item['category']: item['total_amount'] for item in response.data}
        
        
        self.assertAlmostEqual(float(summary_dict['Food']), 61.25)
        self.assertAlmostEqual(float(summary_dict['Travel']), 50.00)