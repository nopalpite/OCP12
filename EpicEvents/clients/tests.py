from django.urls import reverse_lazy
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from contracts.models import Contract
from events.models import Event
from status.models import Status
from .models import Client

class ClientAPITestCase(APITestCase):
    
    def setUp(self):
        self.sales_user = User.objects.create_user(
            email='sales@example.com',
            password='password123',
            role='sales'
        )
        self.support_user = User.objects.create_user(
            email='support@example.com',
            password='password123',
            role='support'
        )
        self.sales_token = str(AccessToken.for_user(self.sales_user))
        self.support_token = str(AccessToken.for_user(self.support_user))
        self.client_1_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '123456789',
            'mobile': '987654321',
            'company_name': 'ACME Inc.',
            'sales_contact': self.sales_user,
            'is_active': True
        }
        self.client_2_data = {
            'first_name': 'Bob',
            'last_name': 'Grill',
            'email': 'bob.grill@example.com',
            'phone': '123456789',
            'mobile': '987654321',
            'company_name': 'ACME Inc.',
            'sales_contact': self.sales_user,
            'is_active': True
        }
        self.contract_data = {
            'sales_contact': self.sales_user,
            'amount': 20000,
            'payment_due': "2023-07-20",
            'status': True
        }
        self.event_data  = {
            'name': 'super event',
            'support_contact': self.support_user,

        }
    
    def test_sales_user_create_client(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.sales_token)
        response = self.client.post(reverse_lazy('clients-list'), data=self.client_1_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_support_user_cannnot_create_client(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.support_token)
        response = self.client.post(reverse_lazy('clients-list'), data=self.client_1_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_clients_list_for_sales_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.sales_token)
        Client.objects.create(**self.client_1_data)
        Client.objects.create(**self.client_2_data)
        response = self.client.get(reverse_lazy('clients-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert b'john.doe@example.com' in response.content
        assert b'bob.grill@example.com' in response.content

    def test_get_clients_list_for_support_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.support_token)
        client = Client.objects.create(**self.client_1_data)
        event_status = Status.objects.create(name="en cours")
        contract = Contract.objects.create(**self.contract_data, client=client)
        Event.objects.create(**self.event_data, status=event_status, contract=contract)
        response = self.client.get(reverse_lazy('clients-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert b'john.doe@example.com' in response.content
        assert b'bob.grill@example.com' not in response.content
    
    def test_get_client_by_email(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.sales_token)
        Client.objects.create(**self.client_1_data)
        Client.objects.create(**self.client_2_data)
        response = self.client.get("/clients/?email=john.doe@example.com")
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert b'john.doe@example.com' in response.content
        assert b'bob.grill@example.com' not in response.content

    def test_get_client_by_last_name(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.sales_token)
        Client.objects.create(**self.client_1_data)
        Client.objects.create(**self.client_2_data)
        response = self.client.get("/clients/?last_name=Doe")
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert b'john.doe@example.com' in response.content
        assert b'bob.grill@example.com' not in response.content

    def test_get_client_by_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.sales_token)
        client = Client.objects.create(**self.client_1_data)
        Client.objects.create(**self.client_2_data)
        response = self.client.get(f"/clients/{client.pk}/")
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert b'john.doe@example.com' in response.content
        assert b'bob.grill@example.com' not in response.content