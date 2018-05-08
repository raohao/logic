# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from common.forms import EmailPostForm


# Create your views here.
def home(request):
    return render(request, 'index.html')


def send_email(request, post_id):
    post = get_object_or_404(request.POST, id=post_id, status='new')

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
