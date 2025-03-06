from rest_framework import serializers

from accounts.models import Account
from transactions.models import TransactionHistory


class AccountSerializer(serializers.ModelSerializer):
    masked_account_number = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = [
            "account_id",
            "account_number",
            "masked_account_number",
            "bank_code",
            "account_type",
            "balance",
        ]
        read_only_fields = ["account_id", "balance", "masked_account_number"]
        extra_kwargs = {
            "account_number": {
                "write_only": True
            }  # 계좌번호는 쓰기만 가능하고 응답에는 포함되지 않음
        }

    def get_masked_account_number(self, obj):
        if not obj.account_number:
            return ""

        account_number = obj.account_number
        return account_number[:4] + "*" * (len(account_number) - 4)


class AccountDetailSerializer(AccountSerializer):
    transactions = serializers.SerializerMethodField()

    class Meta(AccountSerializer.Meta):
        fields = AccountSerializer.Meta.fields + ["transactions"]

    def get_transactions(self, obj):
        transactions = TransactionHistory.objects.filter(
            account_id=obj
        ).order_by("-transaction_date")
        transaction_data = []
        for transaction in transactions:
            transaction_data.append(
                {
                    "amount": transaction.amount,
                    "balance_after_transaction": transaction.balance_after_transaction,
                    "transaction_description": transaction.transaction_description,
                    "transaction_type": transaction.transaction_type,
                    "transaction_method": transaction.transaction_method,
                    "transaction_date": transaction.transaction_date,
                }
            )
        return transaction_data
