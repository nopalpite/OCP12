from django.urls import reverse_lazy
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from contracts.models import Contract
from events.models import Event
from status.models import Status
from clients.models import Client


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
        self.contract_1_data = {
            'sales_contact': self.sales_user,
            'amount': 20000,
            'payment_due': "2023-07-20",
            'status': True
        }
        self.contract_2_data = {
            'sales_contact': self.sales_user,
            'amount': 40000,
            'payment_due': "2023-08-12",
            'status': True
        }
        self.event_1_data = {
            'name': 'super event',
            'support_contact': self.support_user,
            'location': 'Dubai',
        }
        self.event_2_data = {
            'name': 'mega event',
            'support_contact': self.support_user,
            'location': 'Paris',
        }

    def test_sales_user_create_event(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.sales_token)
        client = Client.objects.create(**self.client_1_data)
        contract = Contract.objects.create(
            **self.contract_1_data, client=client)
        data = self.event_1_data.copy()
        data["contract"] = contract.pk
        response = self.client.post(reverse_lazy('events-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_support_user_cannnot_create_event(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.support_token)
        client = Client.objects.create(**self.client_1_data)
        contract = Contract.objects.create(
            **self.contract_1_data, client=client)
        data = self.event_1_data.copy()
        data["contract"] = contract.pk
        response = self.client.post(reverse_lazy('events-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_events_list_for_sales_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.sales_token)
        client_1 = Client.objects.create(**self.client_1_data)
        client_2 = Client.objects.create(**self.client_2_data)
        contract_1 = Contract.objects.create(
            **self.contract_1_data, client=client_1)
        contract_2 = Contract.objects.create(
            **self.contract_2_data, client=client_2)
        event_1 = Event.objects.create(
            **self.event_1_data, contract=contract_1)
        event_2 = Event.objects.create(
            **self.event_2_data, contract=contract_2)
        response = self.client.get(reverse_lazy('events-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert b'Dubai' in response.content
        assert b'Paris' in response.content

    def test_get_events_list_for_support_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.support_token)
        client_1 = Client.objects.create(**self.client_1_data)
        client_2 = Client.objects.create(**self.client_2_data)
        contract_1 = Contract.objects.create(
            **self.contract_1_data, client=client_1)
        contract_2 = Contract.objects.create(
            **self.contract_2_data, client=client_2)
        event_1 = Event.objects.create(
            **self.event_1_data, contract=contract_1)
        event_2 = Event.objects.create(
            **self.event_2_data, contract=contract_2)
        response = self.client.get(reverse_lazy('events-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert b'Dubai' in response.content
        assert b'Paris' in response.content

    def test_get_event_by_client_lastname(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.sales_token)
        client_1 = Client.objects.create(**self.client_1_data)
        client_2 = Client.objects.create(**self.client_2_data)
        contract_1 = Contract.objects.create(
            **self.contract_1_data, client=client_1)
        contract_2 = Contract.objects.create(
            **self.contract_2_data, client=client_2)
        event_1 = Event.objects.create(
            **self.event_1_data, contract=contract_1)
        event_2 = Event.objects.create(
            **self.event_2_data, contract=contract_2)
        response = self.client.get("/events/?contract__client__last_name=Doe")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert b'Dubai' in response.content
        assert b'Paris' not in response.content

    def test_get_event_by_client_email(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.sales_token)
        client_1 = Client.objects.create(**self.client_1_data)
        client_2 = Client.objects.create(**self.client_2_data)
        contract_1 = Contract.objects.create(
            **self.contract_1_data, client=client_1)
        contract_2 = Contract.objects.create(
            **self.contract_2_data, client=client_2)
        event_1 = Event.objects.create(
            **self.event_1_data, contract=contract_1)
        event_2 = Event.objects.create(
            **self.event_2_data, contract=contract_2)
        response = self.client.get("/events/?contract__client__email=john.doe@example.com")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert b'Dubai' in response.content
        assert b'Paris' not in response.content

    def test_get_event_by_id(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.sales_token)
        client_1 = Client.objects.create(**self.client_1_data)
        client_2 = Client.objects.create(**self.client_2_data)
        contract_1 = Contract.objects.create(
            **self.contract_1_data, client=client_1)
        contract_2 = Contract.objects.create(
            **self.contract_2_data, client=client_2)
        event_1 = Event.objects.create(
            **self.event_1_data, contract=contract_1)
        event_2 = Event.objects.create(
            **self.event_2_data, contract=contract_2)
        response = self.client.get(f"/events/{event_1.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert b'Dubai' in response.content
        assert b'Paris' not in response.content
