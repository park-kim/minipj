from django.test import TestCase

from users.models import User


class TestUser(TestCase):
    email = "test@asd.com"
    nickname = "testnick"
    phone_number = "123123"

    def setUp(self):
        # 객체를 생성하고 반환된 값을 new_user에 할당합니다.
        self.new_user = User.objects.create(
            email=self.email,
            nickname=self.nickname,
            phone_number=self.phone_number,
        )

    def test_exist_user(self):
        pk = 1000
        # 해당 pk로 유저가 없으면 예외 발생을 확인합니다.
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=pk)

        # 유저를 가져와서 필드 값 비교
        exist_user = User.objects.get(pk=self.new_user.pk)
        self.assertEqual(exist_user.email, self.email)
        self.assertEqual(exist_user.nickname, self.nickname)
        self.assertEqual(exist_user.phone_number, self.phone_number)

    def test_put_user(self):
        # 기존 유저를 수정하고 저장
        user = User.objects.get(pk=self.new_user.pk)
        user.email = "fixtest@asd.as"
        user.save()

        # 수정된 이메일이 반영되었는지 확인
        check = User.objects.filter(email="fixtest@asd.as").first()
        self.assertEqual(user.email, check.email)

    def test_delete_user(self):
        # 기존 유저 삭제
        user = User.objects.get(pk=self.new_user.pk)
        user.delete()

        # 삭제된 유저가 없다는 것을 확인
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=self.new_user.pk)
