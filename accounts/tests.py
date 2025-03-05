from django.test import TestCase

from accounts.models import Account
from users.models import User


# Create your tests here.
class AccountsTestCase(TestCase):
    def setUp(self):
        # Given: User와 Account 객체 생성
        self.user = User.objects.create(
            email="testuser@example.com",
            password="testpassword",
            username="testnickname",
            phone_number="01012345678",
        )

        self.account = Account.objects.create(
            user_id=self.user,
            account_number="1234567890",
            bank_code="001",
            account_type="savings",
            balance=1000000,
        )

    def test_account_creation(self):
        # When: Account 객체를 조회
        account = Account.objects.get(account_number="1234567890")

        # Then: Account 객체가 올바르게 생성되었는지 확인
        self.assertEqual(account.user_id, self.user)
        self.assertEqual(account.bank_code, "001")
        self.assertEqual(account.account_type, "savings")
        self.assertEqual(account.balance, 1000000)

    def test_account_delete(self):
        # When: Account 객체 삭제
        self.account.delete()

        # Then: 데이터베이스에서 해당 객체가 삭제되었는지 확인
        with self.assertRaises(Account.DoesNotExist):
            Account.objects.get(account_number="1234567890")

    def test_account_update(self):
        # When: Account 객체 업데이트 (잔액 변경)
        self.account.balance = 2000000  # 잔액 수정
        self.account.save()

        # Then: 데이터베이스에서 변경된 값 확인
        updated_account = Account.objects.get(account_number="1234567890")
        self.assertEqual(updated_account.balance, 2000000)
