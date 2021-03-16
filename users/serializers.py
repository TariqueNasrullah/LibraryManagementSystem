from rest_framework import serializers
from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True, style={'input_type': 'password'})
    avatar = serializers.ImageField(required=False, use_url=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'password', 'avatar', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = super(CustomUserSerializer, self).update(instance, validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
