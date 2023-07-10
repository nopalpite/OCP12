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
        self.event_data = {
            'name': 'super event',
            'support_contact': self.support_user,

        }

    def test_sales_user_create_contract(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.sales_token)
        client = Client.objects.create(**self.client_1_data)
        data = self.contract_1_data.copy()
        data["client"] = client.pk
        response = self.client.post(reverse_lazy('contracts-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_support_user_cannnot_create_contract(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.support_token)
        client = Client.objects.create(**self.client_1_data)
        data = self.contract_1_data.copy()
        data["client"] = client.pk
        response = self.client.post(reverse_lazy('contracts-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_contracts_list_for_sales_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.sales_token)
        client_1 = Client.objects.create(**self.client_1_data)
        client_2 = Client.objects.create(**self.client_2_data)
        contract_1 = Contract.objects.create(
            **self.contract_1_data, client=client_1)
        contract_2 = Contract.objects.create(
            **self.contract_2_data, client=client_2)
        response = self.client.get(reverse_lazy('contracts-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert b'2023-07-20' in response.content
        assert b'2023-08-12' in response.content

    def test_get_contracts_list_for_support_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.support_token)
        client = Client.objects.create(**self.client_1_data)
        event_status = Status.objects.create(name="en cours")
        contract_1 = Contract.objects.create(
            **self.contract_1_data, client=client)
        contract_2 = Contract.objects.create(
            **self.contract_2_data, client=client)
        Event.objects.create(
            **self.event_data, status=event_status, contract=contract_1)
        response = self.client.get(reverse_lazy('contracts-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert b'2023-07-20' in response.content
        assert b'2023-08-12' not in response.content

    def test_get_contract_by_client_lastname(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.sales_token)
        client_1 = Client.objects.create(**self.client_1_data)
        client_2 = Client.objects.create(**self.client_2_data)
        contract_1 = Contract.objects.create(
            **self.contract_1_data, client=client_1)
        contract_2 = Contract.objects.create(
            **self.contract_2_data, client=client_2)
        response = self.client.get("/contracts/?client__last_name=Doe")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert b'2023-07-20' in response.content
        assert b'2023-08-12' not in response.content

    def test_get_contract_by_client_email(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.sales_token)
        client_1 = Client.objects.create(**self.client_1_data)
        client_2 = Client.objects.create(**self.client_2_data)
        contract_1 = Contract.objects.create(
            **self.contract_1_data, client=client_1)
        contract_2 = Contract.objects.create(
            **self.contract_2_data, client=client_2)
        response = self.client.get(
            "/contracts/?client__email=john.doe@example.com")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert b'2023-07-20' in response.content
        assert b'2023-08-12' not in response.content

    def test_get_contract_by_amount(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.sales_token)
        client_1 = Client.objects.create(**self.client_1_data)
        client_2 = Client.objects.create(**self.client_2_data)
        contract_1 = Contract.objects.create(
            **self.contract_1_data, client=client_1)
        contract_2 = Contract.objects.create(
            **self.contract_2_data, client=client_2)
        response = self.client.get("/contracts/?amount=20000")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert b'2023-07-20' in response.content
        assert b'2023-08-12' not in response.content

    def test_get_contract_by_id(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.sales_token)
        client_1 = Client.objects.create(**self.client_1_data)
        client_2 = Client.objects.create(**self.client_2_data)
        contract_1 = Contract.objects.create(
            **self.contract_1_data, client=client_1)
        contract_2 = Contract.objects.create(
            **self.contract_2_data, client=client_2)
        response = self.client.get(f"/contracts/{contract_1.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert b'2023-07-20' in response.content
        assert b'2023-08-12' not in response.content

    def test_sales_user_patch_contract(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.sales_token)
        client = Client.objects.create(**self.client_1_data)
        contract = Contract.objects.create(**self.contract_1_data, client=client)
        response = self.client.patch(f"/contracts/{contract.pk}/", data={"amount": 100000})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert b'100000' in response.content
        assert b'20000' not in response.content

    def test_support_user_cannot_patch_contract(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.support_token)
        client = Client.objects.create(**self.client_1_data)
        contract = Contract.objects.create(**self.contract_1_data, client=client)
        response = self.client.patch(f"/contracts/{contract.pk}/", data={"amount": 100000})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    