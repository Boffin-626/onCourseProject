# serializers.py
from rest_framework import serializers
from .models import User, Learner, LearnerProgress, Parent, School, Teacher, ConceptGrasp, USSDRequest, WhatsAppRequest

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type']

class LearnerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Learner
        fields = ['id', 'user', 'name', 'parent', 'school']

class LearnerProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearnerProgress
        fields = ['id', 'learner', 'concepts_grasped', 'concepts_not_grasped', 'period_start', 'period_end', 'created_at']

class ParentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Parent
        fields = ['id', 'user', 'name', 'phone_number', 'email']

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name', 'address']

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'name', 'school']

class ConceptGraspSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConceptGrasp
        fields = ['id', 'learner', 'subject', 'concept', 'grasped', 'created_at']

class USSDRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = USSDRequest
        fields = ['id', 'parent', 'request_type', 'created_at', 'status', 'response_message']

class WhatsAppRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhatsAppRequest
        fields = ['id', 'parent', 'request_type', 'created_at', 'status', 'response_message']
