# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .forms import signinForm, commentForm, profile_picForm
from django.db import connection
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from datetime import *

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
def profile_pic(request):

    user = request.user
    success = {'success': 1}

    if request.method == 'POST':
        form = profile_picForm(request.POST, request.FILES)

        if form.is_valid():
            myfile = request.FILES['photo']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)

            with connection.cursor() as cursor:

                cursor.execute('''UPDATE auth_user
                set profile_pic = %s where username = %s;''', [uploaded_file_url, user])
                row = cursor.fetchall()

            return render(request, 'profile_pic.html', success)
    else:
        form = profile_picForm()
    return render(request, 'profile_pic.html', {'form': form})



@login_required
def profile(request):
    user = request.user
    template = 'profile.html'
    with connection.cursor() as cursor:



        cursor.execute("SELECT profile_pic FROM auth_user WHERE username = %s", [user])
        profile_pic = dictfetchall(cursor)[0]

        profile_pic['upload_url'] = '/accounts/profile_pic'

        cursor.execute("SELECT p_id, p_name, product_pic_link, p_quantity FROM Product WHERE sellerid = %s", [user])
        row = dictfetchall(cursor)

        cursor.execute('''SELECT o_id, productid, product_pic_link, o_quantity, buyerid, o_date, trade_result
                    FROM OrderRecord, Product WHERE productseller = %s and p_id = productid''', [user])
        sell_record = dictfetchall(cursor)

        cursor.execute('''SELECT p_id, p_name, productseller, product_pic_link, o_id, productid, o_quantity, buyerid, o_date, trade_result
                    FROM OrderRecord, Product WHERE buyerid = %s and p_id = productid''', [user])
        order_record = dictfetchall(cursor)

        for prod in row:
            prod['update_url'] = '/products/update/%s'%prod['p_id']

        for record in sell_record:
            url = '/products/conformation/%s'%record['o_id']
            pid = record['productid']
            cursor.execute("SELECT p_name, p_quantity FROM Product WHERE p_id = %s", [pid])
            product = dictfetchall(cursor)
            pname = product[0]['p_name']
            quantity = int(product[0]['p_quantity'])
            record['result'] = record['trade_result']
            record['p_name'] = pname
            record['date_ago'] = (datetime.now().date() - record['o_date']).days
            record['url'] = url
            # if quantity < 1:
            #     sell_record.remove(record)

        for record in order_record:

            record['comment_url'] = '/accounts/comments/%s_pid_%s'%(record['productseller'], record['p_id'])
            if record['trade_result'] == 1:
                record['trade_result'] = 'Succeed!'
            elif record['trade_result'] == 2:
                record['trade_result'] = 'Declined by Seller'
            else:
                record['trade_result'] = 'Still pending'

        cursor.execute("SET sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY','')); ")
        cursor.execute("SELECT F.f_id, p_id, p_name, F.f_date, F.f_content, F.FeedbackUser, score FROM("
                       "SELECT p_id, p_name, Feedback.f_id, Feedback.f_date, Feedback.FeedbackUser, Feedback.f_content, AVG(Rating.r_score) AS score FROM Feedback, auth_user, Product, Rating "
                       "WHERE Feedback.f_id = Rating.Feedback_id "
                       "AND seller = %s "
                       "GROUP BY Feedback.f_id "
                       "ORDER BY score DESC) AS F ",
                       [user])
        comment_list = dictfetchall(cursor)
        print comment_list
        cursor.execute("SELECT FeedbackUser, f_content, f_date, f_id, p_name, p_id "
                       "FROM Feedback, Product "
                       "WHERE Seller = %s "
                       "AND Feedback.Product = Product.p_id",
                       [user])
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
            comment['date_ago'] = (datetime.now().date() - comment['f_date']).days

    context = {'product_list': row,
               'comment_list': comment_list,
               'sell_record': sell_record,
               'order_record': order_record,
               'profile_pic' : profile_pic}
    return render(request, template, context)

@login_required
def comment(request, pk):
    user = request.user
    comment_on = pk.split('_pid_')[0]
    product_id = pk.split('_pid_')[1]
    template = 'comment.html'
    context = {}
    with connection.cursor() as cursor:
        cursor.execute('''SELECT f_id FROM Feedback where Seller = %s and Product = %s and FeedbackUser = %s;''', [comment_on, product_id, user])
        row = cursor.fetchall()
    if row != ():
        context['duplicate_comments'] = 1

    if request.method == 'POST':
        form = commentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data.get('comments')
            now = datetime.now().replace(microsecond=0)
            with connection.cursor() as cursor:
                cursor.execute('''SELECT f_id FROM Feedback ORDER BY f_id DESC LIMIT 1;''')

                row = cursor.fetchall()
                if row == ():
                    cursor.execute(
                    '''INSERT INTO Feedback
                    values (%s, %s, %s, %s, %s, %s, %s);  ''',
                    [0, user, product_id, comment_on, comment, 0, now]
                    )
                else:
                    fid = int(row[0][0]) + 1
                    cursor.execute(
                    '''INSERT INTO Feedback
                    values (%s, %s, %s, %s, %s, %s, %s);  ''',
                    [fid, user, product_id, comment_on, comment, 0, now]
                    )

            return redirect('home')
    else:
        form = commentForm()
    context['form'] = form
    return render(request, template, context)


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
