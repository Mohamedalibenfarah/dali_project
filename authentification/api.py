from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializer import AuthSerializer, AuthLoginSerializer, AuthGetSerializer
from .models import Auth
from rest_framework.exceptions import PermissionDenied

class AuthCreateApi(generics.CreateAPIView):
    queryset = Auth.objects.all()
    serializer_class = AuthSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        auth_instance = Auth.objects.get(regNo=request.data['regNo'])
        refresh = RefreshToken.for_user(auth_instance)

        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    
class AuthLoginApi(generics.GenericAPIView):
    serializer_class = AuthLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        regNo = serializer.validated_data['regNo']
        password = serializer.validated_data['password']

        try:
            auth_instance = Auth.objects.get(regNo=regNo)
            if auth_instance.check_password(password):
                refresh = RefreshToken.for_user(auth_instance)
                return Response({
                    'user': AuthGetSerializer(auth_instance).data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Auth.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class AuthGetApi(generics.ListAPIView):
   queryset = Auth.objects.all ()
   serializer_class = AuthGetSerializer

class AuthUpdateApi(generics.UpdateAPIView):
    queryset = Auth.objects.all()
    serializer_class = AuthSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be authenticated to update your Auth information.")
        return self.request.user.auth

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance != self.request.user.auth:
            self.permission_denied(self.request, message="You can only update your own information.")
        serializer.save()

class AuthDeleteApi(generics.DestroyAPIView):
    queryset = Auth.objects.all()
    serializer_class = AuthSerializer

    def get_object(self):
        return self.request.user.auth  

