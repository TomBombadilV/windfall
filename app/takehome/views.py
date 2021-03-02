import json, urllib.request, time, typing

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import FollowSubredditForm
from .models import Subreddit

# Define JSON type for type hints
JSONType = typing.Union[str,\
                        int,\
                        float,\
                        bool,\
                        None,\
                        typing.Dict[str, typing.Any],\
                        typing.List[typing.Any]]

def get_subreddit_names() -> [str]:
    """ Retrieves list of all subreddit names that are currently being followed

    Returns:
        [str]: List of subreddit names as strings
    """
    subreddits = Subreddit.objects.all()
    subreddit_names = [subreddit.name for subreddit in subreddits]
    return subreddit_names

def check_valid_subreddit(subreddit_name: str) -> bool:
    """ Takes a subreddit name as a string and checks if it is a subreddit that
        actually exists.

    Args:
        subreddit_name (str): Potential subreddit name

    Returns:
        bool: Whether that subreddit exists or not
    """
    # Define custom user agent to avoid triggering 429 error
    header = {'User-Agent': 'lightweight reddit feed for Windfall take-home'}

    # Define subreddit URL
    url_str = "http://reddit.com/r/" + subreddit_name

    # Create and open request
    request = urllib.request.Request(url_str, data=None, headers=header)
    try:
        urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:
        print('URLError: {0}'.format(e.reason))
        return False
    else:
        return True

def retrieve_subreddit_as_json(subreddit_name: str) -> JSONType:
    """ Takes a subreddit name, constructs the desired URL, and retrieves JSON from
        URL.

    Args:
        subreddit_name (str): Subreddit's name

    Returns:
        JSONType: Dictionary of JSON data from given subreddit
    """
    # Define custom user agent to avoid triggering 429 error
    header = {'User-Agent': 'lightweight reddit feed for Windfall take-home'}

    # Get subreddit's top post of all time
    url_str = "http://reddit.com/r/" + subreddit_name + "/top/.json?t=all&limit=1"

    # Create and open request
    request = urllib.request.Request(url_str, data=None, headers=header)
    try:
        data = urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:
        print('URLError: {0}'.format(e.reason))
        return {}
    else:
        # Decode data and parse as JSON
        json_data = json.loads(data.read().decode('utf-8'))
        # Parse JSON for most relevant information
        return parse_json_data(json_data)

def parse_json_data(json_data: JSONType) -> JSONType:
    """ Takes a JSON object of subreddit's data and returns a dictionary of 
        relevant information:
        - Subreddit name
        - Post title
        - Post URL
        - Post score (upvotes + downvotes)
        As long as the post has a title, we will display it. If it is missing
        any of the other fields, we'll simply leave that field blank.

    Args:
        subreddit_data (JSONType): JSON object of post information

    Returns:
        JSONType: Relevant post information
    """
    # Validate JSON 
    if 'data' in json_data and\
        'children' in json_data['data'] and\
        json_data['data']['children'] and\
        'data' in json_data['data']['children'][0] and\
        'title' in json_data['data']['children'][0]['data']:
        
        # Save top post "child"
        post = json_data['data']['children'][0]['data']

        # Convert epoch time to datetime
        epoch_time = post['created_utc']  if 'created_utc' in post else 0
        readable_time = time.strftime('%b %d, %Y %I:%M %p', time.localtime(epoch_time))

        # Get title, timestamp, and number of likes
        post_info = {
            'subreddit':    post['subreddit'] if 'subreddit' in post else '',
            'title':        post['title'] if 'title' in post else '',
            'url':          post['url']  if 'url' in post else '',
            'score':        post['score']  if 'score' in post else '',
            'created_utc':  readable_time
        }

        return post_info
    # If invalid JSON data, return empty dictionary
    else:
        return {}

def index(request: HttpRequest) -> HttpResponse:
    """[summary]

    Args:
        request ([type]): [description]

    Returns:
        HttpResponse: [description]
    """
    # Get list of names and count of all subreddits currently being followed
    subreddit_names = get_subreddit_names()
    subreddit_count = len(subreddit_names)

    # Retrieve top post for each subreddit
    top_posts = []

    for name in subreddit_names:
        top_posts.append(retrieve_subreddit_as_json(name))
    
    # Sort posts by vote count (highest score first)
    top_posts = sorted(top_posts, key=lambda k: k['score'], reverse=True) 

    context = {
        'subreddit_form': FollowSubredditForm(),
        'subreddit_count': subreddit_count,
        'top_posts': top_posts
    }
    return render(request, 'takehome/index.html', context)

def evict_oldest_subreddit() -> None:
    """ Evicts the oldest subreddit followed """
    oldest_subreddit = Subreddit.objects.earliest('date_followed')
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
            # Create object from form data
            req_subreddit = follow_form.save(commit=False)
            req_subreddit_name = req_subreddit.name

            # Check that it is a valid subreddit
            if not check_valid_subreddit(req_subreddit_name):
                return redirect(reverse('index'))

            # Check that subreddit is not already being followed
            followed_subreddit = Subreddit.objects.filter(name=req_subreddit_name)
            if followed_subreddit:
                return redirect(reverse('index'))

            # Check if subreddit limit has been reached. If so, 
            # evict oldest followed subreddit.
            follow_count = Subreddit.objects.count()
            if follow_count == 5:
                evict_oldest_subreddit()

            # Save Subreddit object
            req_subreddit.save()

            # Display index page
            return redirect(reverse('index'))
        else:
            messages.error(request, "Invalid form data")

    # If not a POST request, create a new blank form
    else:
        return redirect(reverse('index'))