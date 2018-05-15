from django.urls import path
from django.contrib.auth.decorators import login_required
from centre import views

app_name = 'centre'

urlpatterns = [
    path('', login_required(views.home), name='centre_home'),
]