from datetime import datetime

from django.test import TestCase

from accounts.models import Account
from analytics.models import Analysis
from users.models import User


class TestAnalysis(TestCase):

    def setUp(self):
        # 사용자 생성
        self.user = User.objects.create(
            email="testuser@example.com",
            password="testpassword",
            username="testnickname",
            phone_number="01012345678",
        )

        # 계좌 생성
        self.account = Account.objects.create(
            user_id=self.user,
            account_number="1234567890",
            bank_code="001",
            account_type="savings",
            balance=1000000,
        )

        # 분석 생성
        self.analysis = Analysis.objects.create(
            user=self.user,
            account=self.account,
            analysis_type="type1",
            start_date=datetime(2025, 1, 1),
            end_date=datetime(2025, 1, 31),
            description="Test analysis",
            result_image="http://example.com/result.jpg",
            analysis_period="monthly",
        )

    def test_create_analysis(self):
        # Analysis 객체가 성공적으로 생성되었는지 확인
        analysis = Analysis.objects.get(analysis_id=self.analysis.analysis_id)
        self.assertEqual(analysis.user, self.user)
        self.assertEqual(analysis.account, self.account)
        self.assertEqual(analysis.analysis_type, "type1")
        self.assertEqual(analysis.description, "Test analysis")
        self.assertEqual(analysis.result_image, "http://example.com/result.jpg")
        self.assertEqual(analysis.analysis_period, "monthly")

    def test_read_analysis(self):
        # Analysis 객체가 올바르게 조회되는지 확인
        analysis = Analysis.objects.get(analysis_id=self.analysis.analysis_id)
        self.assertEqual(analysis.user.email, "testuser@example.com")
        self.assertEqual(analysis.account.account_number, "1234567890")

    def test_update_analysis(self):
        # 분석 정보를 업데이트하고 저장한 후 업데이트가 반영되었는지 확인
        self.analysis.description = "Updated description"
        self.analysis.save()

        updated_analysis = Analysis.objects.get(
            analysis_id=self.analysis.analysis_id
        )
        self.assertEqual(updated_analysis.description, "Updated description")

    def test_delete_analysis(self):
        # Analysis 객체 삭제 후, 삭제된 객체가 더 이상 존재하지 않는지 확인
        self.analysis.delete()

        with self.assertRaises(Analysis.DoesNotExist):
            Analysis.objects.get(analysis_id=self.analysis.analysis_id)

    def test_analysis_str_method(self):
        # `__str__` 메소드가 제대로 동작하는지 확인
        analysis_str = str(self.analysis)
        self.assertEqual(
            analysis_str,
            f"{self.user.username} - {self.analysis.analysis_type} ({self.analysis.start_date} ~ {self.analysis.end_date})",
        )
