"""View module for handling requests about posts"""
# from cProfile import label
# from unicodedata import category
# from rareapi.models.category import Category
# from urllib.request import url2pathname
# from wsgiref.util import request_uri
# from django import urls
# from django.forms import URLField
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.core.exceptions import ValidationError
from rareapi.models import Post, RareUser, Comment, Subscription
from rareapi.views.comment import CommentSerializer
from django.db.models import Q

class PostView(ViewSet):
    """Rare posts view"""
    
    def retrieve(self, request, pk):
        """Handle GET request to get single post
        
        Returns:
            Response -- JSON serialized post
        """
        try: 
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request): 
        """Handle GET requests to get all posts
        
        Returns:
            Response -- JSON serialized list of posts
        """
        
        posts = Post.objects.all()
        category = request.query_params.get('category', None)
        if category is not None:
            posts = posts.filter(category_id=category)
        user = request.query_params.get('user', None)
        if user is not None:
            posts = posts.filter(user_id=user)
        search_title = self.request.query_params.get('q', None)
        if search_title is not None:
            posts = Post.objects.filter(
                Q(title__contains=search_title)
            )
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    @action(methods=['get'], detail=False)
    def my_posts(self, request):
        """Get request to display logged-in user's posts on /posts/my_posts page"""
        user = RareUser.objects.get(user=request.auth.user)
        posts = Post.objects.all()
        posts = posts.filter(user_id=user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    @action(methods=['get'], detail=True)
    def comments(self, request, pk):
        """Get request to display comments on each post
        """
        comments = Comment.objects.all()
        posts = Post.objects.get(pk=pk)
        comments = comments.filter(post_id=posts)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    @action(methods=['get'], detail=False)
    def my_comments(self, request):
        """Get request to display all logged-in user's comments on /posts/my_comments """
        user = RareUser.objects.get(user=request.auth.user)
        comments = Comment.objects.all()
        comments = comments.filter(author=user)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data) 
    
    @action(methods=['get'], detail=False)
    def subscribed(self, request):
        """Get request to display posts of authors logged-in user is subscribed to """
        
        user = RareUser.objects.get(user=request.auth.user)
        user_subs = Subscription.objects.filter(follower=user)
        user_subs_users = [sub.author for sub in user_subs]
        subscribed_posts = Post.objects.filter(user__in=user_subs_users)
        serializer = PostSerializer(subscribed_posts, many=True)
        return Response(serializer.data)
    
   
    def create(self, request):
        """Handle POST operations
        
        Returns:
            Response -- JSON serialized post instance
        """
        user = RareUser.objects.get(user=request.auth.user)
        serializer = CreatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a post
        
        Returns:
        Response -- Empty body with 204 status code
        """
        post = Post.objects.get(pk=pk)
        serializer = CreatePostSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def filter_by_category(self, request, pk):
        """Handle GET requests for a post's category
        
        Returns:
            Response -- JSON serialized list of posts
        """
        posts = Post.objects.all()
        category = request.query_params.get('category', None)
        if category is not None:
            posts = posts.filter(category_id=category)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)   
        
class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    """
    class Meta:
        model = Post
        fields = ['id', 'user', 'category', 'title', 'publication_date', 'image_url', 'content', 'tags', 'reactions']
        depth = 2

class CreatePostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    """
    class Meta:
        model = Post
        fields = ['id', 'category', 'title', 'publication_date', 'image_url', 'content', 'approved']