from rest_framework import serializers
from accounts.models import Account
from transactions.models import TransactionHistory
from uuid import UUID


class TransactionListSerializer(serializers.ModelSerializer):
    account_id = serializers.UUIDField(source='account_id.account_id')

    class Meta:
        model = TransactionHistory
        fields = [
            'transaction_id',
            'account_id',
            'amount',
            'balance_after_transaction',
            'transaction_description',
            'transaction_type',
            'transaction_date',
            'transaction_method'
        ]


class TransactionCreateSerializer(serializers.ModelSerializer):
    balance_after_transaction = serializers.ReadOnlyField()
    account_id = serializers.UUIDField(source='account_id.account_id')

    class Meta:
        model = TransactionHistory
        fields = [
            'account_id',
            'amount',
            'balance_after_transaction',
            'transaction_description',
            'transaction_type',
            'transaction_method'
        ]

