"""View module for handling requests about users"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.core.exceptions import ValidationError
from rareapi.models import RareUser, Post
from rareapi.models.subscription import Subscription

class UserView(ViewSet):
    """Rare users view"""
    
    def retrieve(self, request, pk):
        """Handle Get requests to get a single user
        
        Returns:
            Response -- JSON serialized post
        """
        
        try:
            user = RareUser.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except RareUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request):
        """Handle GET requests to get all users
        
        Returns:
            Response -- JSON serialized list of users
        """
        
        users = RareUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
     
class UserSerializer(serializers.ModelSerializer):
    """JSON serialize for users
    """
    class Meta:
        model = RareUser
        fields = ['id', 'user', 'bio', 'profile_image_url']
        depth = 3