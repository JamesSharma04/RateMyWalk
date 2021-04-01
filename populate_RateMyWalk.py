#Not Working Yet
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RateMyWalk.settings')    

import django
django.setup()

from django.utils import timezone
from rate_my_walk.models import WalkPage, Comment, Rating, Photo, UserProfile
from django.contrib.auth.models import User
from datetime import datetime

def generate_users():
    user_examples = [
    {
    'username': 'ryang45',
    'email': 'ryang45@gmail.com',
    'password': 'Qwerty1235',
    'first_name': 'Ryan',
    'last_name': 'Gregson'},
    {
    'username': 'jamess12',
    'email': 'jamess12@gmail.com',
    'password': 'Qwerty1236',
    'first_name': 'James',
    'last_name': 'Sharma'},
    {
    'username': 'zsoltt98',
    'email': 'zsoltt98@gmail.com',
    'password': 'Qwerty1237',
    'first_name': 'Zsolt',
    'last_name': 'Takacs'},
    {
    'username': 'paule34',
    'email': 'paule34@gmail.com',
    'password': 'Qwerty1238',
    'first_name': 'Paul',
    'last_name': 'Ewins'},
    ]

    for u in user_examples:
        add_user(username=u['username'],email=u['email'],password=u['password'],first_name=u['first_name'],last_name=u['last_name'])

def add_user(username,email,password,first_name,last_name):
    u = User.objects.get_or_create(username=username)[0]
    u.email = email
    u.password = password
    u.first_name = first_name
    u.last_name = last_name
    u.save()

def populate():

    # In media directory
    WalkImageFolder ='page_image'

    walk_examples = [
    {
    'user': User.objects.get(username="ryang45"),
    'name': 'Kelvingrove Park',
    'desc': 'Lovely walk through the park, saw some ducks',
    'start': 'At the park near Sauchiehall Street',
    'end': 'On Eldon Street near the St Andrews Building',
    'cover': os.path.join(WalkImageFolder, 'kgPark.jpg'),
    'enjoyment':8,
    'duration':3,
    'difficulty':5,
    'date':datetime.strptime('3-20-21', '%m-%d-%y')},
    {
    'user': User.objects.get(username="ryang45"),
    'name': 'Kelvin Walkway',
    'desc': 'Had a good time going along the river',
    'start': 'At the skatepark ',
    'end': 'At the botanic gardens',
    'cover': os.path.join(WalkImageFolder, 'kgPark.jpg'),
    'enjoyment':9,
    'duration':5,
    'difficulty':4,
    'date':datetime.strptime('3-24-21', '%m-%d-%y')},
    {
    'user': User.objects.get(username="ryang45"),
    'name': 'Buchanan Street',
    'desc': 'Was nice looking at all the shops, saw some buskers. It was raining though.',
    'start': 'At Sauchiehall street by the concert hall ',
    'end': 'At argyle street',
    'cover': os.path.join(WalkImageFolder, 'kgPark.jpg'),
    'enjoyment':6,
    'duration':2,
    'difficulty':2,
    'date':datetime.strptime('3-22-21', '%m-%d-%y')},
     {
    'user': User.objects.get(username="ryang45"),
    'name': 'Glasgow Green',
    'desc': 'Sunny and bright. Perfect for pints on the grass.',
    'start': 'Saltmarker',
    'end': 'The Green',
    'cover': os.path.join(WalkImageFolder, 'kgPark.jpg'),
    'enjoyment':9,
    'duration':5,
    'difficulty':1,
    'date':datetime.strptime('4-2-21', '%m-%d-%y')},
     {
    'user': User.objects.get(username="ryang45"),
    'name': 'River Clyde',
    'desc': 'Long walk with a nice breeze. Fairly busy.',
    'start': 'Castlebank St',
    'end': 'Clyde St',
    'cover': os.path.join(WalkImageFolder, 'kgPark.jpg'),
    'enjoyment':5,
    'duration':8,
    'difficulty':5,
    'date':datetime.strptime('3-17-21', '%m-%d-%y')},
     {
    'user': User.objects.get(username="ryang45"),
    'name': 'Glasgow Botanic Gardens',
    'desc': 'Lovely area to view some stunning flowers.',
    'start': 'Great Western Rd',
    'end': 'Ford Rd',
    'cover': os.path.join(WalkImageFolder, 'kgPark.jpg'),
    'enjoyment':7,
    'duration':2,
    'difficulty':4,
    'date':datetime.strptime('3-14-21', '%m-%d-%y')},
    ]
    
    for w in walk_examples:
        add_page(user=w['user'],name=w['name'],desc=w['desc'],start=w['start'],end=w['end'],cover=w['cover'],enjoyment=w['enjoyment'],duration=w['duration'],difficulty=w['difficulty'],date=w['date'])

def add_page(user,name,desc,start,end,cover,enjoyment=5,duration=5,difficulty=5,date=timezone.now()):
    #[0] returns the object reference only
    w = WalkPage.objects.get_or_create(name=name)[0]
    w.user = user
    w.desc = desc
    w.start = start
    w.end = end
    w.cover = cover
    w.enjoyment=enjoyment
    w.duration=duration
    w.difficulty=difficulty
    w.date=date
    w.save()
    return w

def makeRatingsForBotanics():

    botanicRatingExamples = [
    {
    'walk': WalkPage.objects.get(name='Glasgow Botanic Gardens'),
    'rater': User.objects.get(username='ryang45'),
    'duration': 4,
    'difficulty': 5,
    'enjoyment': 7},
    {
    'walk': WalkPage.objects.get(name='Glasgow Botanic Gardens'),
    'rater': User.objects.get(username='zsoltt98'),
    'duration': 1,
    'difficulty': 3,
    'enjoyment': 5},
    {
    'walk': WalkPage.objects.get(name='Glasgow Botanic Gardens'),
    'rater': User.objects.get(username='paule34'),
    'duration': 2,
    'difficulty': 3,
    'enjoyment': 10}
    ]

    for wr in botanicRatingExamples:
        add_GBGRates(walk=wr['walk'],rater=wr['rater'],duration=wr['duration'],difficulty=wr['difficulty'],enjoyment=wr['enjoyment'])

def add_GBGRates(walk, rater, duration, difficulty, enjoyment):
    wr = Rating.objects.get_or_create(walk=walk, rater=rater)[0]
    wr.duration = duration
    wr.difficulty = difficulty
    wr.enjoyment = enjoyment
    wr.save()

def morePhotosForBotanics():
    moreImagesFolder = 'more_page_image'

    botanicMorePhotos = [
    {
    'walk': WalkPage.objects.get(name='Glasgow Botanic Gardens'),
    'date': datetime.strptime('3-18-21', '%m-%d-%y'),
    'owner': User.objects.get(username='jamess12'),
    'picture': os.path.join(moreImagesFolder, 'default.jpg')},
    {
    'walk': WalkPage.objects.get(name='Glasgow Botanic Gardens'),
    'date': datetime.strptime('3-18-21', '%m-%d-%y'),
    'owner': User.objects.get(username='zsoltt98'),
    'picture': os.path.join(moreImagesFolder, 'default.jpg')}
    ]

    for wp in botanicMorePhotos:
        add_GBGImages(walk=wp['walk'],date=wp['date'],owner=wp['owner'],picture=wp['picture'])

def add_GBGImages(walk, date, owner, picture):
    wp = Photo.objects.get_or_create(walk=walk, owner=owner, picture=picture)[0]
    wp.date = date
    wp.save()

if __name__=='__main__':
    print('Starting Population Script for RateMyWalk..')
    generate_users()
    populate()
    makeRatingsForBotanics()
    morePhotosForBotanics()
    print("Done")
    