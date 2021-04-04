from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, RequestFactory
from rate_my_walk.models import UserProfile, WalkPage, Rating, Comment
from django.utils import timezone
from django.urls import reverse
from rate_my_walk.views import showWalk, uploadWalk, editWalk, rateWalk, moreImages
from django.shortcuts import render, redirect


# Create your tests here.

def add_user(username,email,password,first_name,last_name):
    u = User.objects.get_or_create(username=username)[0]
    u.email = email
    u.password = password
    u.first_name = first_name
    u.last_name = last_name
    u.save()
    
    return u


    
class UserTests(TestCase):
    def test_ensure_user_is_created(self):
        """
        Checks to make sure that when a user is created, its details are added appropriately.
        """
        user = add_user('test', 'testeremail@test.com', 'Test123789', 'Joe', 'Bloggs')
        
        self.assertEqual((user.username =='test'), True)
        self.assertEqual((user.email =='testeremail@test.com'), True)
        self.assertEqual((user.password =='Test123789'), True)
        self.assertEqual((user.first_name=='Joe'), True)
        self.assertEqual((user.last_name=='Bloggs'), True)


#---------View Tests--------------
#helper function to register a walk
def add_walk(owner, name, desc, start, end, date):
    walk = WalkPage.objects.get_or_create(owner=owner,
                                          name = name,
                                          desc = desc,
                                          start = start,
                                          end = end,
                                          date = date)[0]
    walk.save()
    return walk

#helper function to register a walk based on name and user and fill the rest with dummy data
def add_new_walk(name, user):
    add_walk(user,
             name,
             'this is description',
             'startpoint',
             'endpoint',
             timezone.now())

#helper function adding ratings
def add_rating(walk, rater, duration, difficulty, enjoyment):
    rating = Rating.objects.get_or_create(walk=walk,
                                          rater=rater,
                                          duration=duration,
                                          difficulty=difficulty,
                                          enjoyment=enjoyment)[0]
    rating.save()
    return rating

def add_comment(owner, walk, title, comment):
    comment = Comment.objects.get_or_create(owner=owner,
                                            walk=walk,
                                            title=title,
                                            comment=comment,
                                            date=timezone.now())[0]
    comment.save()
    return comment


class IndexViewTests(TestCase): 
    def test_index_shows_right_data(self):
        """
        Checks to make sure that the index page works correctly.
        """
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='user', email='user@user.com', password='user_password')

        request = self.factory.get('/rate_my_walk/index')
        request.user = self.user

        add_new_walk('newwalk', request.user)
        add_new_walk('newwalk2', request.user)
        
        response = self.client.get(reverse('rate_my_walk:index'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "newwalk")
        self.assertContains(response, "newwalk2")
        
        num_enjoy = len(response.context['enjoyment'])
        num_recent = len(response.context['recent'])
        self.assertEquals(num_enjoy, 2)
        self.assertEquals(num_recent, 2)
        
    def test_index_view_with_no_walks(self):
        """
        Checks to make sure that the index page works correctly if no walks are added.
        """
        response = self.client.get(reverse('rate_my_walk:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no walks present.')
        self.assertQuerysetEqual(response.context['enjoyment'], [])
        self.assertQuerysetEqual(response.context['recent'], [])
    

class AllWalks(TestCase):
    def test_all_wallks_with_no_walks(self):
        """
        Checks to make sure that the walks page works correctly if no walks are added.
        """
        response = self.client.get(reverse('rate_my_walk:walks'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['walk_list'], [])
    
    def test_all_walks_with_data(self):
        """
        Checks to make sure that the walks page works correctly if walks are present.
        """
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='user', email='user@user.com', password='user_password')

        request = self.factory.get('/rate_my_walk/index')
        request.user = self.user

        add_new_walk('newwalk', request.user)
        add_new_walk('newwalk2', request.user)

        response = self.client.get(reverse('rate_my_walk:walks'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "newwalk")
        self.assertContains(response, "newwalk2")
        
        num_walks = len(response.context['walk_list'])
        self.assertEquals(num_walks, 2)
        


class ShowWalkViewTests(TestCase):
    def test_show_walk_anon_user(self):
        """
        Checks to make sure that the walks show correctly if the user is not logged in.
        """
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='user', email='user@user.com', password='user_password')

        request = self.factory.get('/rate_my_walk/index')
        request.user = self.user
        
        add_new_walk('newwalk', request.user)

        request.user = AnonymousUser()
        response = showWalk(request, 'newwalk')
    
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "newwalk")
        self.assertContains(response, "You must be logged in to leave a comment.")
        self.assertContains(response, "You must be logged in to upload an image.")
        
    def test_show_walk_loggedin_user(self):
        """
        Checks to make sure that the walks show correctly and the user is able to write comments if the user is logged in.
        """
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='user', email='user@user.com', password='user_password')
        
        request = self.factory.get('/rate_my_walk/index')
        request.user = self.user
        
        add_new_walk('newwalk', request.user)
        
        response = self.client.get(reverse('rate_my_walk:showWalk', kwargs={'walk_name_slug': 'newwalk'}))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('walk' in response.context)
        self.assertTrue('photo_form' in response.context)
        self.assertTrue('delete_form' in response.context)
        self.assertTrue('comment_form' in response.context)
        
        response = showWalk(request, 'newwalk')
        self.assertContains(response, "newwalk")
        self.assertContains(response, "Please enter the title of your comment")
        self.assertContains(response, "Write your comment here")
        self.assertContains(response, "If you also had a walk at this location you can upload a picture here")
        self.assertContains(response, "No one rated this walk yet.")
    
    def test_show_walk_loggedin_user_comments_ratings(self):
        """
        Checks to make sure that the comments show correctly if they are posted.
        """
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='user', email='user@user.com', password='user_password')
        
        request = self.factory.get('/rate_my_walk/index')
        request.user = self.user
        
        add_new_walk('newwalk', request.user)
        
        #add 2 ratings
        this_walk = WalkPage.objects.get(name='newwalk')
        add_rating(this_walk, request.user, 10, 10, 10)
        add_rating(this_walk, request.user, 2, 2, 2)
        
        #add comments
        add_comment(request.user, this_walk, "pretty", "very pretty park")
        
        response = self.client.get(reverse('rate_my_walk:showWalk', kwargs={'walk_name_slug': 'newwalk'}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "6")
        self.assertContains(response, "pretty")
        self.assertContains(response, "very pretty park")
        
        num_comments = len(response.context['comments'])
        self.assertEqual(num_comments, 1)
        self.assertEqual(response.context['duration'], 6)
        self.assertEqual(response.context['difficulty'], 6)
        self.assertEqual(response.context['enjoyment'], 6)

        

    
class UploadWalkViewTests(TestCase):
    def test_upload_Walk(self):
        """
        Checks to make sure that the upload walk page works correctly.
        """
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='user', email='user@user.com', password='user_password')
        
        request = self.factory.get('/rate_my_walk/index')
        request.user = self.user
        
        response = uploadWalk(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Have you been on walk recently?")
        self.assertContains(response, "Tell us about it by completing the following form.")
        self.assertContains(response, "Please enter the name of your walk")
        self.assertContains(response, "Please write the description of your walk here")

class EditWalkViewTests(TestCase):
    def test_edit_walk(self):
        """
        Checks to make sure that the edit walk page works correctly.
        """
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='user', email='user@user.com', password='user_password')

        request = self.factory.get('/rate_my_walk/index')
        request.user = self.user
        
        add_new_walk('newwalk', request.user)
        
        response = editWalk(request, 'newwalk')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter the name of your walk")
        self.assertContains(response, "Please write the description of your walk here")
        self.assertContains(response, "newwalk")
        self.assertContains(response, "this is description")


class RateWalkViewTests(TestCase):
    def test_rate_Walk(self):
        """
        Checks to make sure that the rate walk page works correctly.
        """
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='user', email='user@user.com', password='user_password')

        request = self.factory.get('/rate_my_walk/index')
        request.user = self.user
        
        add_new_walk('newwalk', request.user)

        request = self.factory.get('/rate_my_walk/newwalk/')
        request.user = self.user

        response = rateWalk(request, 'newwalk')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rate this walk (between 0-10) for the following three conditions")
        self.assertContains(response, "Duration")
        self.assertContains(response, "Enjoyment")
        self.assertContains(response, "Difficulty")
        

class AboutContactViewTests(TestCase):
    def test_contact_us_page(self):
        """
        Checks to make sure that the contact us page loads correctly
        """
        response = self.client.get(reverse('rate_my_walk:contact_us'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "If you have any suggestions on how we can improve our website")
    
    def test_about_page(self):
        """
        Checks to make sure that the about us page loads correctly
        """
        response = self.client.get(reverse('rate_my_walk:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Our objective is to create a walking social media in Glasgow ")
        
class MoreImagesViewTests(TestCase):
    def test_more_images_page(self):
        """
        Checks to make sure that the more images page loads correctly
        """
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='user', email='user@user.com', password='user_password')

        request = self.factory.get('/rate_my_walk/index')
        request.user = self.user
        
        add_new_walk('newwalk', request.user)
        
        response = moreImages(request, 'newwalk')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "More images of newwalk")
        




        
        


        


