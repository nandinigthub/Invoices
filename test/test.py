import pytest
import json
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from invoice.models import Invoice, InvoiceDetail
from invoice.serializers import InvoiceSerializer


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def data():
    return {
       
        "date": "2022-01-31",
        "customer_name": "John Doe",
        "invoice_details": [
            {
                
                "description": "Product A",
                "quantity": 3,
                "unit_price": 10.99,
                "price": 32.97
            }
           
        ]
    }


@pytest.mark.django_db
def test_create(api_client, data):
    url = '/invoices/'
    response = api_client.post(url, data=json.dumps(data), content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Invoice.objects.count() == 1

    created_invoice = Invoice.objects.first()
    assert created_invoice.date.isoformat() == data['date']
    assert created_invoice.customer_name == data['customer_name']


@pytest.mark.django_db
def test_retrieve(api_client, data):
    url = '/invoices/'
    response = api_client.post(url, data=json.dumps(data), content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Invoice.objects.count() == 1

    created_invoice = Invoice.objects.first()
    assert created_invoice.date.isoformat() == data['date']
    assert created_invoice.customer_name == data['customer_name']
    url = f'/invoices/{created_invoice.id}/'
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data['date'] == data['date']
    assert response.data['customer_name'] == data['customer_name']
    assert len(response.data['invoice_details']) == 1

    retrieved_detail = response.data['invoice_details'][0]
    assert retrieved_detail['description'] == data['invoice_details'][0]['description']
    assert retrieved_detail['quantity'] == data['invoice_details'][0]['quantity']
    


@pytest.mark.django_db
def test_update(api_client, data):
    url = '/invoices/'
    response = api_client.post(url, data=json.dumps(data), content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Invoice.objects.count() == 1

    created_invoice = Invoice.objects.first()
    assert created_invoice.date.isoformat() == data['date']
    assert created_invoice.customer_name == data['customer_name']
    updated_data = {
        "date": "2023-02-28",
        "customer_name": "Updated Name",
        "invoice_details": [
            {
                "description": "Updated Product",
                "quantity": 5,
                "unit_price": 12.99,
                "price": 64.95
            }
        ]
    }
    url = f'/invoices/{created_invoice.id}/'
    response = api_client.put(url, data=json.dumps(updated_data), content_type='application/json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['date'] == updated_data['date']
    assert response.data['customer_name'] == updated_data['customer_name']
    assert len(response.data['invoice_details']) == 1

    updated_detail = response.data['invoice_details'][0]
    assert updated_detail['description'] == updated_data['invoice_details'][0]['description']
    assert updated_detail['quantity'] == updated_data['invoice_details'][0]['quantity']
    


@pytest.mark.django_db
def test_delete(api_client, data):
    url = '/invoices/'
    response = api_client.post(url, data=json.dumps(data), content_type='application/json')
    #import pdb ; pdb.set_trace()
    assert response.status_code == status.HTTP_201_CREATED
    assert Invoice.objects.count() == 1

    created_invoice = Invoice.objects.first()
    assert created_invoice.date.isoformat() == data['date']
    assert created_invoice.customer_name == data['customer_name']
    url = f'/invoices/{created_invoice.id}/'
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Invoice.objects.count() == 0
    assert InvoiceDetail.objects.count() == 0    