__author__ = 'kctheng'
from django.forms import widgets
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from auth_user.models import MyUser, FbAccount
from django.core.validators import RegexValidator
from rest_framework.authtoken.models import Token
import auth_user.views
import requests
from django.conf import settings

class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """
    class Meta:
        model = Token
        fields = ('key', 'created',)



class CheckTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'dob', 'gender', 'agree_toc')





class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(help_text='Required. 15 characters or fewer. Alphanumerics only.',
                                     max_length=15,
                                     validators=[RegexValidator(regex='^[a-z0-9_-]{3,16}$',
                                                                message='No Special Symbols allowed. Alphanumerics only',
                                                                code='invalid'),
                                                 UniqueValidator(queryset=MyUser.objects.all())
                                                 ]
                                     )
    password = serializers.CharField(max_length=128, style={'input_type': 'password'}, write_only=True)
    email = serializers.EmailField(label='Email address',
                                   max_length=254,
                                   required=True,
                                   validators=[UniqueValidator(queryset=MyUser.objects.all(),
                                                               message='This email has been taken.Please choose another one.')]
                                   )
    first_name = serializers.CharField(allow_blank=True, max_length=30, required=False)
    last_name = serializers.CharField(allow_blank=True, max_length=30, required=False)
    dob = serializers.DateField(required=True)
    gender = serializers.CharField(max_length=2,
                                   required=True,
                                   validators=[RegexValidator(regex='^([M|m]|[F|f])$',
                                                              message='Please input M or F only. M for Male, F for Female',
                                                              code='invalid')
                                               ]
                                   )
    auth_token = TokenSerializer(read_only=True)

    class Meta:
        model = MyUser
        fields = ('id','username', 'password', 'email', 'first_name', 'last_name', 'dob', 'gender', 'auth_token')


    def create(self, validated_data):
        user = MyUser.objects.create(**validated_data)
        Token.objects.get_or_create(user=user)
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.gender = validated_data.get('gender', instance.gender)
        token_data = validated_data.pop('auth_token')
        auth_token = instance.auth_token
        # Unless the application properly enforces that this field is
        # always set, the follow could raise a `DoesNotExist`, which
        # would need to be handled.
        instance.auth_token = validated_data.get('auth_token', instance.auth_token)
        auth_token.key = token_data.get(
            'key',
            auth_token.key
        )
        auth_token.created = token_data.get(
            'created',
            auth_token.created
        )
        instance.save()
        return instance


'''class TestSignUpSerializer(serializers.ModelSerializer):
    auth_token = TokenSerializer(read_only=True)

    class Meta:
        model = MyUser
        fields = ('id','username', 'password', 'email', 'auth_token')


    def create(self, validated_data):
        user = MyUser(email=validated_data['email'],
                      username=validated_data['username']
                     # first_name=validated_data['first_name'],
                     # last_name=validated_data['last_name'],
                     # dob=validated_data['dob']
                     # gender=validated_data['gender']
                      )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.get_or_create(user=user)
        #user = MyUser(auth_token=self.validate(auth_token))
        return user

    def validate(self, attrs):
        raise serializers.ValidationError("error")
        return attrs'''

class FBDetailSerializer(serializers.ModelSerializer):

    user = serializers.IntegerField(read_only=True)
    expires_at = serializers.FloatField()

    class Meta:
        model = FbAccount
        fields = ('id', 'user', 'uid', 'date_joined', 'expires_at')
        read_only_fields = ('id', 'date_joined')



class FBAccountSerializer(serializers.ModelSerializer):

    user = serializers.IntegerField(read_only=True)

    class Meta:
        model = FbAccount
        fields = ('id', 'user', 'access_token', 'uid', 'date_joined', 'extra_data', 'expires_at')
        read_only_fields = ('id', 'user', 'uid', 'date_joined', 'extra_data', 'expires_at')


class FBExtraDataSerializer(serializers.ModelSerializer):

    user = serializers.IntegerField(read_only=True)

    class Meta:
        model = FbAccount
        fields = ('id', 'user', 'extra_data')
        read_only_fields = ('id', 'user')


'''    def validate(self, attrs):
        access_token = attrs.get('access_token')
        json = auth_user.views.get_user_facebook_token(access_token)

        if json['data']['error']:
            raise serializers.ValidationError('There is error in the access token')

        return attrs

    def create(self, validated_data):
        access_token=validated_data.pop['access_token']
        token = FbAccount(access_token=access_token)
        token.save()
        json = get_user_facebook_token(access_token)
        extra_data = FbAccount(uid=json['data']['user_id'],
                               expires_at=json['data']['expires_at'],
                               extra_data=json['data']['app_id']
                               )
        extra_data.save()
        return token'''
