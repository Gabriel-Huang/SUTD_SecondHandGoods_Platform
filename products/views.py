# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .forms import postForm
from django.shortcuts import render
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from datetime import datetime


def detials(request, pk):
    detials = {}
    with connection.cursor() as cursor:
        cursor.execute('''SELECT p_id, p_name, product_pic_link, sellerid,
        p_quantity, p_description, p_date, price
        FROM Product where p_id = %s;''', (pk))
        row = cursor.fetchall()[0]
    detials['name'] = row[1]
    detials['order_url'] = '/products/order/%s'%pk
    detials['pic_link'] = row[2]
    seller = row[3]
    user_url = '/accounts/profile/%s'%seller
    detials['user_url'] = user_url
    detials['seller'] = seller
    detials['quantity'] = row[4]
    detials['description'] = row[5]
    detials['date']= row[6]
    detials['price'] = row[7]
    context = {'detial': detials}

    template = 'detials.html'
    return render(request, template, context)


@login_required
def post(request):
    user = request.user
    template = 'post.html'
    pic = ''
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
                pid = int(cursor.fetchall()[0][0]) + 1
                cursor.execute('''INSERT INTO Product (p_id, sellerid, sellername,
                p_name, p_quantity, p_description, p_date, product_pic_link, category, price) values
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);''', (pid, user, '',
                productname, quantity, discription, now, uploaded_file_url, category, price))
            return render(request, 'post.html', {
                        'uploaded_file_url': uploaded_file_url})

    else:
        form = postForm()
    return render(request, template, {'form': form})
