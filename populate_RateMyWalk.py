#Not Working Yet
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RateMyWalk.settings')    

import django
django.setup()

from django.utils import timezone
from rate_my_walk.models import WalkPage, Comment, Rating, Photo, UserProfile
from django.contrib.auth.models import User
from datetime import datetime

# Generates Users and creates UserProfiles
def generate_users():
    profilePicFolder ='profile_images'

    user_examples = [
    {
    'username': 'ryang45',
    'email': 'ryang45@gmail.com',
    'password': 'Qwerty1235',
    'first_name': 'Ryan',
    'last_name': 'Gregson',
    'website': 'https://www.github.com/Ryan2469038G',
    'picture': os.path.join(profilePicFolder, 'ryanprofilepic.png')},
    {
    'username': 'jamess12',
    'email': 'jamess12@gmail.com',
    'password': 'Qwerty1236',
    'first_name': 'James',
    'last_name': 'Sharma',
    'website': 'https://www.github.com/JamesSharma04',
    'picture': os.path.join(profilePicFolder, 'jamesprofilepic.png')},
    {
    'username': 'zsoltt98',
    'email': 'zsoltt98@gmail.com',
    'password': 'Qwerty1237',
    'first_name': 'Zsolt',
    'last_name': 'Takacs',
    'website': 'https://www.github.com/2472886T',
    'picture': os.path.join(profilePicFolder, 'myprofilepic.png')},
    {
    'username': 'paule34',
    'email': 'paule34@gmail.com',
    'password': 'Qwerty1238',
    'first_name': 'Paul',
    'last_name': 'Ewins',
    'website': 'https://www.github.com/polewins',
    'picture': os.path.join(profilePicFolder, 'myprofilepic.png')},
    ]

    for u in user_examples:
        userObj = add_user(username=u['username'],email=u['email'],password=u['password'],first_name=u['first_name'],last_name=u['last_name'])
        add_userprofile(user=userObj,website=u['website'],picture=u['picture'])

def add_user(username,email,password,first_name,last_name):
    u = User.objects.get_or_create(username=username)[0]
    u.email = email
    u.password = password
    u.first_name = first_name
    u.last_name = last_name
    u.save()
    return u

def add_userprofile(user,website,picture):
    up = UserProfile.objects.get_or_create(user=user)[0]
    up.website=website
    up.picture=picture
    up.save()


# Generates walks and fills pages with content
# First block of lists - walk ratings
# Second block of lists - walk comments
# Third block of lists - walk more images
# Fourth block of lists - walks and their description
def populateWalks():

    # Walk Ratings

    kgParkRatingExamples = [
    {
    'rater': User.objects.get(username='ryang45'),
    'duration': 2,
    'difficulty': 8,
    'enjoyment': 5},
    {
    'rater': User.objects.get(username='zsoltt98'),
    'duration': 7,
    'difficulty': 2,
    'enjoyment': 9},
    {
    'rater': User.objects.get(username='paule34'),
    'duration': 6,
    'difficulty': 4,
    'enjoyment': 10}
    ]

    kwwRatingExamples = [
    {
    'rater': User.objects.get(username='ryang45'),
    'duration': 7,
    'difficulty': 8,
    'enjoyment': 7},
    {
    'rater': User.objects.get(username='zsoltt98'),
    'duration': 7,
    'difficulty': 2,
    'enjoyment': 9},
    {
    'rater': User.objects.get(username='paule34'),
    'duration': 2,
    'difficulty': 6,
    'enjoyment': 3}
    ]

    bsRatingExamples = [
    {
    'rater': User.objects.get(username='ryang45'),
    'duration': 2,
    'difficulty': 3,
    'enjoyment': 5},
    {
    'rater': User.objects.get(username='zsoltt98'),
    'duration': 1,
    'difficulty': 2,
    'enjoyment': 7},
    {
    'rater': User.objects.get(username='paule34'),
    'duration': 2,
    'difficulty': 6,
    'enjoyment': 3}
    ]

    ggRatingExamples = [
    {
    'rater': User.objects.get(username='ryang45'),
    'duration': 7,
    'difficulty': 8,
    'enjoyment': 9},
    {
    'rater': User.objects.get(username='zsoltt98'),
    'duration': 7,
    'difficulty': 2,
    'enjoyment': 7},
    {
    'rater': User.objects.get(username='paule34'),
    'duration': 2,
    'difficulty': 6,
    'enjoyment': 5}
    ]

    rcRatingExamples = [
    {
    'rater': User.objects.get(username='ryang45'),
    'duration': 7,
    'difficulty': 8,
    'enjoyment': 8},
    {
    'rater': User.objects.get(username='zsoltt98'),
    'duration': 9,
    'difficulty': 6,
    'enjoyment': 3},
    {
    'rater': User.objects.get(username='paule34'),
    'duration': 7,
    'difficulty': 4,
    'enjoyment': 5}
    ]

    gbgRatingExamples = [
    {
    'rater': User.objects.get(username='ryang45'),
    'duration': 4,
    'difficulty': 5,
    'enjoyment': 7},
    {
    'rater': User.objects.get(username='zsoltt98'),
    'duration': 1,
    'difficulty': 3,
    'enjoyment': 9},
    {
    'rater': User.objects.get(username='paule34'),
    'duration': 2,
    'difficulty': 3,
    'enjoyment': 2}
    ]

    # Walk Comments

    kgParkComments = [
    {
    'owner': User.objects.get(username='ryang45'),
    'title': "Sunset",
    'comment': "Lovely sunet view from one of the benches up the hill.",
    'date': datetime.strptime('3-22-21', '%m-%d-%y')},
    {
    'owner': User.objects.get(username='zsoltt98'),
    'title': "Stars",
    'comment': "There's not much light pollution here so if it's clear a walk at night is nice",
    'date': datetime.strptime('3-22-21', '%m-%d-%y')},
    {
    'owner': User.objects.get(username='jamess12'),
    'title': "Good walk",
    'comment': "Quite often walk through here on the way to the university",
    'date': datetime.strptime('3-22-21', '%m-%d-%y')},
    {
    'owner': User.objects.get(username='paule34'),
    'title': "Too busy",
    'comment': "Saw HUNDREDS of people at the park recently, not socially distancing or anything. ",
    'date': datetime.strptime('3-22-21', '%m-%d-%y')},
    ]

    kwwComments = [
    {
    'owner': User.objects.get(username='ryang45'),
    'title': "Massive walk!",
    'comment': "Legs exhausted after todays hike.",
    'date': datetime.strptime('3-27-21', '%m-%d-%y')},
    {
    'owner': User.objects.get(username='zsoltt98'),
    'title': "Good time on the clyde",
    'comment': "Saw some ducks",
    'date': datetime.strptime('3-24-21', '%m-%d-%y')},
    {
    'owner': User.objects.get(username='jamess12'),
    'title': "Fun",
    'comment': "Hadn't been down here before, what a gem",
    'date': datetime.strptime('3-24-21', '%m-%d-%y')},
    {
    'owner': User.objects.get(username='paule34'),
    'title': "Raining",
    'comment': "It was wet and cold. Didn't look like the photo you posted.",
    'date': datetime.strptime('3-22-21', '%m-%d-%y')},
    ]

    bsComments = [
    {
    'owner': User.objects.get(username='ryang45'),
    'title': "Singing performer",
    'comment': "It felt like I was at a concert sitting on those steps at Buchanan Street.",
    'date': datetime.strptime('3-29-21', '%m-%d-%y')},
    {
    'owner': User.objects.get(username='zsoltt98'),
    'title': "Good shopping",
    'comment': "I walked down here, reminicing about the time we had our freedom",
    'date': datetime.strptime('3-22-21', '%m-%d-%y')},
    {
    'owner': User.objects.get(username='jamess12'),
    'title': "Fun to walk",
    'comment': "Because it's so deserted it's actually quite interesting going down here",
    'date': datetime.strptime('3-22-21', '%m-%d-%y')},
    {
    'owner': User.objects.get(username='paule34'),
    'title': "Bit boring",
    'comment': "No green space, no nature at all apart from the pigeons",
    'date': datetime.strptime('3-22-21', '%m-%d-%y')},
    ]

    ggComments = [
    {
    'owner': User.objects.get(username='ryang45'),
    'title': "Jogging",
    'comment': "Took a jog round this flat park which was fun.",
    'date': datetime.strptime('4-6-21', '%m-%d-%y')},
    {
    'owner': User.objects.get(username='zsoltt98'),
    'title': "Big park",
    'comment': "Nice to go here after shopping normally, love being in nature",
    'date': datetime.strptime('4-6-21', '%m-%d-%y')},
    {
    'owner': User.objects.get(username='jamess12'),
    'title': "Nice",
    'comment': "I like how near it is to the river, lovely skyline also",
    'date': datetime.strptime('4-6-21', '%m-%d-%y')},
    {
    'owner': User.objects.get(username='paule34'),
    'title': "Good history",
    'comment': "The nelson monument in the middle is great, did you know it was struck by lightning soon after construction which put a big crack in the thing?",
    'date': datetime.strptime('4-6-21', '%m-%d-%y')},
    ]

    rcComments = [
    {
    'owner': User.objects.get(username='ryang45'),
    'title': "Windy walk",
    'comment': "Extremely chilling winds down here, I should've wore a jumper.",
    'date': datetime.strptime('3-20-21', '%m-%d-%y')},
    {
    'owner': User.objects.get(username='zsoltt98'),
    'title': "Too windy",
    'comment': "Sick fed up of being blown along the road. Go somewhere else",
    'date': datetime.strptime('4-2-21', '%m-%d-%y')},
    {
    'owner': User.objects.get(username='jamess12'),
    'title': "Class walk",
    'comment': "Ignore the others, this walk was great. Very varied scenery. ",
    'date': datetime.strptime('4-5-21', '%m-%d-%y')},
    {
    'owner': User.objects.get(username='paule34'),
    'title': "Decent walk",
    'comment': "Good view of the skyline",
    'date': datetime.strptime('4-6-21', '%m-%d-%y')},
    ]

    gbgComments = [
    {
    'owner': User.objects.get(username='ryang45'),
    'title': "Chilling",
    'comment': "Me and my friends chilled here today because it was sunny.",
    'date': datetime.strptime('3-24-21', '%m-%d-%y')},
    {
    'owner': User.objects.get(username='zsoltt98'),
    'title': "Lovely greenery",
    'comment': "Nice to see all the exotic plants around here",
    'date': datetime.strptime('4-6-21', '%m-%d-%y')},
    {
    'owner': User.objects.get(username='jamess12'),
    'title': "Brilliant",
    'comment': "Good to learn about all the plants and that, they have labels which helps",
    'date': datetime.strptime('4-6-21', '%m-%d-%y')},
    {
    'owner': User.objects.get(username='paule34'),
    'title': "Rip off",
    'comment': "Some charlatan charged me a fiver for entry, thought it was free? And the coffee was too expensive too. Don't recommend, walkers",
    'date': datetime.strptime('4-6-21', '%m-%d-%y')},
    ]

    # Walk More Images

    MoreWalkImageFolder ='more_page_image'

    kgParkPhotos = [
    {
    'owner': User.objects.get(username='ryang45'),
    'picture': os.path.join(MoreWalkImageFolder, 'ryanKgPark.jpg'),
    'date': datetime.strptime('3-22-21', '%m-%d-%y')},
    {
    'owner': User.objects.get(username='zsoltt98'),
    'picture': os.path.join(MoreWalkImageFolder, 'zsolttKGPark.jpg'),
    'date': datetime.strptime('3-22-21', '%m-%d-%y')},
    ]

    kwwPhotos = [
    {
    'owner': User.objects.get(username='ryang45'),
    'picture': os.path.join(MoreWalkImageFolder, 'ryanKWW.jpg'),
    'date': datetime.strptime('3-22-21', '%m-%d-%y')},
    {
    'owner': User.objects.get(username='zsoltt98'),
    'picture': os.path.join(MoreWalkImageFolder, 'zsolttKWW.jpg'),
    'date': datetime.strptime('3-22-21', '%m-%d-%y')},
    ]

    bsPhotos = [
    {
    'owner': User.objects.get(username='ryang45'),
    'picture': os.path.join(MoreWalkImageFolder, 'ryanBS.jpeg'),
    'date': datetime.strptime('3-22-21', '%m-%d-%y')},
    {
    'owner': User.objects.get(username='paule34'),
    'picture': os.path.join(MoreWalkImageFolder, 'paulBS.jpg'),
    'date': datetime.strptime('3-22-21', '%m-%d-%y')},
    ]

    ggPhotos = [
    {
    'owner': User.objects.get(username='jamess12'),
    'picture': os.path.join(MoreWalkImageFolder, 'jamesGG.png'),
    'date': datetime.strptime('3-22-21', '%m-%d-%y')},
    {
    'owner': User.objects.get(username='paule34'),
    'picture': os.path.join(MoreWalkImageFolder, 'paulGG.jpg'),
    'date': datetime.strptime('3-22-21', '%m-%d-%y')},
    ]

    rcPhotos = [
    {
    'owner': User.objects.get(username='jamess12'),
    'picture': os.path.join(MoreWalkImageFolder, 'jamesRC.jpg'),
    'date': datetime.strptime('3-22-21', '%m-%d-%y')},
    {
    'owner': User.objects.get(username='paule34'),
    'picture': os.path.join(MoreWalkImageFolder, 'paulRC.png'),
    'date': datetime.strptime('3-22-21', '%m-%d-%y')},
    ]

    gbgPhotos = [
    {
    'owner': User.objects.get(username='jamess12'),
    'picture': os.path.join(MoreWalkImageFolder, 'jamesGBG.jpg'),
    'date': datetime.strptime('3-22-21', '%m-%d-%y')},
    {
    'owner': User.objects.get(username='zsoltt98'),
    'picture': os.path.join(MoreWalkImageFolder, 'zsolttGBG.jpg'),
    'date': datetime.strptime('3-22-21', '%m-%d-%y')},
    ]

    # Walks

    # In media directory
    WalkImageFolder ='page_image'

    walk_examples = [
    {
    'user': User.objects.get(username="zsoltt98"),
    'name': 'Kelvingrove Park',
    'desc': 'Lovely walk through the park, saw some ducks',
    'start': 'At the park near Sauchiehall Street',
    'end': 'On Eldon Street near the St Andrews Building',
    'cover': os.path.join(WalkImageFolder, 'kgpark.jpg'),
    'enjoyment':8,
    'duration':3,
    'difficulty':5,
    'date':datetime.strptime('3-20-21', '%m-%d-%y'),
    'userRating':kgParkRatingExamples,
    'userComment':kgParkComments,
    'moreImages': kgParkPhotos},
    {
    'user': User.objects.get(username="jamess12"),
    'name': 'Kelvin Walkway',
    'desc': 'Had a good time going along the river',
    'start': 'At the skatepark ',
    'end': 'At the botanic gardens',
    'cover': os.path.join(WalkImageFolder, 'KWW.jpg'),
    'enjoyment':9,
    'duration':5,
    'difficulty':4,
    'date':datetime.strptime('3-24-21', '%m-%d-%y'),
    'userRating':kwwRatingExamples,
    'userComment':kwwComments,
    'moreImages':kwwPhotos},
    {
    'user': User.objects.get(username="jamess12"),
    'name': 'Buchanan Street',
    'desc': 'Was nice looking at all the shops, saw some buskers. It was raining though.',
    'start': 'At Sauchiehall street by the concert hall ',
    'end': 'At argyle street',
    'cover': os.path.join(WalkImageFolder, 'BC.jpg'),
    'enjoyment':6,
    'duration':2,
    'difficulty':2,
    'date':datetime.strptime('3-22-21', '%m-%d-%y'),
    'userRating':bsRatingExamples,
    'userComment':bsComments,
    'moreImages':bsPhotos},
    {
    'user': User.objects.get(username="paule34"),
    'name': 'Glasgow Green',
    'desc': 'Sunny and bright. Perfect for pints on the grass.',
    'start': 'Saltmarker',
    'end': 'The Green',
    'cover': os.path.join(WalkImageFolder, 'GG.jpg'),
    'enjoyment':9,
    'duration':5,
    'difficulty':1,
    'date':datetime.strptime('4-2-21', '%m-%d-%y'),
    'userRating':ggRatingExamples,
    'userComment':ggComments,
    'moreImages':ggPhotos},
    {
    'user': User.objects.get(username="paule34"),
    'name': 'River Clyde',
    'desc': 'Long walk with a nice breeze. Fairly busy.',
    'start': 'Castlebank St',
    'end': 'Clyde St',
    'cover': os.path.join(WalkImageFolder, 'RC.jpg'),
    'enjoyment':5,
    'duration':8,
    'difficulty':5,
    'date':datetime.strptime('3-17-21', '%m-%d-%y'),
    'userRating':rcRatingExamples,
    'userComment':rcComments,
    'moreImages':rcPhotos},
    {
    'user': User.objects.get(username="ryang45"),
    'name': 'Glasgow Botanic Gardens',
    'desc': 'Lovely area to view some stunning flowers.',
    'start': 'Great Western Rd',
    'end': 'Ford Rd',
    'cover': os.path.join(WalkImageFolder, 'ryanGBG.jpeg'),
    'enjoyment':7,
    'duration':2,
    'difficulty':4,
    'date':datetime.strptime('3-14-21', '%m-%d-%y'),
    'userRating':gbgRatingExamples,
    'userComment':gbgComments,
    'moreImages':gbgPhotos},
    ]

    for w in walk_examples:
        walkObj = add_page(user=w['user'],name=w['name'],desc=w['desc'],start=w['start'],end=w['end'],cover=w['cover'],enjoyment=w['enjoyment'],duration=w['duration'],difficulty=w['difficulty'],date=w['date'])
        for wr in w['userRating']:
            add_rates(walk=walkObj,rater=wr['rater'],duration=wr['duration'],difficulty=wr['difficulty'],enjoyment=wr['enjoyment'])
        for wc in w['userComment']:
            add_comments(owner=wc['owner'],walk=walkObj,title=wc['title'],comment=wc['comment'],date=wc['date'])
        for wp in w['moreImages']:
            add_moreImages(walk=walkObj,date=wp['date'],owner=wp['owner'],picture=wp['picture'])

def add_page(user,name,desc,start,end,cover,enjoyment=5,duration=5,difficulty=5,date=timezone.now()):
    #[0] returns the object reference only
    w = WalkPage.objects.get_or_create(name=name)[0]
    w.owner = user
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

def add_rates(walk, rater, duration, difficulty, enjoyment):
    wr = Rating.objects.get_or_create(walk=walk, rater=rater)[0]
    wr.duration = duration
    wr.difficulty = difficulty
    wr.enjoyment = enjoyment
    wr.save()

def add_comments(owner, walk, title, comment, date):
    wc = Comment.objects.get_or_create(walk=walk, owner=owner, date=date)[0]
    wc.title = title
    wc.comment = comment
    wc.save()

def add_moreImages(walk, date, owner, picture):
    wp = Photo.objects.get_or_create(walk=walk, owner=owner, picture=picture)[0]
    wp.date = date
    wp.save()

if __name__=='__main__':
    print('Starting Population Script for RateMyWalk..')
    generate_users()
    populateWalks()
    print("RateMyWalk populated")