# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .forms import signinForm
from django.db import connection
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

import datetime

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = signinForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('home')
    else:
        form = signinForm()
    return render(request, 'signin.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    if request.method == 'POST':
        rate = request.POST.get("rate", "")
        feedback_user = request.POST.get("feedback_user", "")
        product = request.POST.get("product", "")
        Feedback_id = request.POST.get("Feedback_id", "")
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO Rating VALUES (1, %s, %s, %s, 'gil1', %s, %s)",
                           [rate, datetime.datetime.now().date(), feedback_user, product, Feedback_id])
    user = request.user
    template = 'profile.html'
    with connection.cursor() as cursor:
        cursor.execute("SELECT p_name FROM Product WHERE sellerid = %s", [user])
        row = cursor.fetchall()
        cursor.execute("SELECT FeedbackUser, f_content, f_date, Product, f_id, p_name "
                       "FROM Feedback, Product "
                       "WHERE Seller = %s "
                       "AND Feedback.Product = Product.p_id",
                       [user])
        comment_list = dictfetchall(cursor)
        for comment in comment_list:
            comment['date_ago'] = (datetime.datetime.now().date() - comment['f_date']).days
    context = {'product_list': row,
               'comment_list': comment_list}
    return render(request, template, context)


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
