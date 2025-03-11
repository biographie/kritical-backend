from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import CustomUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView 
from rest_framework_simplejwt.exceptions import InvalidToken

class LoginView(APIView):
    def post(self, request):
        ##Takes incoming request and validates it against the CustomUserSerializer
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            ##If the serializer is valid, it means the user is authenticated
            user = serializer.validated_data
            ##Generates a refresh token for the user    
            refresh = RefreshToken.for_user(user)
            ##Converts the refresh token to a string
            access_token = str(refresh.access_token)

            ##Creates a response object with the user's email, first name, last name, and organization name
            response = Response(
                {
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "organization_name": user.organization.name,
                },
                status=status.HTTP_200_OK,
            )
            ##Sets the access token in the response cookie
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                samesite="None",
            )

            ##Sets the refresh token in the response cookie
            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite="None",
            )
            return response
        ##If the serializer is not valid, it means the user is not authenticated
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                refresh.blacklist()
            except Exception as e:
                return Response(
                    {"error": "Error invalidating token:" + str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        response = Response(
            {"message": "Successfully logged out!"}, status=status.HTTP_200_OK
        )
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response


class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request):

        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"error": "Refresh token not provided"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            response = Response(
                {"message": "Access token token refreshed successfully"},
                status=status.HTTP_200_OK,
            )
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                samesite="None",
            )
            return response
        except InvalidToken:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED
            )
