from django.shortcuts import render

# Create your views here.
"""from todo.models import Desks
from todo.serializers import DesksSerializer"""
from rest_framework import generics

from rest_framework import permissions
#from todo.permissions import IsOwnerOrReadOnly

from django.contrib.auth.models import User
from todo.serializers import UserSerializer, CreateUserSerializer, DesksSerializer, ProfileSerializer 


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from todo.models import Desks, CompanyName, Profile

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from todo import myfunctions
from datetime import datetime

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
"""________________"""


@api_view(['GET', 'POST'])
@permission_classes((IsAdminUser,))
def desk_list(request):
    
    #List all code snippets, or create a new snippet.
    

    if request.method == 'GET':
        desks = Desks.objects.all()
        serializer = DesksSerializer(desks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DesksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

@api_view(['GET'])
def company_todo(request, pk):

    try:
        company = CompanyName.objects.get(name=pk)
    except CompanyName.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

   
    if request.method == 'GET':
        key_idsession_f=request.GET.get("idsession")
        
        if myfunctions.check_auth(key_idsession_f, company.name):
            desks = Desks.objects.filter(company_name=company.id)
            serializer = DesksSerializer(desks, many=True)
            return Response(serializer.data)
        else:
            return Response('You must log in to this company',
                                status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def auth_user(request, pk):

    try:
        company = CompanyName.objects.get(name=pk)
    except CompanyName.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
   
    if request.method == 'PUT':

        user_obj = User.objects.get(username=request.user)
        now = datetime.now()


        modProfile=Profile.objects.get(user=user_obj)
       
        if  Profile.objects.filter(user=user_obj, enabled_company=company.id).count()>0:
            modProfile.date_idsession=now.strftime("%Y-%m-%d")
            modProfile.idsession=myfunctions.idsession_generator()
            modProfile.active_company=pk
            modProfile.save()

            serializer = ProfileSerializer(modProfile)
            return Response(serializer.data)
        else:
             return Response('Your profile does not have access to this company',
                                status=status.HTTP_400_BAD_REQUEST)
        
   
@api_view(['GET', 'PUT'])
@permission_classes((IsAdminUser,))
def desk_detail(request):
    
    #Retrieve, update or delete a code snippet.

 
    try:
        task_f=request.GET.get("task")
        desks = Desks.objects.get(task=task_f)
    except Desks.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DesksSerializer(desks)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DesksSerializer(desks, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
@api_view(['POST'])
def create_auth(request):
    if request.method == 'POST':
 

   
        serialized = CreateUserSerializer(data=request.data)
        if serialized.is_valid():


            emails = User.objects.filter(email=serialized.data['email']).count()
            if emails < 1:

                User.objects.create_user(
                    serialized.data['username'],
                    serialized.data['email'],
                    serialized.data['password']
                    )

                 
                modProfile=Profile.objects.get(user=User.objects.get(username=serialized.data['username']))
                
                modProfile.enabled_company.add(CompanyName.objects.get(name=serialized.data['company1']))
                modProfile.enabled_company.add(CompanyName.objects.get(name=serialized.data['company2']))
                modProfile.enabled_company.add(CompanyName.objects.get(name=serialized.data['company3']))
                modProfile.enabled_company.add(CompanyName.objects.get(name=serialized.data['company4']))
         
                return Response(serialized.data, status=status.HTTP_201_CREATED)
            else:
                return Response('Such email is already registered in the system',
                                status=status.HTTP_400_BAD_REQUEST)

                
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
