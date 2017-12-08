# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.shortcuts import render
from django.db import connection
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from difflib import SequenceMatcher
from collections import Counter


# Create your views here.
def home(request):
    user = request.user

    recommend = []
    TargetProduct = []
    Test = []
    with connection.cursor() as cursor:
        cursor.execute('''SELECT p_id, productid, p_name FROM OrderRecord, Product where p_id = productid and buyerid = "%s"''' %user)
        user_products = dictfetchall(cursor)
        cursor.execute("SELECT p_id, p_name FROM Product")
        all_product = dictfetchall(cursor)

    for i in user_products:
        TargetProduct.append((i['p_id'], i['p_name']))
    for i in all_product:
        Test.append(i['p_name'])

    productid = []
    # for k in range (0,len(TargetProduct)):
    #     for i in range (0, len(Test)):
    #            listofsimilarity[k].append((Test[i][0],similar(Test[i][1],TargetProduct[k])))
	# b = sorted(range(len(listofsimilarity[k])), key=lambda i: listofsimilarity[k][i][1],reverse=True)[:2]
	# for j in b:
	# 	productid.append(listofsimilarity[k][j][0])

    # pid = first_n(productid)
    ##################tmr#####################


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
        if request.user.is_authenticated():
            cursor.execute("INSERT INTO Search_Record VALUES (%s, %s, %s)",
                           [request.user, q, '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())])
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

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def first_n(productid, num):
	count = Counter(productid)
	c = sorted(range(len(count)), key=lambda i: count[i],reverse=True)[:num]
	return c
