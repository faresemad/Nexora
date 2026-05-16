from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.email import ChangeEmailSerializer
from ..services.email_service import EmailService

User = get_user_model()


class ChangeEmailRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangeEmailSerializer(data=request.data)
        if serializer.is_valid():
            new_email = serializer.validated_data["new_email"]
            EmailService.send_email_change_verification(request.user, new_email)
            return Response(
                {"detail": "Verification email sent to the new address."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeEmailConfirmView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        uidb64 = request.query_params.get("uid")
        token = request.query_params.get("token")
        new_email = request.query_params.get("new_email")

        if not uidb64 or not token or not new_email:
            return Response(
                {"error": "Missing parameters."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            try:
                user.change_email(new_email)
                return Response(
                    {"detail": "Email updated successfully."}, status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST
            )
