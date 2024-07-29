from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from utils.response import CustomResponse
from .models import Post
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models.query import Q

"""
USER REGISTRATION
"""
class UserRegisterView(APIView):
    serializer_class = UserSerializer
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.get_success_response(message="User Registered")
        return CustomResponse.get_failure_response(message="User Registration Failed!", data=serializer.errors)
"""
USER VERIFICATION
Check if user is authenticated or not.
"""
class UserVerify(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return CustomResponse.get_failure_response("Not logged in!")
        return CustomResponse.get_success_response("Logged In", data={"username":user.username})
        
"""
Create, Edit and  Delete posts
"""
class PostView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerailzer
    def delete(self, request, slug):
        user = request.user
        post = Post.objects.filter(slug=slug, user_id=user)
        if  post is None or len(post) == 0:
            return CustomResponse.get_failure_response("Post Doesnt exists!")
        post.delete()
        return CustomResponse.get_success_response("Delete Success!")

    def patch(self, request, slug):
        user = request.user
        post = Post.objects.filter(slug=slug, user_id=user)
        if  post is None or len(post) == 0:
            return CustomResponse.get_failure_response("Post Doesnt exists!")
        serializer = PostEditSerailzer(instance=post, data=request.data, partial=True)
        if not serializer.is_valid():
            return CustomResponse.get_failure_response("Edit Failed!", data=serializer.errors)
        serializer.validated_data['edited_on'] = datetime.now()
        post.update(
            **serializer.validated_data
        )
        return CustomResponse.get_success_response("Edited!")


    def post(self, request):
        user = request.user
        data = request.data.dict()
        data['user_id'] = user.id
        serializer = PostCreateSerailzer(data=data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.get_success_response(message="Post Created!", data={'slug':serializer.data['slug']})
        return CustomResponse.get_failure_response(message="Failed to create Post!", data=serializer.errors)
"""
Get Posts
"""
class GetPostsView(APIView):
    serializer_class = GetPostsSerializer
    def get(self, request, slug=None):
        if not slug:
            posts = Post.objects.filter()
            published_on = request.query_params.get('published_on')
            author = request.query_params.get('author')
            search = request.query_params.get('search')
            if published_on:
                try:
                    published_on = datetime.strptime(published_on,'%d-%m-%Y')
                except Exception as e:
                    return CustomResponse.get_failure_response("Time format error!", data={
                        "message":"Expected DD-MM-YYYY"
                    })
                posts = posts.filter(posted_on__gt=published_on)
            if author:
                posts = posts.filter(user_id__username=str(author))
            if search:
                posts = posts.filter(Q(title__icontains=search) | Q(content__icontains=search))
            serializer = PostSerailzer(posts, many=True)
        else:
            serializer = PostSerailzer(Post.objects.filter(slug=slug), many=True)
        return CustomResponse.get_success_response(message="Posts", data=serializer.data)

"""
Token Generation
"""
class TokenView(TokenObtainPairView):pass
class TokenRefresh(TokenRefreshView):pass