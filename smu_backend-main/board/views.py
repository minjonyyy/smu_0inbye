from rest_framework import generics
from .serializers import PostSerializer, PostImageSerializer, PostImageSerializer2
from .models import Post, PostImage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UpdateLatestPostView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            latest_post = Post.objects.filter(
                title='', content='', price='', region='', address='', size='', direction='', availability='', floor='', apart=''
            ).latest('created')
            
            return Response({"postId": latest_post.id}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({"error": "해당 항목을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
class PostImageCreateView(generics.CreateAPIView):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer2

    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        if post_id is None:
            raise ValueError("post_id is required")
        
        # post를 설정하여 저장
        serializer.save(post_id=post_id)