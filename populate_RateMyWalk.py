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

    new_user = User.objects.create(
        username="ryang45",
        first_name="Ryan",
        last_name="Gregson",
    )
    new_user.save()
    # create profile for user
    p = UserProfile.objects.create(user=new_user)
    p.save()

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
    'date':datetime.strptime('3-20-20', '%m-%d-%y')},
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
    
if __name__=='__main__':
    print('Starting Population Script for RateMyWalk..')
    generate_users()
    populate()
    print("Done")
    