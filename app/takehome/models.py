from django.db import models

class SubReddit(models.Model):
    """ A subreddit must have:
        - Identifying name (ex: 'AskReddit'). Limited by 180 chars
    """
    name = models.CharField(max_length=180)
