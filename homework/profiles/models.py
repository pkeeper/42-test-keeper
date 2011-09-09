import datetime
from django.db import models


class Profile(models.Model):

    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
#    birthdate = models.DateField(default=datetime.date(
#                                                       year=1988,
#                                                       month=9,
#                                                       day=15))
    bio = models.TextField()


class ContactField(models.Model):
    CONTACT_TYPE_CHOICES = (
                            ('Email', 'Email'),
                            ('ICQ', 'ICQ'),
                            ('Jabber', 'Jabber'),
                            ('Skype', 'Skype'),
                            ('Other contacts', 'Other contacts'))

    owner = models.ForeignKey(Profile)
    contact_type = models.CharField(max_length=20, db_column='type',
                            choices=CONTACT_TYPE_CHOICES)
    uid = models.CharField(max_length=50)
