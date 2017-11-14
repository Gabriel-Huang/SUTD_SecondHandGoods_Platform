# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .forms import registerForm
from django.db import connection
# Create your views here.
def register(request):
    form = registerForm(request.POST or None)

    if form.is_valid():
        username = '"'+form.cleaned_data['username']+'"'
        password = '"'+form.cleaned_data['password']+'"'
        userid = 2
        email = '"'+form.cleaned_data['email']+'"'
        pic = '"'+'23asdf'+'"'
        with connection.cursor() as cursor:
            query_prefix = "INSERT INTO User (u_id, login_name, password, email, user_pic_link) VALUES "
            query = query_prefix+"(%s,%s,%s,%s,%s);"%(userid,username,password,email,pic)
            print (query)
            cursor.execute(query)
        print request.POST
    context = locals()
    template = 'register.html'
    return render(request, template, context)
