import random
import facebook

from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework import status, renderers, parsers
from rest_framework.response import Response
from rest_framework.views import APIView


class CheckFacebook(APIView):
    renderer_classes = (renderers.TemplateHTMLRenderer,)

    def get(self, request):
        return Response(template_name='login_facebook.html')


class FacebookOAuthAPIView(APIView):
    """
    Api view for facebook authentication
    """

    parser_classes = (parsers.JSONParser,)

    def post(self, request) -> Response:
        try:
            graph = facebook.GraphAPI(access_token=request.data['authResponse'].get('accessToken'))
            profile = graph.request('/me?fields=name,email')
        except Exception:
            return Response(data={'error': 'invalid token facebook'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            user = get_user_model().objects.get_or_create(email=profile.get('email'),
                                                          username=profile.get('name'),
                                                          first_name=profile.get('name').split(' ')[0],
                                                          last_name=profile.get('name').split(' ')[-1],
                                                          is_active=True,
                                                          provider='facebook')
            user[0].last_login = timezone.now()
            user[0].save()
            returned_data = user[0].__dict__
            returned_data.pop('_state')
            return Response(data=returned_data, status=status.HTTP_200_OK)
        except Exception as e:
            # TODO add checking for unique username(randint)
            user = get_user_model().objects.get_or_create(email=profile.get('email'),
                                                          username=f'{profile.get("name")}_{random.randint(0, 1000)}',
                                                          first_name=profile.get('name').split(' ')[0],
                                                          last_name=profile.get('name').split(' ')[-1],
                                                          is_active=True,
                                                          provider='facebook')
            user[0].last_login = timezone.now()
            user[0].save()
            returned_data = user[0].__dict__
            returned_data.pop('_state')
            return Response(data=123, status=status.HTTP_200_OK)
