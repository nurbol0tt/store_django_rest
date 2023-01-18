from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from product.models import Product
from user.models import User, UserRating


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        super(RegisterSerializer, self).create(validated_data)
        return validated_data


class PasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ('token',)


class UserSerializer(serializers.ModelSerializer):
    middle_star = serializers.IntegerField()

    class Meta:
        model = User
        fields = ("id", "username", "email", "middle_star")


class CreateRatingUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRating
        fields = ("star", "username")

    def create(self, validated_data):
        rating = UserRating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            username=validated_data.get('username', None),
            defaults={'star': validated_data.get("star")}
        )
        return rating


class MyWishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('image', 'title', 'description')
