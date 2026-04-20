from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import UserSerializer, RegisterUserSerializer, ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated


class CreateUserView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
