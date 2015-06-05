from django.shortcuts import render
import requests
import json
# Create your views here.
from django.http import HttpResponse
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from auth_user.models import MyUser, RegisterForm, FbAccount
from auth_user.serializers import MyUserSerializer, SignUpSerializer, CheckTokenSerializer, FBTokenSerializer
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLogin
from django.conf import settings
from rest_auth.serializers import TokenSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


def default(self):
    return HttpResponse("Hello world!")


def get_fb_app_access_token(cid, secret):
    req = requests.get('https://graph.facebook.com/v2.3/oauth/access_token?',
                       params={
                           'client_id':cid,
                           'client_secret':secret,
                           'grant_type':'client_credentials'
                       })
    json_resp = req.json()
    return json_resp['access_token']


def get_user_facebook_token(token):
        req = requests.get('https://graph.facebook.com/v2.2/debug_token?',
                           params={
                               'input_token': token,
                               'access_token': get_fb_app_access_token(settings.SOCIAL_AUTH_FACEBOOK_KEY,
                                                                       settings.SOCIAL_AUTH_FACEBOOK_SECRET
                                                                      )})
        json_resp = req.json()
        return json_resp

def get_fb_user_id(token):
    return get_user_facebook_token(token).get('data').get('user_id')

def check_if_fb_user_exists(token):
    fb_data = get_user_facebook_token(token)
    dt = fb_data.get('data')
    fb_uid = dt.get('user_id')
    if MyUser.objects.filter(fb_uid = fb_uid):
        return True
    else:
        return False


def set_fb_user_id(user_id, token):
    user = MyUser.objects.get(id=user_id)
    if check_if_fb_user_exists(token):
        return JsonResponse({
            'error':True,
            'message':'Facebook user is registered',
            'data':user
        })
    else:
        user.fb_uid = get_fb_user_id(token)
        user.save()
        return True





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

    parser_classes = (JSONParser, FormParser, MultiPartParser,)

    def get(self, request, format=None):
        return Response('GET Method Not Allowed. Only POST method allowed.')

    def post(self, request, format=None):
        facebook_token = request.data.pop('facebook_token')
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            if facebook_token is not None:
                set_fb_user_id(serializer.data['id'], facebook_token)
                return Response({
                    'error': False,
                    'message': 'success',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class FacebookLogin(APIView):

    serializer_class = FBTokenSerializer
    parser_classes = (JSONParser, FormParser, MultiPartParser,)
    response_serializer = TokenSerializer


    def fb_login(self):
        self.fb_uid = get_fb_user_id(self.serializer.data['facebook_token'])
        try:
            self.user = MyUser.objects.get(fb_uid = self.fb_uid)
            self.token_object = Token.objects.get(user_id = self.user.id)
        except MyUser.DoesNotExist:
            return self.get_response_error()



    def get_response(self):
        if MyUser.DoesNotExist:
            return self.get_response_error()
        else:
            return Response(self.response_serializer(self.token_object).data,
                            status=status.HTTP_200_OK)

    def get_response_error(self):
        return Response({'error':True,
                         'message':'Facebook user NOT registered',
                         'data':self.serializer.validated_data['facebook_token']},
                        status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        return Response('GET Method Not Allowed. Only POST method allowed.')

    def post(self, request, *args, **kwargs):
        self.serializer = self.serializer_class(data=self.request.data)
        if self.serializer.is_valid() is False and check_if_fb_user_exists(self.serializer.data['facebook_token'] is False):
            self.get_response_error()
        else:
            self.fb_login()
            return self.get_response()

'''
    def post(self, request, format=None):
        access_serializer = FBAccountSerializer(data=request.data)
        if access_serializer.is_valid():
            fb_detail = get_user_facebook_token(access_serializer.data['facebook_token'])
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

'''

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

