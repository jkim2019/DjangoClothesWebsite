from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import Context
from django.template.loader import get_template
from django.urls import reverse
from django.views.decorators.cache import never_cache

from .forms import Login_Form, Clothes_Form, Feedback_Form
from .models import Clothes_Item, Favorite

'''
TO FIX LIST
------------------------------------------------------------------------------------------------------------------
1. Pictures
2. Make sure all views work with an unauthorized user
3. When pictures have been added, make sure users can cycle through all pictures within thumbnail (see craigslist)
------------------------------------------------------------------------------------------------------------------
'''

'''
TO FIX FOR OBJECT SEARCH FILTERS
----------------------------------------------------------------------------
1. Add filter__type (ie. gender, size, color, etc.)
2. change get_favorite_clothes_ids method so that
it only gets favorites which are displated
----------------------------------------------------------------------------
'''


# never_cache decorator keeps main page from caching favorite values
# and misrepresenting data from the database when back button is used
# never-cache also used on profile and detail pages
@never_cache
def index(request):
    clothes = Clothes_Item.objects.all()
    filter_category = request.GET.get("filter_category")
    if filter_category:
        clothes = Clothes_Item.objects.filter(gender=filter_category)
        clothes_ids = [x.id for x in clothes]
        to_json = {'clothes_ids': clothes_ids}
        return JsonResponse(to_json)
    else:
        if request.user.is_authenticated():
            favorite_clothes_ids = get_favorite_clothes_ids(request)
            return render(request, 'index.html', {'clothes': clothes, 'favorite_clothes_ids': favorite_clothes_ids})
        return render(request, 'index.html', {'clothes': clothes})

@never_cache
def profile(request, username):
    user = request.user
    context = {}
    if user.is_authenticated():
        clothes = Clothes_Item.objects.filter(user=user)
        favorite_clothes_ids = get_favorite_clothes_ids(request)
        favorite_clothes = set()
        for id in favorite_clothes_ids:
            favorite_clothes.add(Clothes_Item.objects.get(id=id))
        form = Clothes_Form()
        male_form = Clothes_Form(initial={'gender': 'male'})
        female_form = Clothes_Form(initial={'gender': 'female'})
        unisex_form = Clothes_Form(initial={'gender': 'unisex'})
        male_form.fields['clothing_type'].choices = [('Tops', 'Tops'), ('Bottoms', 'Bottoms'), ('Shoes', 'Shoes'), ('Accessories', 'Accessories'), ('Costumes', 'Costumes'), ('Other', 'Other')]
        female_form.fields['clothing_type'].choices = [('Tops', 'Tops'), ('Bottoms', 'Bottoms'), ('Dresses', 'Dresses'), ('Shoes', 'Shoes'),('Accessories', 'Accessories'), ('Costumes', 'Costumes'), ('Other', 'Other')]
        unisex_form.fields['clothing_type'].choices = [('Tops', 'Tops'), ('Bottoms', 'Bottoms'), ('Shoes', 'Shoes'), ('Accessories', 'Accessories'), ('Costumes', 'Costumes'), ('Other', 'Other')]
        context = {'username': username, 'clothes': clothes, 'form': form, 'male_form' : male_form, "female_form" : female_form,
                   'unisex_form': unisex_form, "favorite_clothes": favorite_clothes, "favorite_clothes_ids": favorite_clothes_ids}
    return render(request, 'profile.html', context)


# detail page for an article of clothing
@never_cache
def detail(request, clothing_item_id):
    clothes_item = Clothes_Item.objects.get(id=clothing_item_id)
    favorite_clothes_ids = get_favorite_clothes_ids(request)
    return render(request, 'detail.html', {'clothes_item': clothes_item, "favorite_clothes_ids": favorite_clothes_ids})


def login_view(request):
    if request.method == 'POST':
        form = Login_Form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                # the password verified for the user
                if user.is_active:
                    print("User is valid, active and authenticated")
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    print("The password is valid, but the account has been disabled!")
            else:
                # the authentication system was unable to verify the username and password
                print("The username and password were incorrect.")
    else:
        form = Login_Form()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def post_clothes_item(request):
    # if POST request then process form data
    if request.user.is_authenticated():
        if request.method == 'POST':
            username = request.user
            form = Clothes_Form(data=request.POST, files=request.FILES)
            if form.is_valid():
                messages.success(request, 'Clothes item successfully posted!')
                clothes_item = form.save(commit=False)
                clothes_item.user = request.user
                clothes_item.save()
            return HttpResponseRedirect(reverse('profile', args=[username]))


# have feedback form send email with feedbacktext to bam4564@live.unc.edu and senpenguin@gmail.com
# FIX THIS METHOD
def feedback(request):
    feedback_form = Feedback_Form
    if request.method == 'POST':
        form = feedback_form(data=request.POST)
        if form.is_valid():
            messages.success(request, 'Feedback form successfully submitted!')
            contact_name = request.POST.get('contact_name', '')
            contact_email = request.POST.get('contact_email', '')
            form_content = request.POST.get('content', '')
            # Email the profile with the
            # contact information
            template = get_template('feedback_template.txt')
            context = Context({
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            })
            content = template.render(context)
            send_mail('Clothes Site Feedback', content, contact_email, ['bam4564@live.unc.edu'], fail_silently=False)
            return redirect('feedback')
    return render(request, 'feedback.html', {
        'feedback_form': feedback_form,
    })


def favorite_clothes_item(request):
    user = request.user
    clothes_item_id = request.GET.get('clothes_item_id', None)
    clothes_item = Clothes_Item.objects.get(id=clothes_item_id)
    try:
        Favorite.objects.get(user=user, clothes_item=clothes_item)
    except:
        favorite = Favorite.objects.create(user=user, clothes_item=clothes_item)
        favorite.save()
    return HttpResponse(True)


def unfavorite_clothes_item(request):
    user = request.user
    clothes_item_id = request.GET.get('clothes_item_id', None)
    clothes_item = Clothes_Item.objects.get(id=clothes_item_id)
    to_unfavorite = Favorite.objects.get(user=user, clothes_item=clothes_item)
    to_unfavorite.delete()
    return HttpResponse(to_unfavorite)


# helper method to return list of the ids for each favorited clothes item of a specific user
def get_favorite_clothes_ids(request):
    user = request.user
    favorites = Favorite.objects.filter(user=user).values()
    favorite_clothes_ids = set()
    for favorite in favorites:
        favorite_clothes_ids.add(favorite['clothes_item_id'])
    return favorite_clothes_ids
