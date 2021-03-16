from rest_framework import serializers
from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer Class for CustomUser Model
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
        # extract password from the request data
        password = validated_data.pop('password', None)

        instance = self.Meta.model(**validated_data)

        # set Hashed password to the user
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        # extract password from the request data
        password = validated_data.pop('password', None)

        instance = super(CustomUserSerializer, self).update(instance, validated_data)

        # set Hashed password to the user
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
