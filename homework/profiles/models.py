from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    birthdate = models.DateField()
    bio  = models.TextField()
    
class ContactField(models.Model):
    CONTACT_TYPE_CHOICES = (
                            ('email', 'Email'),
                            ('icq', 'ICQ'),
                            ('jabber', 'Jabber'),
                            ('skype', 'Skype'),
                            ('other', 'other')
                            )
    
    owner = models.ForeignKey(Profile)
    contact_type = models.CharField(max_length=20, db_column='type',
                            choices=CONTACT_TYPE_CHOICES)
    uid = models.CharField(max_length=50)