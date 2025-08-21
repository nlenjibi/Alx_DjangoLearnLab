from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from django.contrib.auth import get_user_model

User = get_user_model()
# ...existing code...
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import CustomUser

class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(CustomUser, pk=user_id)
        request.user.following.add(user_to_follow)
        user_to_follow.followers.add(request.user)
        return Response({'detail': f'You are now following {user_to_follow.username}'}, status=status.HTTP_200_OK)

class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(CustomUser, pk=user_id)
        request.user.following.remove(user_to_unfollow)
        user_to_unfollow.followers.remove(request.user)
        return Response({'detail': f'You have unfollowed {user_to_unfollow.username}'}, status=status.HTTP_200_OK)
class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        user_to_follow = get_object_or_404(User, pk=pk)
        request.user.following.add(user_to_follow)
        user_to_follow.followers.add(request.user)
        return Response({'status': f'You are now following {user_to_follow.username}'})

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        user_to_unfollow = get_object_or_404(User, pk=pk)
        request.user.following.remove(user_to_unfollow)
        user_to_unfollow.followers.remove(request.user)
        return Response({'status': f'You have unfollowed {user_to_unfollow.username}'})
# ...existing code...

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
