import pytest
from rest_framework.test import APIClient
from random import choice
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from students.models import Course


@pytest.mark.django_db
def test_create_course(api_client):
    '''  Cоздание курса  '''

    url = reverse('courses-list')
    count = Course.objects.count()
    response = api_client.post(url, data={'name': 'fizika'})
    response_2 = api_client.get(url)
    data = response_2.json()
    assert response.status_code == 201
    assert response_2.status_code == 200
    assert Course.objects.count() == count + 1
    assert data[0]['name'] == 'fizika'

################

@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_first_course(api_client, factory_course):
    '''  Получение первого курса  '''

    url = reverse('courses-detail', args='1')
    # url = reverse('courses-list')
    # assert url == '/api/v1/courses/1/'
    course = factory_course(_quantity=5)
    response = api_client.get(url)
    data = response.json()
    assert response.status_code == 200
    assert data['name'] == course[0].name
    # assert data['name'] == course[1].name
    # assert data['name'] == course[2].name
    # assert data['name'] == course[3].name
    # assert data['name'] == course[4].name



