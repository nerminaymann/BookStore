from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Book,Review
from django.contrib.auth.models import User

# --------------------------------------USER------------------------------------

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect Credentials Passed.')


# --------------------------------------BOOK------------------------------------

class BookSerializer (serializers.ModelSerializer):
    # title = serializers.CharField(max_length=100)
    # author = serializers.CharField(max_length=100)
    # email = serializers.CharField(max_length=100)
    # date = serializers.DateTimeField()
    #
    # def create(self, validated_data):
    #     return Book.objects.create(validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title',instance.title)
    #     instance.author = validated_data.get('author',instance.author)
    #     instance.email = validated_data.get('email',instance.email)
    #     instance.date = validated_data.get('date',instance.date)
    #     instance.save()
    #     return instance

    class Meta:
        model = Book
        fields=('__all__')


class Search_BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'img']


# --------------------------------------REVIEWS------------------------------------

class ReviewSerializer(serializers.ModelSerializer):
    bookDetail= BookSerializer(many=True)
    class Meta:
        model = Review
        fields=('__all__')
