from django.contrib.auth.models import User
from django.test import TestCase
from rate_my_walk.models import UserProfile,WalkPage
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

 
