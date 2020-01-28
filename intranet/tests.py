from django.test import TestCase
from .models import *
# Create your tests here.
# class MyUserManagerTestClass(TestCase):
   
#    # Set up method
#     def setUp(self):
#         self.myusermanager= MyUserManager(user_type=1,department='alldepartments')

#     def test_instance(self):
#         self.asserTrue(isinstance(self.myusermanager,MyUserManager))
    
#     # def test_save_method(self):
#     #     self.myusermanager.create_superuser()
#     #     myusermanager=MyUserManager.objects.all()
#     #     self.assertTrue(len(myusermanager)>0)

#     # def test_delete_method(self):
#     #     self.myusermanager.create_superuser()
#     #     self.myusermanager.delete_superuser()
#     #     myusermanager = MyUserManager.objects.all()
#     #     self.assertTrue(len(myusermanager) is 0)
    
#     def tearDown(self):
#         MyUserManager.objects.all().delete()


# class UserTestClass(TestCase):

#     def setUp(self):
#         self.user = User(usertype=2, department='inventory')

#     def test_instance(self):
#         self.assertTrue(isinstance(self.name,User))

#     def tearDown(self):
#         User.objects.all().delete()

#     def test_save_method(self):
#         self.name.save_user()
#         user = User.objects.all()
#         self.assertTrue(len(user)>0)

#     def test_delete_method(self):
#         self.name.delete_user('admin')
#         user = User.objects.all()
#         self.assertTrue(len(user)==0)

class ProfileTestClass(TestCase):
    def setUp(self):
        self.profile_one = Profile(image='images/mine.jpg', first_name='Ikerriz', last_name='Okoth',user_id=1)
        
        
    def test_instance(self):
        self.assertTrue(isinstance(self.profile_one,Profile)) 

    def test_save_method(self):
        self.profile_one.save_profile()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles) > 0)

    def test_delete_method(self):
        self.profile_one.save_profile()
        self.profile_one.delete_profile()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles) is 0)
        
    def test_update_method(self):
        self.profile_one.save_profile()
        first_name = 'Faith'
        done = self.profile_one.update_profile(self.profile_one.pk, first_name)
        self.assertEqual(done, first_name)
        
    def tearDown(self):
        Profile.objects.all().delete()