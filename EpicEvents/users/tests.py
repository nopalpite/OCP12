from django.test import TestCase
from .models import User



class UserTestCase(TestCase):
    def setUp(self):
        self.superuser_data = {
            'email': 'test@example.com',
            'password': 'password123',
        }
        self.staff_user_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'role': 'management',
        }
        self.sales_user_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'role': 'sales',
        }


    def test_create_staff_user(self):
        user = User.objects.create_user(**self.sales_user_data)
        self.assertEqual(user.email, self.sales_user_data['email'])
        self.assertTrue(user.check_password(self.sales_user_data['password']))
        self.assertEqual(user.role, self.sales_user_data['role'])
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(**self.superuser_data)
        self.assertEqual(superuser.email, self.superuser_data['email'])
        self.assertTrue(superuser.check_password(self.superuser_data['password']))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)

    
    def test_user_str(self):
        user = User.objects.create_user(**self.staff_user_data)
        expected_str = f"{self.staff_user_data['email']} ({self.staff_user_data['role']})"
        self.assertEqual(str(user), expected_str)
