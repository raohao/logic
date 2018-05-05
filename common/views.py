# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import FormView
from common.forms import ContactForm


# Create your views here.
class CommonView(View):
    pass


class ContactView(FormView):
    template_name = 'icons.html'
    form_class = ContactForm
    success_url = '/index/'

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)