from allauth.account.utils import user_display, user_username
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.http import HttpResponse
from allauth.account.admin import EmailAddress
from rest_framework import viewsets
from allauth.account.models import EmailAddress
from allauth.account.adapter import DefaultAccountAdapter

def email_success(request):
    res = 'Email is verified!'
    name=request.GET.get('username')
    print(EmailAddress.user.username)
   # if EmailAddress.objects.filter(user=request.user, verified=True).exists():
    #    print(request.user)
   # print(users)
   # for i in users:
   #     i.is_staff= True
   #     i.save()
    return HttpResponse('<p>%s</p>' % res)


class email_view(viewsets.ModelViewSet):
    def get_queryset(self):
            # can view public lists and lists the user created
            if self.request.user.is_authenticated:
                print('is there a verified email address?')
                print(EmailAddress.objects.filter(user=self.request.user, verified=True).exists())

            return self.request.user

