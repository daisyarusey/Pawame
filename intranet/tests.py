from django.test import TestCase
from .models import *
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