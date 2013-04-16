# Create your views here.
from django.views.generic.base import View
from django.http import HttpResponse
from django.utils import simplejson as json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User



class UserStatus (View):
    '''
     If the user clicks on one of the accounts, ac.js sends an HTTP POST request
     to this view.
     URL query parameters:
         "email"
         "displayName"
         "photoUrl"
         "providerId"
     return: JSON representing the status od user:
         {"registered":true} means the user is registered, redirect to login
         {"registered":false} means the user is not registered, redirect to signup
         {"authUri":"IP-uri"} means that user relys on an Identity Provider
         and the user should be redirected to the provided IP-uri which
         will start the appropriate federation protocol with that IDP.
         In this case ac.js will dispatch to that URI,
         and the subsequent login path depends on how that provider works.
    '''
    
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        if request.method == "POST" :
            user =User.objects.filter(username = request.POST['displayName']) or User.objects.filter(email= request.POST['email'])
            # if len(user.filter(profile__pi_url != null)) != 0:
            #     response_data = {"ip_uri" : user.profile.ip_uri}
            if user:
                response_data = {"register": True}
            else:
                response_data = {"register": False}
        else:
            response_data = {"register": False}
        return HttpResponse(json.dumps(response_data),
                            mimetype="application/json")
