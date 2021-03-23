from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rate_my_walk.models import User, WalkPage, Rating, Photo, Comment
from rate_my_walk.forms import UserForm, WalkPageForm, RatingForm, PhotoForm, CommentForm


def index(request):
    #here I use id as it's in the ER diagram, but for urls we would sue names so might be worth setting name up as a unique foreign key
    most_enjoyable = WalkPage.objects.order_by('-enjoyment')[:5]
    most_recent = WalkPage.objects.order_by('-date')[:5]
    context_dict = {'enjoyment': most_enjoyable,
                    'recent': most_recent}
    return render(request, 'rate_my_walk/index.html', context=context_dict)

def contact_us(request):
    context_dict = {}
    #return render(request, 'RateMyWalk/contact_us.html', conext=context_dict)
    return HttpResponse("contact us page")

def about(request):
    context_dict = {}
    return render(request, 'RateMyWalk/about.html', context=context_dict)
    return HttpResponse("about us page")

def walks(request):
    allWalks = WalkPage.objects.all()
    context_dict = {'walk_list': allWalks,}
    return render(request, 'rate_my_walk/walks.html', context=context_dict)

def showWalk(request, walk_name_slug):
    context_dict = {}
    
    try:
        walk = WalkPage.objects.get(slug = walk_name_slug)
        context_dict['walk'] = walk
    except WalkPage.DoesNotExist:
        context_dict['walk'] = None
    return render(request, 'rate_my_walk/walk.html', context=context_dict)
    #return HttpResponse("shows the clicked walk, based on slug")

def moreImages(request, walk_name_slug):
    allImages = Photo.objects.get(slug = walk_name_slug)
    context_dict = {'images': allImages}
    return render(request, 'RateMyWalk/moreImages.html', context=context_dict)
    return HttpResponse("shows all pictures for one walk based on slug")

@login_required()
def rateWalk(request, walk_name_slug):
    try:
        walk = WalkPage.objects.get(slug=walk_name_slug)
    except WalkPage.DoesNotExist:
        walk = None
    
    if walk is None:
        return redirect('/RateMyWalk/')
    
    form = RatingForm()
    
    if request.method == 'POST':
        form = RatingForm(request.POST)
        
        if form.is_Valid():
            if walk:
                rating = form.save(commit = False)
                rating.walk = walk
                rating.save()
                
                return redirect(reverse('RateMyWalk:show_walk', kwargs = {'walk_name_slug': walk_name_slug}))
    return HttpResponse("can rate a specific walk on this page based on slug")

@login_required()
def myAccount(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect(reverse('RateMyWalk:index'))
    
    walks = WalkPage.objects.get(user=user)
    
    context_dict = {'user': user,
                    'walks': walks,}
    return render(request, 'RateMyWalk/my_profile.html', context=context_dict)
    return HttpResponse("Account details with link to mywalks")

@login_required()
def uploadWalk(request):
    form = WalkPageForm()
    
    if request.method == "POST":
        form = WalkPageForm(request.POST)
        
        if form.isValid():
            form.save(commit = True)
            return redirect('RateMyWalk')
        else:
            print(form.errors)
    return render(request, 'RateMyWalk/upload_walk.html', {'form': form})
    return HttpResponse("form to upload a walk")

@login_required()
def editWalk(request, walk_name_slug):
    #find the walk object to edit
    walk = WalkPage.objects.get(slug=walk_name_slug)
    #extract required infos for auto fill
    walkName = walk.Name
    #put extracted infos into context_dict to show in html
    context_dict = {'walkName': walkName,}
    return HttpResponse("same form as upload, but already filled out and able to change")"""