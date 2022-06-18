from functools import partial
from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import io
from rest_framework.parsers import JSONParser
from .models import User,Product,Transaction
from .serializers import UserSerializer,TokenObtainPairSerializer,ProductCreationSerializer,ProductGetSerializer,TransactionSerializer
from .utils import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import VerifyPermission,sellerPermission,userPermission

# Create your views here.

class CreateUser(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

    def perform_create(self, serializer):
        obj=serializer.save()
        verifyEmail(obj.email,obj.uid)

# Verify user
@api_view(['PATCH'])
def verifyUser(request):
    try:
        io_data=io.BytesIO(request.body)
        py_data=JSONParser().parse(io_data)
        user=User.objects.get(email=py_data['email'])
        if User.objects.filter(email=py_data['email']).exists() and py_data['key']==user.uid:
            serialized_user=UserSerializer(user,data={'verified':True},partial=True)
            if serialized_user.is_valid():
                serialized_user.save()
        else:
            raise ValueError("Key didn't match!")

        return JsonResponse({'message':'User verified'},status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return JsonResponse({'error':'Something went wrong!'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Send uid
@api_view(['POST'])
@permission_classes([VerifyPermission])
def getUid(request):
    try:
        io_data=io.BytesIO(request.body)
        dict_data=JSONParser().parse(io_data)
        email=dict_data['email']
        user=User.objects.get(email=email)
        verifyEmail(email,user.uid)
        return JsonResponse({'message':'Email sent!'},status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return JsonResponse({'error':'Something went wrong!'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Reset password
@api_view(['PUT'])
@permission_classes([VerifyPermission])
def resetPassword(request):
    try:
        io_data=io.BytesIO(request.body)
        py_data=JSONParser().parse(io_data)
        user=User.objects.get(email=py_data['email'])
        if User.objects.filter(email=py_data['email']).exists() and py_data['key']==user.uid:
            serialized_user=UserSerializer(user,data={'password':py_data['password']},partial=True)
            if serialized_user.is_valid():
                serialized_user.save()
        else:
            raise ValueError("Inavlid credentials!")
        return JsonResponse({'message':'Password reset successful!'},status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return JsonResponse({'error':'Something went wrong!'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Change password
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def changePassword(request):
    try:
        io_data=io.BytesIO(request.body)
        py_data=JSONParser().parse(io_data)
        old_user=User.objects.get(email=request.user)
        new_user=UserSerializer(old_user,data={'password':py_data['password']},partial=True)
        if new_user.is_valid(raise_exception=True):
            new_user.save()
        return JsonResponse({'message':'Password has been changed!'},status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return JsonResponse({'error':'Something went wrong!'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Generate token
class EmailTokenObtainPairView(TokenObtainPairView):
    permission_classes=[VerifyPermission]
    serializer_class = TokenObtainPairSerializer

# Update user
class GetOrUpdateUser(generics.RetrieveUpdateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

# Create product
class CreateProduct(generics.CreateAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductCreationSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated,sellerPermission]

# Get all available products
class GetProducts(generics.ListAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductGetSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return super().get_queryset().filter(quantity__gt=0).order_by('-id')

# Get a product
class GetAProduct(generics.RetrieveAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductGetSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

# Buy a product
@api_view(['PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated,userPermission])
def buyProduct(request):
    try:
        io_data=io.BytesIO(request.body)
        dict_data=JSONParser().parse(io_data)
        id=dict_data['id']
        product=Product.objects.get(id=id)
        if product.quantity>0 and request.user.balance>=product.productPrice:
            updated_product=ProductGetSerializer(product,data={'quantity':product.quantity-1},partial=True)
            if updated_product.is_valid(raise_exception=True):
                updated_product.save()
            updated_user=UserSerializer(request.user,{'balance':request.user.balance-product.productPrice},partial=True)
            if updated_user.is_valid(raise_exception=True):
                updated_user.save()
            seller=User.objects.get(id=product.postedby.id)
            updated_seller=UserSerializer(seller,{'balance':product.productPrice},partial=True)
            if updated_seller.is_valid(raise_exception=True):
                updated_seller.save()
            transaction_data={'product':product.id,'amount':product.productPrice,'buyer':request.user.id}
            print(transaction_data)
            transaction_serializer=TransactionSerializer(data=transaction_data)
            if transaction_serializer.is_valid(raise_exception=True):
                transaction_serializer.save()
            return JsonResponse({'message':'Order placed!'},status=status.HTTP_200_OK)
        elif product.quantity<=0:
            return JsonResponse({'error':'Out of stock!'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'error':'User doesn\'t have enough balance'})
    except Exception as e:
        print(e)
        return JsonResponse({'error':'Something went wrong!'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)