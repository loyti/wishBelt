from django.shortcuts import render, redirect, HttpResponse
from .models import User, Item
from django.contrib import messages
import bcrypt

from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse


# Create your views here.
def index(request):
    #---------------------------------------------
    #------     show user home page         ------
    #---------------------------------------------
    return render(request, 'main/index.html')

def login(request):
    #---------------------------------------------
    #--- if existing user provide login access ---
    #------ and send to user dashboard      ------
    #---------------------------------------------
    if 'user_id' in request.session:
        return redirect('/')
    return render(request, 'main/dashboard.html')

def create_user(request):
    #---------------------------------------------
    #------------- make a new user ---------------
    #---------------------------------------------
    if request.method == 'POST':

        # validate all form data
        errors = User.objects.user_validator(request.POST)

        # populate messages with errors or specifics if true
        if len(errors):
            for error in errors:
                messages.error(request, error)
            return redirect('/')
        else:
        # if errors FREE
            try:
                # does email already exist in database
                check_email = User.objects.get(email = request.POST['email'])
                messages.error(request, 'Please try another email input.')
                return redirect('/')
            except:
                # hash password
                hash_it = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

                # insert user into database
                user = User(user_name=request.POST['user_name'], alias=request.POST['alias'],email=request.POST['email'],password=hash_it)
                user.save()
                messages.success(request, 'You have successfully registered')
    return redirect('/')


def itemsList(request):
    if 'user_id' not in request.session:
        messages.error(request, 'You are not logged in.')
        return redirect('/')

    users = User.objects.all()
    current_user = User.objects.get(id=request.session['user_id'])
    user = User.objects.get(id=request.session['user_id'])

    wishItems = user.user_items.all()

    items = Item.objects.exclude(id__in=wishItems).order_by('-created_at')

    context = {
        'current_user_id' : request.session['user_id'],
        'user' : user,
        'wishItems' : wishItems,
        'items': items,
    }

    return render (request, 'main/dashboard.html', context)

def itemInfo(request, item_id):
    if 'user_id' not in request.session:
        messages.error(request, 'You are not logged in.')
        return redirect('/')

    Items = Item.objects.all()

    users = User.objects.all()
    current_user = User.objects.get(id=request.session['user_id'])
    user = User.objects.get(id=request.session['user_id'])

    wishItems = user.user_items.all()

    items = Item.objects.exclude(id__in=wishItems).order_by('-created_at')

    wishItems = user.user_items.all()

    items = Item.objects.exclude(id__in=wishItems).order_by('-created_at')

    context = {
        'user' : user,
        'wishItems' : wishItems,
        'items': items,
    }

    return render(request, 'main/items.html', context)


def logout(request):
    request.session.clear()
    return redirect('/')

def signin(request):
    if request.method == 'POST':
        try:
            get_email = User.objects.get(email = request.POST['email'])
            if bcrypt.checkpw(request.POST['password'].encode(), get_email.password.encode()):
                request.session['user_id'] = get_email.id

                current_user = User.objects.get(id=request.session['user_id'])

                return redirect('/dashboard')

        except:
            messages.error(request, 'Your information is incorrect. Please try again.')
    return redirect('/signin')

def new_item(request):
    if request.method == 'POST':
        errors = Item.objects.item_validator(request.POST)

        # populate messages with errors if true
        if len(errors):
            for error in errors:
                messages.error(request, error)
            return redirect('/create')

        user = User.objects.get(id=request.session['user_id'])
        item = Item(content=request.POST['content'],user=user)
        item.save()
        messages.success(request,'Successfully posted your item.')

    return redirect('/dashboard')

def create(request):
    if 'user_id' not in request.session:
        messages.error(request, 'You are not logged in.')
        return redirect('/')

    return render(request, 'main/create.html')


def addWish(request, item_id):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['user_id'])
        item = Item.objects.get(id=item_id)
        item.wishItems.add(user)
        item.save()
    return redirect('/dashboard')

def unWish(request, item_id):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['user_id'])
        item = Item.objects.get(id=item_id)
        user.user_items.remove(item)
    return redirect('/dashboard')

def delete(request, item_id):
    item = Item.objects.get(id=item_id)
    item.delete()
    return redirect('/dashboard')
