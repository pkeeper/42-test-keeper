from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    bio  = models.TextField()
    
class ContactField(models.Model):
    CONTACT_TYPE_CHOICES = (
                            ('email', 'email'),
                            ('icq', 'icq'),
                            ('jabber', 'jabber'),
                            )
    owner = models.ForeignKey(Profile)
    type = models.CharField(max_length=20, choices=CONTACT_TYPE_CHOICES)
    uid = models.CharField(max_length=50)