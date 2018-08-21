import sqlite3

from sqlite3 import Error
from django.urls import re_path
from manage import *
from . import views

urlpatterns = [
    # ex: /api/GetContact/{contact_id}/
    re_path(r'^(?i)GetContact/(?P<contact_id>\d+)/$', views.get_contact, name='get_contact'),
    # ex: /api/GetFullContactList/
    re_path(r'^(?i)GetFullContactList/$', views.get_full_contact_list, name='get_full_contact_list'),
    # ex: /api/CreateContact/
    re_path(r'^(?i)CreateContact/$', views.create_contact, name='create_contact'),
    # ex: /api/EditContact/
    re_path(r'^(?i)EditContact/(?P<contact_id>\d+)/$', views.edit_contact, name='edit_contact'),
    # ex: /api/DeleteContact/
    re_path(r'^(?i)DeleteContact/$', views.delete_contact, name='delete_contact'),
]
