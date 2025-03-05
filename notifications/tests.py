from django.test import TestCase

from notifications.models import Notification
from users.models import User


# Create your tests here.
class NotificationModelTest(TestCase):
    # Given: User와 Notification 객체 생성
    def setUp(self):
        self.user = User.objects.create(
            email="testuser@example.com",
            password="testpassword",
            username="testnickname",
            phone_number="01012345678",
        )

        self.notification = Notification.objects.create(
            user_id=self.user, message="test message"
        )

    def test_notification_creation(self):
        # When: Notification 객체 조회
        notification = Notification.objects.get(message="test message")

        # Then: Notification 객체가 올바르게 생성되었는지 확인
        self.assertEqual(notification.user_id, self.user)
        self.assertEqual(notification.message, "test message")
        self.assertFalse(notification.is_read)

    def test_notification_update(self):
        # When: Notification 객체 업데이트 (읽음 상태로 변경)
        self.notification.is_read = True
        self.notification.save()

        # Then: 업데이트된 내용 확인
        updated_notification = Notification.objects.get(
            notification_id=self.notification.notification_id
        )
        self.assertTrue(updated_notification.is_read)

    def test_notification_delete(self):
        # When: Notification 객체 삭제
        self.notification.delete()

        # Then: 삭제 확인
        with self.assertRaises(Notification.DoesNotExist):
            Notification.objects.get(
                notification_id=self.notification.notification_id
            )

    def test_multiple_notifications(self):
        # When: 추가 알림 생성
        Notification.objects.create(user_id=self.user, message="test message2")

        # Then: 사용자에 연결된 알림 수 확인
        notifications_count = Notification.objects.filter(
            user_id=self.user
        ).count()
        self.assertEqual(notifications_count, 2)

    def test_user_notification_relationship(self):
        # When: 사용자를 통해 알림 조회
        user_notifications = self.user.notifications.all()

        # Then: 사용자와 연결된 알림 확인
        self.assertEqual(user_notifications.count(), 1)
        self.assertEqual(user_notifications.first(), self.notification)
