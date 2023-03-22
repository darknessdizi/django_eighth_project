from rest_framework import serializers
from students.models import Course
from django.conf import settings


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")


    def validate(self, data):
        
        if self.context["request"].method == 'PATCH':
            if len(data['students']) <= settings.MAX_STUDENTS_PER_COURSE:
                return data
            else:
                raise serializers.ValidationError("Слишком много студентов")
        elif self.context["request"].method == 'POST':
            return data