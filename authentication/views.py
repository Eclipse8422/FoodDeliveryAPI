from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from .models import User
from .serializers import UserCreationSerializer

class UserCreateView(GenericAPIView):
    serializer_class = UserCreationSerializer

    def post(self,request):
        
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(    
                {"message": "User created successfully!", "user": serializer.data}, 
                status=status.HTTP_201_CREATED
                )
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)