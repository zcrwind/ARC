from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'register', register),
    url(r'login', login),
    url(r'upload', upload),
    url(r'query/class=(?P<queryclass>(.*))',query),
    url(r'index', index),
    url(r'logout', logout),
    url(r'function', function),
    url(r'manage', manage),
    url(r'detail/uuid=(?P<uuid>(.*))$', detail),
    url(r'addtoorder/uuid=(?P<uuid>(.*))$', addtoorder),
    url(r'addtoshoppingcart/uuid=(?P<uuid>(.*))', addtoshoppingcart),
    url(r'delbook/uuid=(?P<uuid>(.*))',delbook),
    url(r'makesure/uuid=(?P<uuid>(.*))',makesureorder),
    url(r'delshoppingcart/uuid=(?P<uuid>(.*))',delshoppingcart),
]
