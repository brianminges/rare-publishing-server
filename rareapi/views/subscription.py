"""View module for handling requests about subscriptions"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.core.exceptions import ValidationError
from rareapi.models import Subscription, RareUser 


class SubscriptionView(ViewSet):
    """Rare subscriptions view"""
    
    def list(self, request):
        """Handle GET requests to get all subscriptions
        
        Returns:
            Response -- JSON serialized list of subscriptions
        """
        
        subscriptions = Subscription.objects.all()
        
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations 
        
        Returns:
            Response -- JSON serialized subscription instance
        """
        follower = RareUser.objects.get(user=request.auth.user)
        serializer = CreateSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(follower=follower)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk):
        """Handle DELETE operations
        
        Returns:
            Response -- JSON serialized subscription instance
        """
        
        subscription = Subscription.objects.get(pk=pk)
        subscription.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
               
            
    @action(methods=['get'], detail=False)
    def subscribed(self,request):
        """Get request to return list of authors logged-in user is subscribed to """
        subs = Subscription.objects.all()
        user = RareUser.objects.get(user=request.auth.user)
        subs = subs.filter(follower=user)
        serializer = SubscriptionSerializer(subs, many=True)
        return Response(serializer.data)
            

class SubscriptionSerializer(serializers.ModelSerializer):
    """JSON serializer for subscriptions
    """
    
    class Meta:
        model = Subscription
        fields = ['id', 'follower', 'author', 'created_on', 'ended_on']
        depth = 2
        
class CreateSubscriptionSerializer(serializers.ModelSerializer):
    """JSON serializer for subscriptions
    """
    class Meta:
        model = Subscription
        fields = ['id', 'author', 'created_on', 'ended_on']