# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import connection
from django.shortcuts import render

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
    context = {'products': products}
    template = 'home.html'
    return render(request, template, context)
