from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from users.models import User
from users.permissions import IsOwner, IsStaff
from users.serializers import UserSerializer, OwnerSerializer


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsStaff]


class UserCreateAPIView(generics.CreateAPIView):
    authentication_classes = ()
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        new_user = serializer.save()
        password = serializer.data["password"]
        new_user.set_password(password)
        new_user.save()


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = OwnerSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsAdminUser | IsStaff]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.user == self.get_object():
            return OwnerSerializer
        return UserSerializer
    permission_classes = [IsAuthenticated]


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsAdminUser]
