import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Student, Course


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def factory_course():
    def course(*args, **kwargs):
        ans = baker.make(Course, *args, **kwargs)
        return ans
    return course

@pytest.fixture
def factory_student():
    def student(*args, **kwargs):
        return  baker.make(Student, *args, **kwargs)
    return student

# @pytest.fixture
# def change_max_students(value, settings):
#     if value > settings.MAX_STUDENTS_PER_COURSE:
#         assert False
#     else:
#         assert True