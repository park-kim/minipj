from gc import get_objects

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response

from accounts.models import Account
from transactions.models import TransactionHistory
from transactions.serializers import TransactionListSerializer, \
    TransactionCreateSerializer
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsOwner


class Transaction(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request):
        accounts = Account.objects.filter(user_id=request.user)
        transactions = TransactionHistory.objects.filter(account_id__in=accounts)
        serializer = TransactionListSerializer(transactions, many=True)

        return Response(serializer.data, status=200)

    def post(self, request):
        account = get_object_or_404(Account, account_id=request.data.get('account_id'))
        print(account.account_id)
        amount = request.data.get('amount')
        transaction_type  =  request.data.get('transaction_type')

        if transaction_type == "WITHDRAW":
            balance_after_transaction = account.balance - amount
            if balance_after_transaction<0:
                return Response({"errors":"잔액보다 큰 금액을 출금할 수 없습니다."})
        else:
            balance_after_transaction = account.balance + amount
        new_transaction = TransactionHistory.objects.create(
            account_id=account,
            amount=amount,
            balance_after_transaction=balance_after_transaction,
            transaction_description= request.data.get('transaction_description'),
            transaction_method=request.data.get('transaction_method'),
            transaction_type=transaction_type)
        serializer = TransactionCreateSerializer(new_transaction, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, status=200)
        return Response(serializer.errors, status=400)

    def put(self,request):
        pass

    def patch(self, request):
        pass

    def delete(self,request, pk=None):
        transaction = get_object_or_404(TransactionHistory, pk=pk)
        transaction.delete()
        return Response({"msg": "삭제 성공"}, status=200)
