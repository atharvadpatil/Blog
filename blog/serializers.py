from rest_framework import serializers
from blog.models import *
from django.contrib.auth.models import User

class blogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'


class registerationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs={
            'password' : {'write_only': True}
        }

    def create(self, validated_data):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password==password2:
            user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        else:
            raise serializers.ValidationError({'Password': 'Passwords must match'})
        return user

class userPropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username', 'email']