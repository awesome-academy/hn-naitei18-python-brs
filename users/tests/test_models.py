from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Profile
from django.core.files.uploadedfile import SimpleUploadedFile

class ModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create(username='testuser')
        profile = Profile.objects.get(id=1)
        profile.image=SimpleUploadedFile(name='test_image.jpg',
                                        content=open("media/default.png", 'rb').read(),
                                        content_type='image/jpeg')

    def test_profile_user_name_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile.user._meta.get_field('username').verbose_name
        self.assertEquals(field_label, 'username')

    def test_object_username_is_username(self):
        profile = Profile.objects.get(id=1)
        expected_object_name = profile.user.username + ' Profile'
        self.assertEquals(expected_object_name, str(profile))
