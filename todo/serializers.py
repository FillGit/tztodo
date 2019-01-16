from django.contrib.auth.models import User, Group
from rest_framework import serializers
from todo.models import Desks, LANGUAGE_CHOICES, STYLE_CHOICES, CompanyName, Profile
from rest_framework.validators import UniqueTogetherValidator


class DesksSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    company_name=serializers.SlugRelatedField(
        slug_field='name',
        queryset=CompanyName.objects.all()
     )
    class Meta:
        model = Desks
        fields = ('id','company_name','created','done','due_date','task','owner','executor')


    def create(self, validated_data):
        
        #Create and return a new `Desks` instance, given the validated data.
        
        return Desks.objects.create(**validated_data)

    def update(self, instance, validated_data):
        
        #Update and return an existing `Desks` instance, given the validated data.
        
        instance.due_date = validated_data.get('title', instance.title)
        instance.task = validated_data.get('code', instance.code)
        #instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance

"""class CompanyNameSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    company_name=serializers.SlugRelatedField(
        #many=True,
        #read_only=True,
        slug_field='name',
        queryset=CompanyName.objects.all()
     )
    class Meta:
        model = CompanyName
        fields = ('id','company_name','created','done','due_date','task','owner')


    def create(self, validated_data):
        
        #Create and return a new `Desks` instance, given the validated data.
        
        return CompanyName.objects.create(**validated_data)

    def update(self, instance, validated_data):
        
        #Update and return an existing `Desks` instance, given the validated data.
        
        instance.due_date = validated_data.get('title', instance.title)
        instance.task = validated_data.get('code', instance.code)
        #instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance"""

from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    desks = serializers.PrimaryKeyRelatedField(many=True, queryset=Desks.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'desks')

class CreateUserSerializer(serializers.ModelSerializer):

    """company1=serializers.StringRelatedField(many=True)
    company2=serializers.StringRelatedField(many=True)
    company3=serializers.StringRelatedField(many=True)
    company4=serializers.StringRelatedField(many=True)"""

    company1=serializers.SlugRelatedField(
                slug_field='name',
                queryset=CompanyName.objects.all())
    company2=serializers.SlugRelatedField(
                slug_field='name',
                queryset=CompanyName.objects.all())
    company3=serializers.SlugRelatedField(
                slug_field='name',
                queryset=CompanyName.objects.all())
    company4=serializers.SlugRelatedField(
                slug_field='name',
                queryset=CompanyName.objects.all())
    
    class Meta:
        model = User

        fields = ('username', 'email', 'password',
                  'company1', 'company2', 'company3', 'company4')

class ProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile

            fields = ('idsession', 'active_company')
    
