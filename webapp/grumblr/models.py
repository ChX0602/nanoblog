from django.db import models
from django.contrib.auth.models import User
import datetime

class CustomUser(models.Model):
    user = models.OneToOneField(User)
    followers = models.ManyToManyField(User, related_name="follower")
    blocked = models.ManyToManyField(User, related_name="blocked")
    
class Profile(models.Model):
    owner = models.OneToOneField(User)
    first_name = models.CharField(max_length=200, default="", blank=True)
    last_name = models.CharField(max_length=200, default="", blank=True)
    address_1 = models.CharField(max_length=200, default="", blank=True)
    address_2 = models.CharField(max_length=200, default="", blank=True)
    city = models.CharField(max_length=200, default="", blank=True)
    state = models.CharField(max_length=200, default="", blank=True)
    zip = models.CharField(max_length=200, default="", blank=True)
    country = models.CharField(max_length=200, default="", blank=True)
    phone = models.CharField(max_length=200, default="", blank=True)
    picture = models.ImageField(upload_to="profile-photos", default='profile-photos/default_user.png', blank=True)

    def __unicode__(self):
        return self.first_name + " " + self.last_name
    @staticmethod
    def get_profiles(owner):
        return Profile.objects.filter(owner=owner).order_by('last_name', 'first_name')
    def getAllFields():
        return self._meta.get_all_field_names()
    


class Post(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    user_name = models.CharField(max_length=200, null=True)
    dislikers = models.ManyToManyField(Profile)
    date = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now())
    picture = models.ImageField(upload_to="post-photos", null=True, blank=True)
    def __unicode__(self):
        return self.text

class Comment(models.Model):
    text = models.CharField(max_length=200)
    post = models.ForeignKey(Post)
    commenter = models.ForeignKey(User)
    commenter_name = models.CharField(max_length=200, null=True)
    def __unicode__(self):
        return self.text

    
    
class Info(models.Model):
    firstname = models.CharField(max_length=50, default="")
    lastname = models.CharField(max_length=50, default="")
    dateofbirth = models.CharField(max_length=50, default="")
    organization = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=50, default="")
    state = models.CharField(max_length=50, default="")
    country = models.CharField(max_length=50, default="")
    user = models.ForeignKey(User, default="")
    def _unicode__(self):
        return self.firstname + self.lastname
    
