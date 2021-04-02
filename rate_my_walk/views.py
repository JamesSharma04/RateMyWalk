from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rate_my_walk.models import User, WalkPage, Comment, Photo, Rating, UserProfile
from rate_my_walk.forms import RatingForm, WalkPageForm, PhotoForm, CommentForm, DeleteWalkForm, UserProfileForm
#from rate_my_walk.forms import UserForm, WalkPageForm, RatingForm, PhotoForm, CommentForm
from rate_my_walk.bing_search import run_query
from django.utils import timezone
from django.views.generic import View
from django.utils.decorators import method_decorator


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
    allWalks = WalkPage.objects.order_by('-enjoyment')
    sort = 'enjoyment'

    if 'attribute' in request.POST:
        attribute = '-' + request.POST['attribute'].lower()
        allWalks = WalkPage.objects.order_by(attribute)
        sort = request.POST['attribute'].lower()
    context_dict = {'walk_list': allWalks,
                    'sort': sort,}
    
    return render(request, 'rate_my_walk/walks.html', context=context_dict)

def showWalk(request, walk_name_slug):
    context_dict = {}
    
    #check if walk exists based on slug
    try:
        walk = WalkPage.objects.get(slug = walk_name_slug)
        context_dict['walk'] = walk
    except WalkPage.DoesNotExist:
        context_dict['walk'] = None
        return redirect(reverse('rate_my_walk:index'))
    
    #get mean user ratings
    ratings = Rating.objects.filter(walk=walk)
    if ratings:
        counter = 0
        difficulty_sum = 0
        duration_sum = 0
        enjoyment_sum = 0
        
        for rating in ratings:
            difficulty_sum += rating.difficulty
            duration_sum += rating.duration
            enjoyment_sum = rating.enjoyment
            counter += 1
            
        difficulty_mean = difficulty_sum/counter
        duration_mean = duration_sum/counter
        enjoyment_mean = enjoyment_sum/counter
        context_dict['duration'] = duration_mean
        context_dict['difficulty'] = difficulty_mean
        context_dict['enjoyment'] = enjoyment_mean

    #get all comments
    all_comments = Comment.objects.filter(walk=walk)
    if all_comments:
        context_dict['comments'] = all_comments
    
    result_list = []
    query=""
    photo_form = PhotoForm()
    comment_form = CommentForm()
    context_dict['photo_form'] = photo_form
    context_dict['comment_form'] = comment_form
    
    delete_form = DeleteWalkForm()
    context_dict['delete_form'] = delete_form
    
    if request.method == 'POST':
        #search related post
        if 'query' in request.POST:
            query = request.POST['query'].strip()
            if query:
                result_list = run_query(query)
        
        #if post is about comments
        if 'comment' in request.POST and 'title' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                if walk:
                    newComment = comment_form.save(commit=False)
                    newComment.owner = request.user
                    newComment.walk = walk
                    newComment.date = timezone.now()
                    newComment.save()
                    return redirect(reverse('rate_my_walk:showWalk', kwargs={'walk_name_slug': walk_name_slug}))
            else:
                print(comment_form.errors)
        
        #extra image related post
        if 'picture' in request.FILES:
            photo_form = PhotoForm(request.POST, request.FILES)
            if photo_form.is_valid():
                if walk:
                    newPhoto = photo_form.save(commit=False)
                    newPhoto.walk = walk
                    newPhoto.owner = request.user
                    newPhoto.date = timezone.now()
                    newPhoto.save()
                    return redirect(reverse('rate_my_walk:more_images', kwargs = {'walk_name_slug': walk_name_slug}))
            else:
                print(photo_form.errors)
        
        #delete related post
        if 'slug' in request.POST:
            walk.delete()
            return redirect(reverse('rate_my_walk:index'))
            
        context_dict['result_list'] = result_list
        context_dict['last_query'] = query
        context_dict['photo_form'] = photo_form

    
    return render(request, 'rate_my_walk/walk.html', context=context_dict)
    #return HttpResponse("shows the clicked walk, based on slug")

def moreImages(request, walk_name_slug):
    currentWalk = WalkPage.objects.get(slug=walk_name_slug)
    allImages = Photo.objects.filter(walk=currentWalk)
    context_dict = {'images': allImages, 'walk':currentWalk}
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
                rating.rater = request.user
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
    
    walks = WalkPage.objects.filter(owner=request.user)
    
    context_dict = {'username': request.user,
                    'walks': walks,}
    return render(request, 'rate_my_walk/my_profile.html', context=context_dict)
    #return HttpResponse("Account details with link to mywalks")

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
        redirect('RateMyWalk')
    
    #fill new form with current instance
    form = WalkPageForm(request.POST or None, instance=walk)
    
    #update all fields based on POST
    if form.is_valid():
        edit = form.save(commit=False)
        #update picture if needed
        if request.FILES:
            edit.cover = request.FILES['cover']
        #should we update date too?
        edit.save()
        return redirect(reverse('rate_my_walk:index'))
    
    context_dict = {'walk': walk,
                    'form': form}

    return render(request, 'rate_my_walk/editWalk.html', context_dict)     

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

@login_required()
def register_profile(request):

    form = UserProfileForm()
    
    if request.method=='POST':
        form = UserProfileForm(request.POST, request.FILES)
        
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user=request.user
            user_profile.save()
            
            return redirect(reverse('rate_my_walk:index'))
        else:
            # probably better to do soemthing else to make it more intuitive for the user
            print(form.errors)
    context_dict={'form': form}
    return render(request,'rate_my_walk/profile_registration.html', context_dict)
    


class ProfileView(View):

    #helper method
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            #will redirect to homepage, could make an error msg 
            return None

        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'website': user_profile.website,
                               'picture': user_profile.picture})
        return (user, user_profile, form)

    #user has to be logged in for both get and post
    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('rate_my_walk:index'))

        context_dict = {'user_profile': user_profile,
                        'selected_user': user, 'form': form}

        return render(request, 'rate_my_walk/profile.html',
                      context_dict)

    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('rate_my_walk:index'))
        form = UserProfileForm(request.POST, request.FILES,
                               instance=user_profile)

        if form.is_valid():
            form.save(commit=True)
            return redirect('rate_my_walk:profile', user.username)
        else:
            print(form.errors)

        context_dict = {'user_profile': user_profile,
                        'selected_user': user, 'form': form}
        return render(request, 'rate_my_walk/updateProfile.html',
                      context_dict)
                      
class ListProfilesView(View):
    @method_decorator(login_required)
    def get(self, request):
        profiles = UserProfile.objects.all()

        return render(request, 'rate_my_walk/list_walkers.html', {'user_profile_list': profiles})