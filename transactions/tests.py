from django.test import TestCase
from django.utils import timezone

from accounts.models import Account
from transactions.models import TransactionHistory
from users.models import User


# Create your tests here.
class TransactionHistoryModelTest(TestCase):
    # Given: User, Account, Transaction 객체 생성
    def setUp(self):
        self.user = User.objects.create(
            email="testuser@example.com",
            password="testpassword",
            nickname="testnickname",
            phone_number="01012345678",
        )

        self.account = Account.objects.create(
            user_id=self.user,
            account_number="1234567890",
            bank_code="001",
            account_type="savings",
            balance=1000000,
        )

        self.transaction = TransactionHistory.objects.create(
            account_id=self.account,
            amount=50000,
            balance_after_transaction=950000,
            transaction_description="test transaction",
            transaction_type="withdrawal",
            transaction_method="ATM",
            transaction_date=timezone.now(),
        )

    def test_transaction_creation(self):
        # When: 거래 내역 조회
        transaction = TransactionHistory.objects.get(
            transaction_description="test transaction"
        )

        # Then: 거래 내역이 올바르게 생성되었는지 확인
        self.assertEqual(transaction.account_id, self.account)
        self.assertEqual(transaction.amount, 50000)
        self.assertEqual(transaction.balance_after_transaction, 950000)
        self.assertEqual(transaction.transaction_description, "test transaction")
        self.assertEqual(transaction.transaction_type, "withdrawal")
        self.assertEqual(transaction.transaction_method, "ATM")

    def test_transaction_update(self):
        # When: 거래 내역 업데이트
        self.transaction.transaction_description = "updated transaction"
        self.transaction.save()

        # Then: 업데이트된 내용 확인
        updated_transaction = TransactionHistory.objects.get(
            transaction_id=self.transaction.transaction_id
        )
        self.assertEqual(
            updated_transaction.transaction_description, "updated transaction"
        )

    def test_transaction_delete(self):
        # When: 거래 내역 삭제
        self.transaction.delete()

        # Then: 삭제 확인
        with self.assertRaises(TransactionHistory.DoesNotExist):
            TransactionHistory.objects.get(
                transaction_id=self.transaction.transaction_id
            )

    def test_multiple_transactions(self):
        # When: 추가 거래 내역 생성
        TransactionHistory.objects.create(
            account_id=self.account,
            amount=30000,
            balance_after_transaction=920000,
            transaction_description="두 번째 출금",
            transaction_type="withdrawal",
            transaction_method="atm",
            transaction_date=timezone.now(),
        )

        # Then: 계좌에 연결된 거래 내역 수 확인
        transactions_count = TransactionHistory.objects.filter(
            account_id=self.account
        ).count()
        self.assertEqual(transactions_count, 2)

    def test_transaction_account_relationship(self):
        # When: 계좌를 통해 거래 내역 조회
        account_transactions = self.account.transactions.all()

        # then: 계좌와 연결된 거래 내역 확인
        self.assertEqual(account_transactions.count(), 1)
        self.assertEqual(account_transactions.first(), self.transaction)
