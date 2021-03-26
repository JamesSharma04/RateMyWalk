#Not Working Yet
import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rate_my_walk.settings')    
from rate_my_walk.models import WalkPage, Comment, Rating, Photo

def populate():
    walk_examples = [
    {'name': 'Kelvingrove Walk',
    'desc': 'Lovely walk through the park, saw some ducks',
    'start': 'At the park near Sauchiehall Street',
    'end': 'On Eldon Street near the St Andrews Building',
    'cover': 'static/images/kg_park_walk_pic.jpg',
    'enjoyment':'8',
    'duration':'3',
    'difficulty':'5',
    'date':'2021-02-24',},
    {'name': 'Kelvin Walkway',
    'desc': 'Had a good time going along the river',
    'start': 'At the skatepark ',
    'end': 'At the botanic gardens',
    'cover': 'static/images/kelvin_walkway_walk_pic.jpg',
    'enjoyment':'9',
    'duration':'5',
    'difficulty':'4',
    'date':'2021-02-28',},
    {'name': 'Buchanan Street',
    'desc': 'Was nice looking at all the shops, saw some buskers. It was raining though.',
    'start': 'At Sauchiehall street by the concert hall ',
    'end': 'At argyle street',
    'cover': 'static:buchanan_street_walk_pic.jpg',
    'enjoyment':'6',
    'duration':'2',
    'difficulty':'2',
    'date':'2021-03-14'}, 
    ]
    
    for w in walk_examples:
        add_page(name=w['name'],desc=w['desc'],start=w['start'],end=w['end'],cover=w['end'],enjoyment=w['enjoyment'],duration=w['duration'],difficulty=w['difficulty'],date=w['date'])
    

def add_page(name,desc,start,end,cover,enjoyment=5,duration=5,difficulty=5,date=timezone.now()):
    #[0] returns the object reference only
    w = WalkPage.objects.get_or_create(name=name)[0]
    w.views = views
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
    populate()
    