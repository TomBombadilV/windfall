# Windfall Take Home Assessment

## Assumptions

## High Level Approach

## Technology Used
- Django 3.1 + Python 3.6
- SQLite
- HTML + CSS + Bootstrap

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
    And the Appointment form is in this one:
    ```
    /app/takehome/forms.py
    ```
4. Open the application in your browser
    ```
    open http://localhost:8000/takehome
    ```

## Moving Forward
