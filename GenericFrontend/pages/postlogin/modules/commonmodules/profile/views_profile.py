"""Module to verify API for login of verified user with session details."""
import logging
import re
import requests
from rest_framework.views import APIView, Response
from django.shortcuts import render, get_object_or_404, redirect
from genericfrontend.settings import *

from utilities.apicallers.apicallers import makebackendapicall_json
# from .validations_preloginhome import validation_login

# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


class PostLoginProfileAPI(APIView):
    """This covers the API for login of verified user with session details."""
    def get(self, request):
        try:
            # Handling case when user is not logged in but has directly hit the particular url
            if 'login_flag' not in request.session or request.session['login_flag'] != 1:
                request.session['redirection_url'] = "user/profile/"
                return redirect('/prelogin/')
            backend_call_params = dict(zip(['api_type', 'api_name', 'request_type', 'api_params'],
                                           ['postlogin', 'fetch_my_profile', 'post', dict()]))
            backend_call_params['api_params']['profile_id'] = request.session["profile_id"]
            backend_call_output = makebackendapicall_json(request, backend_call_params)
            output_json = dict(
                zip(["Status", "Message", "active_item", "Payload"], ["Success", "Backend API called successfully", "user/profile", backend_call_output]))
            return render(request, 'user-profile.html', output_json)
        except Exception as ex:
            output_json = dict(
                zip(["Status", "Message", "Url", "Payload"],
                    ["Success", f"Exception encountered: {ex}", "user/profile", None]))
            return render(request, 'user-profile.html', output_json)

