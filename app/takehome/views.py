from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import FollowSubredditForm
from .models import Subreddit

def index(request):
    return render(request, 'takehome/index.html')

def evict_oldest_subreddit() -> None:
    """ Evicts the oldest subreddit followed """
    oldest_subreddit = Subreddit.objects.latest('date_followed')
    oldest_subreddit.delete()

def follow(request: HttpRequest) -> HttpResponse:
    """ Follows given subreddit. If 5 subreddits already being followed,
        removes oldest followed subreddit.

    Args:
        request (HttpRequest)

    Returns:
        HttpResponse: Status of request
    """
    # Only POST requests handled by this endpoint
    if request.method == "POST":

        follow_form = FollowSubredditForm(request.POST)

        if follow_form.is_valid():
            # Check if subreddit limit has been reached. If so, 
            # evict oldest followed subreddit.
            follow_count = Subreddit.objects.count()
            if follow_count == 5:
                evict_oldest_subreddit()

            # Create Subreddit object from Subreddit ModelForm
            follow_form.save()

            # Display index page
            return redirect(reverse('login'))
        else:
            messages.error(request, "Invalid form data")

    # If not a POST request, create a new blank form
    else:
        return redirect(reverse('login'))