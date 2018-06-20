from django.shortcuts import redirect
from rest_framework_jwt.settings import api_settings


def login_success(request):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(request.user)
    token = jwt_encode_handler(payload)

    return redirect("http://cardforge.net/home.html?token={}".format(token))
