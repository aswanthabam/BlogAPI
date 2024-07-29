from rest_framework import serializers
from .models import User, Post
from datetime import datetime

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(required=True)

class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user
    
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        ]



class PostSerailzer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    slug = serializers.CharField(read_only=True)
    posted_on = serializers.DateTimeField(read_only=True)
    edited_on = serializers.DateTimeField(read_only=True)
    author = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user_id.first_name + " " + obj.user_id.last_name
    def get_author(self, obj):
        return obj.user_id.username
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'user',
            'slug',
            'author',
            'posted_on',
            'edited_on'
        ]

class PostCreateSerailzer(serializers.ModelSerializer):
    title = serializers.CharField()
    content = serializers.CharField()
    user_id = serializers.CharField()
    slug = serializers.CharField(read_only=True)

    def create(self, validated_data):
        slug = validated_data['title'].lower().replace(' ','-')
        user = User.objects.filter(id=validated_data['user_id'])[0]
        counter = 0
        count = Post.objects.filter(slug=slug).count()
        slug_ = slug
        while count > 0:
            counter += 1
            slug_ = f"{slug}-{counter}"
            count = Post.objects.filter(slug=slug_).count()
        validated_data['slug'] = slug_
        validated_data['user_id'] = user
        post = Post.objects.create(**validated_data)
        return post
    
    class Meta:
        model = Post
        fields = [
            'user_id',
            'title',
            'content',
            'slug'
        ]

class PostEditSerailzer(serializers.ModelSerializer):
    title = serializers.CharField()
    content = serializers.CharField()

    def update(self, instance, validated_data):
        validated_data['edited_on'] = datetime.now()
        return super().update(instance, validated_data)
    
    class Meta:
        model = Post
        fields = [
            'title',
            'content'
        ]
