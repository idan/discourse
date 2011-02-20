from django.db import models

class InterestGroupManager(models.Manager):

    def public(self):
        """Return the public groups"""

        return self.get_query_set().filter(public=True)

    def private(self):
        """Return the private groups"""

        return self.get_query_set().exclude(public=True)

