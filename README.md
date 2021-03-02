# Windfall Take Home Assessment
A full-stack web application that supports the following functionality:
- Only need to support one user
- User's Reddit feed should start empty
- User can "follow" new subreddit by typing subreddit name into text box
- User's Reddit feed should only contain the top post for each followed subreddit
- Posts in feed should be sorted by "score"
- Posts in feed should link to actual Reddit post
- A maximum of 5 subreddits can be followed at any given time. The oldest followed subreddit is removed as count goes above 5.

## Assumptions
1. Re-following a subreddit that you already follow does not update its "follow" timestamp.
2. Entering a string that is not a valid subreddit will do nothing.

## High Level Approach
1. Have model for Subreddit so that subreddits followed by user can persist. If a Subreddit object exists for a given subreddit, that means that the user is currently following that subreddit.
2. A "follow" action triggers the following actions:
    - Check how many subreddits the user is currently following (the number of Subreddit objects). If there are 5, evict (delete) the oldest one.
    - Create a new Subreddit object with the given subreddit name and current timestamp


## Technology Used
- Django 3.1 + Python 3.6
- SQLite
- HTML + CSS

## Usage
1. Have Docker installed [https://www.docker.com/](https://www.docker.com/)
2. Clone this repository
    ```
    git clone https://github.com/TomBombadilV/windfall.git
    ```
2. In the project's root directory, build the image (this may take a few minutes)
    ```
    docker-compose build
    ```
3. Run the image
    ```
    docker-compose run
    ```
4. All business logic can be found in this file:
    ```
    /app/takehome/views.py
    ```
    Database schemas are in this one:
    ```
    /app/takehome/models.py
    ```
    The forms are in this one:
    ```
    /app/takehome/forms.py
    ```
    And the index.html template is here:
    ```
    /app/takehome/templates/takehome/index.html
    ```
4. Open the application in your browser
    ```
    open http://localhost:8000/takehome
    ```

## Moving Forward
Moving forward, I would add images to top posts as well as the functionality to close out a post, and I'd also make the interface more responsive, since I did not have enough time to do so. I'd also add thorough tests and more comprehensive error handling of different cases.

Additionally, I would expand on this project with the following features:
- Allow the user to follow an infinite amount of subreddits
- Display paginated results instead of restricting number of displayed results
- Introduce caching to improve latency when fetching posts from subreddits, as well as reduce need to retrieve all subreddits' top posts on every page refresh. This is especially true because most subreddits' top post of all time will likely not change very often
- Use more effective error messages with various erroneous behaviors (entering invalid subreddit, entering subreddit with no posts, etc.)
- Introduce more stringent checks for the subreddit input form
- Use AJAX for smoother user experience