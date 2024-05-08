from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializer import AuthSerializer, AuthLoginSerializer, AuthGetSerializer
from .models import Auth

class AuthCreateApi(generics.CreateAPIView):
    queryset = Auth.objects.all()
    serializer_class = AuthSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = Auth.objects.get(username=request.data['regNo'])  # Get the user instance
        refresh = RefreshToken.for_user(user) 

        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class AuthLoginApi(generics.GenericAPIView):
    serializer_class = AuthLoginSerializer
    permission_classes = [permissions.AllowAny
                        ]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(request, username=serializer.validated_data['regNo'], password=serializer.validated_data['password'])
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': AuthGetSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class AuthGetApi(generics.ListAPIView):
   queryset = Auth.objects.all ()
   serializer_class = AuthGetSerializer

class AuthUpdateApi(generics.RetrieveUpdateAPIView):
    queryset = Auth.objects.all()
    serializer_class = AuthSerializer

    def get_object(self):
        return self.request.user.auth 

class AuthDeleteApi(generics.DestroyAPIView):
    queryset = Auth.objects.all()
    serializer_class = AuthSerializer

    def get_object(self):
        return self.request.user.auth  

