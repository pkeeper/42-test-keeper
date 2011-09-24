from django.db import models


class Profile(models.Model):
    """
        User profile model
    """
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    birthdate = models.DateField()
    bio = models.TextField()

    def __unicode__(self):
        return self.name + ' ' + self.surname


class ContactField(models.Model):
    """
        User profile contact field model
    """
    CONTACT_TYPE_CHOICES = (
                            ('Email', 'Email'),
                            ('ICQ', 'ICQ'),
                            ('Jabber', 'Jabber'),
                            ('Skype', 'Skype'),
                            ('Other contacts', 'Other contacts'))

    owner = models.ForeignKey(Profile, default=1)
    contact_type = models.CharField(max_length=20, db_column='type',
                            choices=CONTACT_TYPE_CHOICES)
    uid = models.CharField(max_length=50)

    def __unicode__(self):
        return self.contact_type + ': ' + self.uid
