import pytest

from random import choice
from django.urls import reverse
from students.models import Course, Student


@pytest.mark.django_db
def test_create_course(api_client):
    '''  Cоздание курса  '''

    url = reverse('courses-list')
    count = Course.objects.count()
    response = api_client.post(url, data={'name': 'physics'})
    response_2 = api_client.get(url)
    data = response_2.json()
    assert response.status_code == 201
    assert response_2.status_code == 200
    assert Course.objects.count() == count + 1
    assert data[0]['name'] == 'physics'


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


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_list_courses(api_client, factory_course):
    '''  Получение списка курсов  '''

    count = Course.objects.count()
    url = reverse('courses-list')
    factory_course(_quantity=10)
    response = api_client.get(url)
    data = response.json()
    assert response.status_code == 200
    assert len(data) == count + 10


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_filtre_id_course(api_client, factory_course):
    '''  Фильтрация списка курсов по id  '''

    url = reverse('courses-list')
    course = factory_course(_quantity=10)
    random_course = choice(course)
    response = api_client.get(url, {'id': str(random_course.id)})
    data = response.json()
    assert response.status_code == 200
    assert data[0]['id'] == random_course.id
    assert len(data) == 1


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_filtre_name_course(api_client, factory_course):
    '''  Фильтрация списка курсов по name  '''

    url = reverse('courses-list')
    course = factory_course(_quantity=10)
    random_course = choice(course)
    response = api_client.get(url, {'name': str(random_course.name)})
    data = response.json()
    assert response.status_code == 200
    assert data[0]['name'] == random_course.name
    assert len(data) == 1


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_update_course(api_client, factory_course):
    '''  Обновление курса  '''

    course = factory_course(_quantity=1)
    id = course[0].id
    url = reverse('courses-detail', args=[id])
    response = api_client.patch(url, {'name': 'physics'})
    assert response.status_code == 200
    response_2 = api_client.get(url)
    data = response.json()
    assert response_2.status_code == 200
    assert data['id'] == id
    assert data['name'] == 'physics'


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_update_course(api_client, factory_course):
    '''  Удаление курса  '''

    course = factory_course(_quantity=5)
    random_id = choice(course).id
    delete_url = reverse('courses-detail', args=[random_id])
    response = api_client.delete(delete_url)
    assert response.status_code == 204

    all_url = reverse('courses-list')
    assert len(course) == 5
    assert len(api_client.get(all_url).json()) == 4
    response = api_client.get(delete_url)
    assert response.status_code == 404
    

@pytest.mark.parametrize(['counts', 'status'], [(0, 400), (5, 200)])
@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_max_student_per_course2(api_client, factory_course, counts, status, settings):
    '''  Ограничить число студентов на курсе  '''

    settings.MAX_STUDENTS_PER_COURSE = counts
    course = factory_course(_quantity=1)
    url = reverse('courses-detail', args=str(course[0].id))
    student = Student.objects.create(name='Ivan', birth_date='1980-01-20')  
    response = api_client.patch(url, {'students': [student.id]})
    assert response.status_code == status