from .serializers import RegisterSerializer
from .models import CustomUser
from rest_framework import generics, status
from rest_framework.response import Response


class RegisterApiView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response(user, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)