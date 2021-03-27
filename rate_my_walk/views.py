from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rate_my_walk.models import User, WalkPage, Comment, Photo, Rating
from rate_my_walk.forms import RatingForm, WalkPageForm, PhotoForm
#from rate_my_walk.forms import UserForm, WalkPageForm, RatingForm, PhotoForm, CommentForm
from rate_my_walk.bing_search import run_query
from django.utils import timezone



def index(request):
    #here I use id as it's in the ER diagram, but for urls we would sue names so might be worth setting name up as a unique foreign key
    most_enjoyable = WalkPage.objects.order_by('-enjoyment')[:5]
    most_recent = WalkPage.objects.order_by('-date')[:5]
    context_dict = {'enjoyment': most_enjoyable,
                    'recent': most_recent}
    return render(request, 'rate_my_walk/index.html', context=context_dict)

def contact_us(request):
    context_dict = {}
    return render(request, 'rate_my_walk/contact_us.html', context=context_dict)
    #return HttpResponse("contact us page")

def about(request):
    context_dict = {}
    return render(request, 'rate_my_walk/about.html', context=context_dict)
    #return HttpResponse("about us page")

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

    #tried to include all comments under a walk.
    #wouldnt't allow datefiedl included in the ForeignKey 
    # if walk:
    #     try:
    #         comments = Comment.objects.get(walkPage=walk)
    #         context_dict['comments'] = comments
    #     except WalkPage.DoesNotExist:
    #         context_dict['comments'] = None
    
    result_list = []
    query=""
    photo_form = PhotoForm()
    context_dict['photo_form'] = photo_form
    
    if request.method == 'POST':
        #search related post
        if 'query' in request.POST:
            query = request.POST['query'].strip()
            if query:
                result_list = run_query(query)
        
        #extra image related post
        if 'picture' in request.FILES:
            photo_form = PhotoForm(request.POST, request.FILES)
            if photo_form.is_valid():
                if walk:
                    print("heyyyyy")
                    newPhoto = photo_form.save(commit=False)
                    newPhoto.walk = walk
                    newPhoto.owner = request.user
                    newPhoto.date = timezone.now()
                    newPhoto.save()
                    print(newPhoto)
                    return redirect(reverse('rate_my_walk:more_images', kwargs = {'walk_name_slug': walk_name_slug}))
            else:
                print(photo_form.errors)
            
        context_dict['result_list'] = result_list
        context_dict['last_query'] = query
        context_dict['photo_form'] = photo_form

    
    return render(request, 'rate_my_walk/walk.html', context=context_dict)
    #return HttpResponse("shows the clicked walk, based on slug")

def moreImages(request, walk_name_slug):
    currentWalk = WalkPage.objects.get(slug=walk_name_slug)
    allImages = Photo.objects.filter(walk=currentWalk)
    context_dict = {'images': allImages}
    #returns all instances of the photo model. images.picture points to the actial pic
    return render(request, 'rate_my_walk/moreImages.html', context=context_dict)

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
        
        if form.is_valid():
            if walk:
                rating = form.save(commit = False)
                rating.walk = walk
                rating.save()
                return redirect(reverse('rate_my_walk:showWalk', kwargs = {'walk_name_slug': walk_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'walk': walk}
    return render(request, 'rate_my_walk/rateWalk.html', context_dict)
    ##return HttpResponse("can rate a specific walk on this page based on slug")

@login_required()
def myAccount(request):
    # try:
    #     user = User.objects.get(username=username)
    # except User.DoesNotExist:
    #     return redirect(reverse('RateMyWalk:index'))
    
    walks = WalkPage.objects.get(owner = request.user)
    
    context_dict = {'username': request.user,
                    'walks': walks,}
    return render(request, 'rate_my_walk/my_profile.html', context=context_dict)
    return HttpResponse("Account details with link to mywalks")

@login_required()
def uploadWalk(request):
    form = WalkPageForm()
    
    if request.method == "POST":
        form = WalkPageForm(request.POST, request.FILES)
        
        if form.is_valid():
            new_walk = form.save(commit=False)
            new_walk.owner = request.user
            new_walk.save()
            return redirect(reverse('rate_my_walk:index'))
        else:
            print(form.errors)
    return render(request, 'rate_my_walk/uploadWalk.html', {'form': form})
    ##return HttpResponse("form to upload a walk")

@login_required()
def editWalk(request, walk_name_slug):
    #find the walk object to edit
    try:
        walk = WalkPage.objects.get(slug=walk_name_slug)
    except WalkPage.DoesNotExist:
        walk = None
    
    if walk is None:
        redirect('RateMyWalk')

    if request.method == "GET":
        #extract required infos for auto fill
        walkName = walk.Name
        #put extracted infos into context_dict to show in html
        context_dict = {'walkName': walkName,}
        #html - <input value="{{walkName}}"/>
        return render(request, 'RateMyWalk/upload_walk.html', context=context_dict)
    
    if request.method == "POST":
        #if walk already exists update it - or delete and create again?
        #redirect to walkPage
        return redirect(reverse('RateMyWalk:walk.html', kwargs = {'walk_name_slug': walk_name_slug}))


@login_required()
def uploadMorePhotos(request, walk_name_slug):
    try:
        walk = WalkPage.objects.get(slug=walk_name_slug)
    except WalkPage.DoesNotExist:
        walk = None
    
    if walk is None:
        return redirect('/RateMyWalk/')

    form = PhotoForm()
    
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        
        if form.is_valid():
            if walk:
                photo = form.save(commit=False)
                photo.walkPage = walk
                photo.owner = request.user
                photo.save()
                return redirect(reverse('RateMyWalk:moreImages', kwargs = {'walk_name_slug': walk_name_slug}))
        else:
            print(form.errors)
    
    return render(request, 'RateMyWalk/upload_more_photos.html', {'form': form})