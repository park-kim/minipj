from gc import get_objects

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response

from accounts.models import Account
from transactions.models import TransactionHistory
from transactions.serializers import (
    TransactionCreateSerializer,
    TransactionListSerializer,
)
from users.permissions import IsOwner


class Transaction(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, pk=None):
        if pk:
            transactions = get_object_or_404(TransactionHistory, pk=pk)
            serializer = TransactionListSerializer(transactions)
            return Response(serializer.data, status=200)
        else:
            accounts = Account.objects.filter(user_id=request.user)
            transactions = TransactionHistory.objects.filter(
                account_id__in=accounts
            ).select_related("account_id")
            serializer = TransactionListSerializer(transactions, many=True)

            return Response(serializer.data, status=200)

    def post(self, request):
        account = get_object_or_404(
            Account, account_id=request.data.get("account_id")
        )

        serializer = TransactionCreateSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data.get("amount")
            transaction_type = serializer.validated_data.get("transaction_type")

            if transaction_type == "WITHDRAW":
                balance_after_transaction = account.balance - amount
                if balance_after_transaction > account.balance:
                    return Response(
                        {"errors": "잔액보다 큰 금액을 출금할 수 없습니다."},
                        status=400,
                    )
            else:
                balance_after_transaction = account.balance + amount

            account.balance = balance_after_transaction
            account.save()

            serializer.save(
                balance_after_transaction=balance_after_transaction,
                account_id=account,
            )

            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def put(self, request, pk=None):
        if pk is None:
            return Response({"error": "transaction 정보가 없습니다."})
        transactions = get_object_or_404(TransactionHistory, pk=pk)
        account = transactions.account_id
        serializer = TransactionCreateSerializer(
            transactions, data=request.data
        )

        if serializer.is_valid():
            new_amount = serializer.validated_data.get("amount")
            new_type = serializer.validated_data.get("transaction_type")

            if transactions.transaction_type == "DEPOSIT":
                account.balance -= transactions.amount

            else:
                account.balance += transactions.amount

            if new_type == "DEPOSIT":
                account.balance += new_amount
            else:
                account.balance -= new_amount
                if account.balance < 0:
                    print(account.balance)
                    return Response(
                        {"err": "잔액보다 큰 금액을 출금할 수 없습니다."},
                        status=400,
                    )

            account.save()

            serializer.save(
                balance_after_transaction=account.balance, account_id=account
            )
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk=None):
        if pk is None:
            return Response(
                {"error": "transaction 정보가 없습니다."}, status=400
            )

        transactions = get_object_or_404(TransactionHistory, pk=pk)
        account = transactions.account_id
        serializer = TransactionCreateSerializer(
            transactions, data=request.data, partial=True
        )

        if serializer.is_valid():
            new_amount = serializer.validated_data.get(
                "amount", transactions.amount
            )
            new_type = serializer.validated_data.get(
                "transaction_type", transactions.transaction_type
            )

            # 기존 거래 취소
            if transactions.transaction_type == "DEPOSIT":
                account.balance -= transactions.amount
            else:
                account.balance += transactions.amount

            # 새 거래 적용
            if new_type == "DEPOSIT":
                account.balance += new_amount
            else:
                account.balance -= new_amount
                if account.balance < 0:
                    return Response(
                        {"error": "잔액보다 큰 금액을 출금할 수 없습니다."},
                        status=400,
                    )
            account.save()
            updated_transaction = serializer.save(
                balance_after_transaction=account.balance, account_id=account
            )
            return Response(
                TransactionCreateSerializer(updated_transaction).data,
                status=220,
            )
        return Response(serializer.errors, status=400)

    def delete(self, request, pk=None):
        transaction = get_object_or_404(TransactionHistory, pk=pk)
        transaction.delete()
        return Response({"msg": "삭제 성공"}, status=200)
