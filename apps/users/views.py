# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from . import models
from models import *
import datetime


# Create your views here.

# Display all users currently in DB
def index(request):
    # Create a list to hold all users in DB
    if not 'list' in request.session:
        request.session['list'] = []
    # Place users into list
    if User.objects.all().values():
        querySet = User.objects.all().values()
        request.session['list'] = list(querySet)
        # Convert non-serialized data in DB to simple datetime format
        for dic in request.session['list']:
            dic['created_at'] = str(dic['created_at'].strftime('%B %d, %Y'))
            dic['updated_at'] = str(dic['updated_at'].strftime('%B %d, %Y'))

    return render(request, 'users/index.html')

# Display currently selected user
def show(request, user_id):
    # Refresh session list of users
    if User.objects.all().values():
        querySet = User.objects.all().values()
        request.session['list'] = list(querySet)
        # Convert non-serialized data in DB to simple datetime format
        for dic in request.session['list']:
            dic['created_at'] = str(dic['created_at'].strftime('%B %d, %Y'))
            dic['updated_at'] = str(dic['updated_at'].strftime('%B %d, %Y'))
   
    request.session['user_id'] = user_id
    # print user_id
    # Select user from session list with user id passed through url
    for user in request.session['list']:
        if user['id'] == int(user_id):
            request.session['user'] = user

    return render(request, 'users/show.html')


# Template with a form with needed information to create a new user
def add(request):
    return render(request, 'users/add.html')

# Create/add a user from the data received from add.html
def create(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    User.objects.create(first_name=first_name,
                        last_name=last_name, email=email)
    # print User.objects.all().values()

    return redirect('/users')

# Display template with a form to edit currently selected user
def edit(request, user_id):
    request.session['user_id'] = user_id
    return render(request, 'users/edit.html')


def update(request):
    user = User.objects.get(id=request.session['user_id'])
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.email = request.POST['email']
    user.save()
    return redirect('/users/'+request.session['user_id'])
