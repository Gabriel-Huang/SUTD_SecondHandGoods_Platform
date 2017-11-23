# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .forms import postForm
from django.shortcuts import render
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage


# Create your views here.
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
            quantity = form.cleaned_data.get('quantity')
            myfile = request.FILES['pic']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            
            return render(request, 'post.html', {
                        'uploaded_file_url': uploaded_file_url})
            # with connection.cursor() as cursor:
            #     cursor.execute("SELECT p_name FROM Product WHERE sellerid = %s", [user])
            #     row = cursor.fetchall()
    else:
        form = postForm()
    return render(request, template, {'form': form})
