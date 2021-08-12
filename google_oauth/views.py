import random

from django.contrib.auth import get_user_model
from django.utils import timezone

from google.auth.transport import requests
from google.oauth2 import id_token

from rest_framework import status, renderers, parsers
from rest_framework.response import Response
from rest_framework.views import APIView


class CheckGoogle(APIView):
    # TODO change name and destination
    renderer_classes = (renderers.TemplateHTMLRenderer,)

    def get(self, request):
        return Response(template_name='login_google.html')


class GoogleOAuthAPIView(APIView):
    """
    Api view for google authentication
    """

    parser_classes = (parsers.JSONParser,)

    def post(self, request) -> Response:
        try:
            id_info = id_token.verify_oauth2_token(
                id_token=request.data.get('id_token'),
                request=requests.Request()
            )
        except Exception:
            return Response(data={'error': 'invalid token gmail'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            user = get_user_model().objects.get_or_create(email=id_info.get('email'),
                                                          username=id_info.get('name'),
                                                          first_name=id_info.get('given_name'),
                                                          last_name=id_info.get('family_name'),
                                                          is_active=True,
                                                          provider='gmail')
            user[0].last_login = timezone.now()
            user[0].save()
            returned_data = user[0].__dict__
            returned_data.pop('_state')
            return Response(data=returned_data, status=status.HTTP_200_OK)
        except Exception:
            user = get_user_model().objects.get_or_create(email=id_info.get('email'),
                                                          username=f'{id_info.get("name")}_{random.randint(0, 1000)}',
                                                          first_name=id_info.get('given_name'),
                                                          last_name=id_info.get('family_name'),
                                                          is_active=True,
                                                          provider='gmail')
            user[0].last_login = timezone.now()
            user[0].save()
            returned_data = user[0].__dict__
            returned_data.pop('_state')
            return Response(data=returned_data, status=status.HTTP_200_OK)
