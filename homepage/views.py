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
        cursor.execute("SELECT p_id, p_name, product_pic_link, sellerid FROM Product order by p_id limit 5")
        products = dictfetchall(cursor)
    for i in range(len(products)):
        url = '/products/detials/%s'%products[i]['p_id']
        products[i]['url'] = url

    template = 'home.html'
    with connection.cursor() as cursor:
        cursor.execute("SELECT username FROM auth_user")
        popular_seller = dictfetchall(cursor)
    for user in popular_seller:
        user['get_absolute_url'] = reverse('user-view', args=[str(user['username'])])
    context = {"popular_seller": popular_seller, "products": products}
    return render(request, template, context)


def search(request):

    q = request.GET.get('q')
    error_msg = ''

    # error.html needed！！！
    # if not q:
    #     error_msg = 'Please type in keywords'
    #     return render(request, 'homepage/errors.html', {'error_msg': error_msg})
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Product WHERE p_name REGEXP %s OR p_description REGEXP %s", [q, q])
        product_list = dictfetchall(cursor)
    for product in product_list:
        product['detail'] = '/products/detials/%s' %product['p_id']
    return render(request, 'results.html', {'error_msg': error_msg,
                                                     'post_list': product_list})


@login_required
def user_view(request, pk):
    if request.method == 'POST':
        rate = request.POST.get("rate", "")
        feedback_user = request.POST.get("feedback_user", "")
        product = request.POST.get("product", "")
        Feedback_id = request.POST.get("Feedback_id", "")
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO Rating VALUES (1, %s, %s, %s, 'gil1', %s, %s)",
                           [rate, datetime.datetime.now().date(), feedback_user, product, Feedback_id])
    template = 'profile_other.html'
    with connection.cursor() as cursor:
        cursor.execute("SELECT p_name, p_id FROM Product WHERE sellerid = %s", [pk])
        products = dictfetchall(cursor)
        cursor.execute("SELECT FeedbackUser, f_content, f_date, Product, f_id, p_name "
                       "FROM Feedback, Product "
                       "WHERE Seller = %s "
                       "AND Feedback.Product = Product.p_id",
                       [pk])
        comment_list = dictfetchall(cursor)

        for comment in comment_list:
            comment['date_ago'] = (datetime.datetime.now().date() - comment['f_date']).days

        for product in products:
            product['detial'] = '/products/detials/%s' %product['p_id']
    seller = {'seller': '''this is %s's public profile page'''%pk}
    context = {'product_list': products,
               'comment_list': comment_list,
               'seller': seller}
    return render(request, template, context)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
