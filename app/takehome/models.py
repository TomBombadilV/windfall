from django.db import models
from django.utils import timezone

class Subreddit(models.Model):
    """ A subreddit must have:
        - Identifying name (ex: 'AskReddit'). Limited by 180 chars
        - Date followed, so that we can evict the oldest if necessary
    """
    name = models.CharField(max_length=180)
    date_followed = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name