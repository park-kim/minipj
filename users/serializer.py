from rest_framework import serializers

from users.models import User


class UserJoinSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields= [
            'email',
            'password',
            'password2',
            'username',
            'phone_number',
        ]
        extra_kwargs = {
            'email':{
            "required":True
        }}

    def validate(self, attrs):
        if attrs['password'] != attrs["password2"]:
            raise serializers.ValidationError("비밀번호가 서로 다릅니다.")
        return attrs

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("중복된 이메일입니다.")
        return value



    def create(self, validated_data):
        new_user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],

        )
        new_user.set_password(validated_data['password'])
        new_user.save()
        return new_user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']



