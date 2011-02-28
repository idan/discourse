from django.db import models

# Taken from LibreList sample code
class Confirmation(models.Model):
    from_address = models.EmailField()
    request_date = models.DateTimeField(auto_now_add=True)
    expected_secret = models.CharField(max_length=50)
    pending_message_id = models.CharField(max_length=200)
    list_name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.from_address

# Taken from LibreList sample code
class UserState(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    state_key = models.CharField(max_length=512)
    from_address = models.EmailField()
    state = models.CharField(max_length=200)

    def __unicode__(self):
        return "%s:%s (%s)" % (self.state_key, self.from_address, self.state)

