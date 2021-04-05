from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, RequestFactory
from rate_my_walk.models import UserProfile, WalkPage, Rating, Comment
from django.utils import timezone
from django.urls import reverse
from rate_my_walk.views import showWalk, uploadWalk, editWalk, rateWalk, moreImages
from django.shortcuts import render, redirect
from rate_my_walk.bing_search import read_bing_key, run_query

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
        Checks to make sure that the walks show correctly and when logged in the user can see more information about commenting
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
        
        response = showWalk(request, 'error')
        #Check that putting in a walk that doesn't exist returns a redirect
        self.assertEqual(response.status_code, 302)
    
    
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
        
        response = editWalk(request, 'error')
        #Check that putting in a walk that doesn't exist returns a redirect
        self.assertEqual(response.status_code, 302)


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
        
        
        response = rateWalk(request, 'error')
        #Check that putting in a walk that doesn't exist returns a redirect
        self.assertEqual(response.status_code, 302)
        

class AboutContactViewTests(TestCase):

    def test_contact_us_url_exists(self):
        """
        Checks to see if the contact us view exists in the correct place, with the correct name.
        """
        url = ''

        try:
            url = reverse('rate_my_walk:contact_us')
        except:
            pass
        self.assertEqual(url, '/RateMyWalk/contact-us/')
        

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
        
class BingTests(TestCase):
    def test_read_bing_key(self):
        """
        Checks to make sure that bing_search.py gets the correct API key as specified in bing.key
        """
        key = read_bing_key()
        self.assertEqual(key, '4ad55fca778f4dbd8487d5dc26ef773c')
        
     
    def test_bing_results_output(self):
        """
        Checks to make sure that the bing search returns the correct search results
        """
        results = run_query('google')
        self.assertEqual(results[0]["title"], 'Google')
        self.assertEqual(results[0]["link"], 'https://www.google.co.uk/')

class RegisterTests(TestCase):
    
    def test_register_page(self):
        """
        Checks to make sure that the register page returns the correct response
        """ 
        #self.factory = RequestFactory()
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter a secure and memorable password.')
        self.assertContains(response, 'Already got an account?')
        
class LoginTests(TestCase):

    def test_login_page(self):
        """
        Checks to make sure that the login page returns the correct response
        """ 
        #self.factory = RequestFactory()
        response = self.client.get('/accounts/login/')
        self.assertContains(response, 'Login')
        self.assertContains(response, 'Not registered?')
        self.assertEqual(response.status_code, 200)
        
    def test_login_post(self):
        """
        Checks to make sure that a user can log in when the correct info is posted
        """     
        self.user = User.objects.create_user(
            username='user', email='user@user.com', password='user_password')
        response = self.client.post(('/accounts/login/'), data={
            'username': 'user',
            'password': 'user_password',
        }, follow = True)
        
        self.assertTrue(response.context['user'].is_active)
        self.assertEqual(response.status_code, 200)
        
        
        
        


        


