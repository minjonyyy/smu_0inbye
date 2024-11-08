# django 라이브러리
from rest_framework import generics,status,permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import Token
from django.shortcuts import render, redirect
import requests

#내가 만든 모듈
from .models import User
from .serializers import SuperUser_Serializer,User_Serializer,TokenSerializer
from .config import CLIENT_ID,REDIRECT_URI, CLIENT_SECRET

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SuperUser_Serializer

class OnlyAuthenticatedUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
		
    # JWT 인증방식 클래스 지정하기
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        # Token에서 인증된 user만 가져온다.
        user = request.user
        print(f"user 정보 : {user}")
        if not user:
            return Response({"error": "접근 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"message": "Accepted"})

class KakaoCallback(APIView):
    def post(self, request):
        print("Received data:", request.data)  # 수신 데이터 로그
        authorize_code = request.data.get('AUTHORIZE_CODE')

        if not authorize_code:
            return Response({'error': 'AUTHORIZE_CODE is required'}, status=status.HTTP_400_BAD_REQUEST)

        token_url = "https://kauth.kakao.com/oauth/token"
        KAKAO_USER_API = "https://kapi.kakao.com/v2/user/me"

        data = {
            "grant_type": "authorization_code",
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "code": authorize_code,
            "client_secret": CLIENT_SECRET,
        }

        # Access token 요청
        token_response = requests.post(token_url, data=data)

        # Token 응답 로그
        print("Token response:", token_response.json())  # 추가된 로그
        if token_response.status_code != 200:
            return Response({'error': 'Token request failed', 'details': token_response.json()}, status=status.HTTP_400_BAD_REQUEST)

        token = token_response.json()
        access_token = token.get('access_token')

        if not access_token:
            return Response({'error': 'Access token not found'}, status=status.HTTP_400_BAD_REQUEST)

        headers = {"Authorization": f"Bearer {access_token}"}
        
        # 사용자 정보 요청
        user_info_response = requests.get(KAKAO_USER_API, headers=headers)

        # 사용자 정보 응답 로그
        print("User info response:", user_info_response.json())  # 추가된 로그
        if user_info_response.status_code != 200:
            return Response({'error': 'User information request failed', 'details': user_info_response.json()}, status=status.HTTP_400_BAD_REQUEST)

        user_information = user_info_response.json()
        kakao_account = user_information.get('kakao_account')

        # 유저 정보 점검
        if not kakao_account:
            return Response({'error': 'Kakao account not found'}, status=status.HTTP_400_BAD_REQUEST)

        user_data = {
            "name": kakao_account.get("name", None),
            "email": kakao_account.get("email", None),
            "phone": kakao_account.get("phone_number", None),
            "birthyear": kakao_account.get("birthyear", None),
            "birthday": kakao_account.get("birthday", None),
            "gender": kakao_account.get("gender", None)
        }

        email = user_data.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            serializer = User_Serializer(user, data=user_data)
            if serializer.is_valid():
                token: Token = TokenSerializer.get_token(user)
                access_token = str(token.access_token)
                refresh_token = str(token)

                return Response(
                    {
                        "access": access_token,
                        "refresh": refresh_token,
                        "email": email
                    },
                    status=status.HTTP_200_OK,
                )
        else:
            serializer = User_Serializer(data=user_data)
            if serializer.is_valid():
                user = serializer.save()
                token: Token = TokenSerializer.get_token(user)
                access_token = str(token.access_token)
                refresh_token = str(token)

                return Response(
                    {
                        "access": access_token,
                        "refresh": refresh_token,
                        "email": email
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

