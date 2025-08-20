
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserRegistrationSerializer
	permission_classes = [AllowAny]

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		token, created = Token.objects.get_or_create(user=user)
		return Response({
			'user_id': user.id,
			'username': user.username,
			'token': token.key
		}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
	permission_classes = [AllowAny]

	def post(self, request):
		serializer = UserLoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = authenticate(
			username=serializer.validated_data['username'],
			password=serializer.validated_data['password']
		)
		if user:
			token, created = Token.objects.get_or_create(user=user)
			return Response({'token': token.key}, status=status.HTTP_200_OK)
		return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(generics.RetrieveUpdateAPIView):
	queryset = User.objects.all()
	serializer_class = UserProfileSerializer
	permission_classes = [IsAuthenticated]

	def get_object(self):
		return self.request.user
