from django.shortcuts import render
import requests
import json
# Create your views here.
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from auth_user.models import MyUser, RegisterForm, FbAccount
from auth_user.serializers import MyUserSerializer, \
    SignUpSerializer, \
    CheckTokenSerializer, \
    FBAccountSerializer, \
    FBDetailSerializer, \
    FBExtraDataSerializer
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_auth.registration.serializers import SocialLoginSerializer
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLogin
from django.conf import settings


def default(self):
    return HttpResponse("Hello world!")


def get_user_facebook_token(token):
        req = requests.get('https://graph.facebook.com/v2.2/debug_token?',
                           params={
                               'input_token': token,
                               'access_token': settings.SOCIAL_AUTH_FACEBOOK_ACCESS_TOKEN})
        json_resp = req.json()
        return json_resp

'''class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def register_user(request, format=None):
    # state = "Join Us now to enjoy private messaging!"
    if request.method == 'GET':
        users = MyUser.objects.all()
        serializer = MyUserSerializer(users, many=True)
        return JSONResponse(serializer.data)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SignUpSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)'''

class check_token(APIView):
    def get(self, request, format=None):
        return Response(data=request.data)


    def post(self, request, format=None):
        serializer = CheckTokenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterUser(APIView):
    def get(self, request, format=None):
        users = MyUser.objects.all()
        serializer = MyUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'error': False,
                'message': 'success',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class FacebookLogin(APIView):

    def get(self, request, format=None):
        return Response('GET Method Not Allowed. Only POST method allowed.')

    def post(self, request, format=None):
        access_serializer = FBAccountSerializer(data=request.data)
        if access_serializer.is_valid():
            fb_detail = get_user_facebook_token(access_serializer.data['access_token'])
            dt = fb_detail.get('data')
            extra_serializer = FBExtraDataSerializer(data={'extra_data': fb_detail})
            if extra_serializer.is_valid():
                if 'error' in extra_serializer.data['extra_data']:
                    return Response({'error': True, 'message': 'token error', 'data': extra_serializer.data}, status=status.HTTP_400_BAD_REQUEST)

                else:
                    serializer = FBDetailSerializer(data={'uid': dt.get('user_id'),
                                                          'expires_at': dt.get('expires_at')
                                                          })
                    if serializer.is_valid():
                        try:
                            FbAccount.objects.get(uid=serializer.data['uid'])
                        except FbAccount.DoesNotExist:
                            return Response({'error': True, 'message': 'User is Not Registered', 'data': access_serializer.data}, status=status.HTTP_400_BAD_REQUEST)

                        return Response({'error': False, 'message': 'User is Registered.', 'data': serializer.data}, status=status.HTTP_201_CREATED)

                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(access_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class FacebookLogin2(SocialLogin):
    adapter_class = FacebookOAuth2Adapter

class user_list(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        users = MyUser.objects.all()
        serializer = MyUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MyUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class user_detail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return MyUser.objects.get(pk=pk)
        except MyUser.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        users = self.get_object(pk)
        serializer = MyUserSerializer(users)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        users = self.get_object(pk)
        serializer = MyUserSerializer(users, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        users = self.get_object(pk)
        users.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

