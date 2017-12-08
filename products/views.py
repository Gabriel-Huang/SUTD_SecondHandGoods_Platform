# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .forms import postForm, OrderForm, conformationForm
from django.shortcuts import render
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from datetime import datetime


def detials(request, pk):

    user = request.user
    context = {}
    detials = {}

    with connection.cursor() as cursor:
        cursor.execute('''SELECT p_id, p_name, product_pic_link, sellerid,
        p_quantity, p_description, p_date, price
        FROM Product where p_id = %s;'''%pk)
        row = cursor.fetchall()[0]

    detials['name'] = row[1]
    detials['order_url'] = '/products/order/%s'%pk
    detials['pic_link'] = row[2]
    seller = row[3]
    user_url = '/homepage/user/%s'%seller
    detials['user_url'] = user_url
    detials['seller'] = seller
    detials['quantity'] = row[4]
    detials['description'] = row[5]
    detials['date']= row[6]
    detials['price'] = row[7]

    if seller == user.username:
        context['denied'] = 1

    context['detial'] = detials

    template = 'detials.html'
    return render(request, template, context)


@login_required
def post(request):
    user = request.user
    template = 'post.html'
    success = {'success': 1}
    if request.method == 'POST':
        form = postForm(request.POST, request.FILES)
        if form.is_valid():
            productname = form.cleaned_data.get('productname')
            discription = form.cleaned_data.get('description')
            quantity = int(form.cleaned_data.get('quantity'))
            price = form.cleaned_data.get('price')
            category = form.cleaned_data.get('category') #note here should be changed in future
            myfile = request.FILES['pic']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            now = datetime.now().replace(microsecond=0)
            with connection.cursor() as cursor:
                cursor.execute('''SELECT p_id FROM Product ORDER BY p_id DESC LIMIT 1;''')
                row = cursor.fetchall()

                if row == ():
                    cursor.execute('''INSERT INTO Product (p_id, sellerid, sellername,
                    p_name, p_quantity, p_description, p_date, product_pic_link, category, price) values
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);''', (0, user, '',
                    productname, quantity, discription, now, uploaded_file_url, category, price))

                else:
                    pid = int(row[0][0]) + 1
                    cursor.execute('''INSERT INTO Product (p_id, sellerid, sellername,
                    p_name, p_quantity, p_description, p_date, product_pic_link, category, price) values
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);''', (pid, user, '',
                    productname, quantity, discription, now, uploaded_file_url, category, price))
            return render(request, 'post.html', success)

    else:
        form = postForm()
    return render(request, template, {'form': form})

@login_required
def order(request, pk):
    user = request.user
    detials = {}
    with connection.cursor() as cursor:
        cursor.execute('''SELECT p_id, p_name, product_pic_link, sellerid,
        p_quantity, p_description, p_date, price
        FROM Product where p_id = %s;'''%pk)
        row = cursor.fetchall()[0]

    pid = row[0]
    detials['name'] = row[1]
    detials['order_url'] = '/products/order/%s'%pk
    detials['pic_link'] = row[2]
    seller = row[3]
    user_url = '/homepage/user/%s'%seller
    detials['user_url'] = user_url
    detials['seller'] = seller
    detials['quantity'] = row[4]
    detials['description'] = row[5]
    detials['date']= row[6]
    detials['price'] = row[7]
    template = 'order.html'

    success = {'success': 1}
    denied = {'denied': 1}
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data.get('message')
            quantity = int(form.cleaned_data.get('quantity'))
            now = datetime.now().replace(microsecond=0)

            if quantity > int(detials['quantity']):
                return render(request, 'order.html', denied)
            else:

                with connection.cursor() as cursor:

                    cursor.execute('''SELECT o_id FROM OrderRecord ORDER BY o_id DESC LIMIT 1;''')

                    row = cursor.fetchall()
                    if row == ():
                        cursor.execute('''INSERT INTO OrderRecord (o_id, productid, productseller,
                        o_quantity, buyerid, o_date, tradeinfo, trade_result) values
                        (%s, %s, %s, %s, %s, %s, %s, %s);''', (0, pid, seller,
                        quantity, user, now, message, 0))

                    else:

                        oid = int(row[0][0]) + 1
                        cursor.execute('''INSERT INTO OrderRecord (o_id, productid, productseller,
                        o_quantity, buyerid, o_date, tradeinfo, trade_result) values
                        (%s, %s, %s, %s, %s, %s, %s, %s);''', (oid, pid, seller,
                        quantity, user, now, message, 0))

            return render(request, 'order.html', success)

    else:
        form = OrderForm()
    context = {'detial': detials, 'form': form}
    return render(request, template, context)


@login_required
def conformation(request, pk):

    detials = {}

    with connection.cursor() as cursor:

        cursor.execute('''SELECT o_id, productid, o_quantity, buyerid, tradeinfo
                    FROM OrderRecord WHERE o_id = %s''', (pk))
        sell_record = dictfetchall(cursor)[0]
        pid = sell_record['productid']

        cursor.execute('''SELECT p_id, p_name, product_pic_link, sellerid,
        p_quantity, p_description, p_date, price
        FROM Product where p_id = %s;'''%pid)
        row = cursor.fetchall()[0]

    product_id = row[0]
    detials['name'] = row[1]
    detials['pic_link'] = row[2]
    detials['quantity_left'] = row[4]
    detials['quantity_acquired'] = sell_record['o_quantity']
    buyer_url = '/homepage/user/%s'%sell_record['buyerid']
    detials['buyer_url'] = buyer_url
    detials['buyer'] = sell_record['buyerid']
    detials['tradeinfo'] = sell_record['tradeinfo']
    template = 'conformation.html'
    success = {'success': 1}

    if request.method == 'POST':
        form = conformationForm(request.POST)
        if form.is_valid():
            result = form.cleaned_data.get('Options')
            with connection.cursor() as cursor:

                cursor.execute('''UPDATE OrderRecord SET trade_result = %s where
                o_id = %s''',(result, pk))
                # if success, cut product quantity by one
                print type(int(result))
                if int(result) == 1:
                    cursor.execute('''UPDATE Product SET p_quantity = p_quantity - %s where
                    p_id = %s''',(sell_record['o_quantity'], product_id))
                    # if no stock, decline all order records
                    cursor.execute('''SELECT p_quantity
                    FROM Product where p_id = %s;'''%product_id)
                    res = dictfetchall(cursor)[0]
                    quantity_left = res['p_quantity']
                    if quantity_left == 0:
                        cursor.execute('''UPDATE OrderRecord SET trade_result = %s where
                        productid = %s and o_id <> %s''',(2, product_id, pk))

            return render(request, template, success)
    else:
        form = conformationForm()

    context = {'detial': detials, 'form': form}

    return render(request, template, context)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
