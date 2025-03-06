from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Account
from accounts.serializers import AccountDetailSerializer, AccountSerializer
from users.permissions import IsOwner


# Create your views here.
class AccountView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user, balance=0)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        accounts = Account.objects.filter(user_id=request.user.user_id)
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AccountDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, account_number):
        account = get_object_or_404(
            Account, account_number=account_number, user_id=request.user.user_id
        )

        serializer = AccountDetailSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, account_number):
        account = get_object_or_404(
            Account, account_number=account_number, user_id=request.user.user_id
        )
        account.delete()
        return Response(
            {"msg": "Successfully deleted"}, status=status.HTTP_204_NO_CONTENT
        )


class MaskedAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        accounts = Account.objects.filter(user_id=request.user.user_id)
        serializer = AccountSerializer(accounts, many=True)

        masked_data = []
        for account in serializer.data:
            masked_data.append(
                {
                    "account_id": account["account_id"],
                    "masked_account_number": account["masked_account_number"],
                    "bank_code": account["bank_code"],
                    "account_type": account["account_type"],
                    "balance": account["balance"],
                }
            )
        return Response(masked_data, status=status.HTTP_200_OK)
