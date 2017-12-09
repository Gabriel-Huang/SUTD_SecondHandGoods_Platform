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
    if user:
        recommend1 = {}
        recommend = []
        TargetProduct = []  # user products
        Test = []   # all products
        with connection.cursor() as cursor:
            cursor.execute('''SELECT content FROM Search_Record where user = "%s"''' %user)
            user_products = dictfetchall(cursor)
            cursor.execute("SELECT p_id, p_name FROM Product where p_quantity > 0")
            all_product = dictfetchall(cursor)

        for i in user_products:
            TargetProduct.append(i['content'])
        for i in all_product:
            Test.append((i['p_id'],i['p_name']))

        listofsimilarity = [[] for x in xrange(len(TargetProduct))]

        productid = []

        for k in range (0,len(TargetProduct)):
        	for i in range (0, len(Test)):
        		listofsimilarity[k].append((Test[i][0],similar(Test[i][1],TargetProduct[k])))
        	b = sorted(range(len(listofsimilarity[k])), key=lambda n: listofsimilarity[k][n][1],reverse=True)[:2]
        	for j in b:
        		productid.append(listofsimilarity[k][j][0])

        # print TargetProduct
        # print Test

        pid = first_n(productid, 4)
        if len(pid) < 4:
            with connection.cursor() as cursor:
                cursor.execute('''SELECT p_id, p_name, product_pic_link, sellerid
                FROM Product where p_quantity >0 order by p_id desc limit 4''')
                recommend = dictfetchall(cursor)

        else:
            with connection.cursor() as cursor:
                for i in pid:
                    if i == 0:
                        cursor.execute('''SELECT p_id, p_name, product_pic_link, sellerid
                        FROM Product where p_id = %s;''' %i)
                        record = dictfetchall(cursor)[0]
                        recommend1 = record
                    else:
                        cursor.execute('''SELECT p_id, p_name, product_pic_link, sellerid
                        FROM Product where p_id = %s;''' %i)
                        record = dictfetchall(cursor)[0]
                        recommend.append(record)

    products = []
    with connection.cursor() as cursor:
        cursor.execute('''SELECT p_id, p_name, product_pic_link, sellerid
        FROM Product where p_quantity >0 order by p_id desc limit 5''')
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
    context = {"popular_seller": popular_seller, "products": products, 'recommend1': recommend1, 'recommend': recommend}
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
    categories = set()
    for product in product_list:
        product['detail'] = '/products/detials/%s' %product['p_id']
        categories.add(product['category'])
    categories = list(categories)

    return render(request, 'results.html', {'error_msg': error_msg,
                                            'post_list': product_list,
                                            'categories': categories})


@login_required
def user_view(request, pk):
    if request.method == 'POST':
        rate = request.POST.get("rate", "")
        rating_user = request.POST.get("rating_user", "")
        feedback_user = request.POST.get("feedback_user", "")
        product = request.POST.get("product", "")
        Feedback_id = request.POST.get("Feedback_id", "")
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Rating ORDER BY r_id DESC LIMIT 1")
            last_record = dictfetchall(cursor)
            if not last_record:
                last_id = 0
            else:
                last_id = last_record[0]["r_id"]

            cursor.execute("INSERT INTO Rating VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           [last_id + 1, rate, datetime.datetime.now().date(), rating_user, feedback_user, product, Feedback_id])
    template = 'profile_other.html'
    with connection.cursor() as cursor:
        cursor.execute("SELECT p_name, p_id, product_pic_link, p_quantity FROM Product WHERE sellerid = %s", [pk])
        products = dictfetchall(cursor)
        cursor.execute("SET sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY','')); ")
        cursor.execute("SELECT F.f_id, p_id, p_name, F.f_date, F.f_content, F.FeedbackUser, score FROM("
                        "SELECT p_id, p_name, Feedback.f_id, Feedback.f_date, Feedback.FeedbackUser, Feedback.f_content, AVG(Rating.r_score) AS score FROM Feedback, auth_user, Product, Rating "
                        "WHERE Feedback.f_id = Rating.Feedback_id "
                        "AND seller = %s "
                        "GROUP BY Feedback.f_id "
                        "ORDER BY score DESC) AS F ",
                       [pk])
        comment_list = dictfetchall(cursor)
        print comment_list
        cursor.execute("SELECT FeedbackUser, f_content, f_date, f_id, p_name, p_id "
                       "FROM Feedback, Product "
                       "WHERE Seller = %s "
                       "AND Feedback.Product = Product.p_id",
                       [pk])
        comment_list2 = dictfetchall(cursor)
        print comment_list2
        comment_ids = set()
        for comment in comment_list:
            comment_ids.add(comment['f_id'])
        for comment in comment_list2:
            if comment['f_id'] not in comment_ids:
                comment['score'] = 'None'
                comment_list += [comment]
        for comment in comment_list:
            comment['date_ago'] = (datetime.datetime.now().date() - comment['f_date']).days

        for comment in comment_list:
            cursor.execute("SELECT * FROM Rating WHERE Feedback_id = %s AND RatingUser = %s;", [int(comment['f_id']), request.user])
            rating_value = dictfetchall(cursor)
            if not rating_value:
                comment['current_rating'] = 0
            else:
                comment['current_rating'] = rating_value[0]['r_score']

        for product in products:
            product['detial'] = '/products/detials/%s' %product['p_id']
    seller = {'seller': '''this is %s's public profile page'''%pk}
    context = {'product_list': products,
               'comment_list': comment_list,
               'seller': seller}
    return render(request, template, context)

def stats(request):
    with connection.cursor() as cursor:
        cursor.execute('''SELECT * FROM Product
            Where p_id IN
            (SELECT productid FROM (
            SELECT productid, count(o_id) FROM OrderRecord
            WHERE trade_result = 0
            GROUP BY productid
            ORDER BY count(o_id) DESC
            LIMIT 5)AS COUNT);''')
        pop_product = dictfetchall(cursor)

        cursor.execute('''SELECT productseller FROM (
            SELECT count(o_id), productseller FROM OrderRecord
            GROUP BY productseller
            ORDER BY count(o_id) DESC
            LIMIT 5) AS COUNT;''')

        pop_seller = dictfetchall(cursor)
    for i in range(len(pop_product)):
        url = '/products/detials/%s'%pop_product[i]['p_id']
        pop_product[i]['url'] = url

    for user in pop_seller:
        user['get_absolute_url'] = '/homepage/user/%s'%user['productseller']

    template = 'stats.html'
    context = {}
    context['pop_product'] = pop_product
    context['pop_seller'] = pop_seller
    return render(request, template, context)


def first_n(productid, num):
    count = Counter(productid).most_common(num)
    pid = []
    if len(count)>=num:

        for i in range(num):
            pid.append(count[i][0])
    return pid

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
