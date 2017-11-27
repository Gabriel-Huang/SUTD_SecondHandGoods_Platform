# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.shortcuts import render
from django.db import connection
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    products = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT p_id, p_name, product_pic_link FROM Product order by p_id limit 2")
        row = cursor.fetchall()
    for i in range(len(row)):
        dic = {}
        url = '/products/detials/%s'%row[i][0]
        dic['url'] = url
        dic['p_name'] = row[i][1]
        dic['pic_link'] = row[i][2]
        products.append(dic)

    template = 'home.html'
    with connection.cursor() as cursor:
        cursor.execute("SELECT username FROM auth_user")
        popular_seller = dictfetchall(cursor)
    for user in popular_seller:
        user['get_absolute_url'] = reverse('user-view', args=[str(user['username'])])
    context = {"popular_seller": popular_seller, "products": products}
    return render(request, template, context)


@login_required
def user_view(request, pk):
    template = 'profile_other.html'
    with connection.cursor() as cursor:
        cursor.execute("SELECT p_name FROM Product WHERE sellerid = %s", [pk])
        row = cursor.fetchall()
        cursor.execute("SELECT FeedbackUser, f_content, f_date, Product, f_id, p_name "
                       "FROM Feedback, Product "
                       "WHERE Seller = %s "
                       "AND Feedback.Product = Product.p_id",
                       [pk])
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
