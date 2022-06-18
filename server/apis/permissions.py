from rest_framework.permissions import BasePermission
from .models import User
import io
from rest_framework.parsers import JSONParser

# Verify permission
class VerifyPermission(BasePermission):
    def has_permission(self, request, view):
        io_data=io.BytesIO(request.body)
        py_data=JSONParser().parse(io_data)
        if User.objects.get(email=py_data['email']).verified==True:
            return True
        return False

# Seller permission
class sellerPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.isSeller==True and request.user.verified==True:
            return True
        return False

# User permission
class userPermission(BasePermission):
    def has_permission(self, request, viewj):
        if request.user.verified==True and request.user.isUser==True:
            return True
        return False