from django.contrib import admin
from .views import index

try:
    admin.site.register_view('djkeeper', index, 'djkeeper')
except AttributeError as ae:
    # adminplus is probably not installed.
    pass
