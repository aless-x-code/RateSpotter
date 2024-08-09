# RateSpotter

RateSpotter is a full-stack web app that allows registered users to have a snapshot of their restaurant reviews from 3 different platforms (Yelp, Google, and TripAdvisor), all in one place.

It uses Flask as a web framework, MongoDB/Flask-login for user authentication and database, Docker for containerization, and Google cloud run for deployment to the server.


## Installation

1. Clone the repo:
   ```sh
   git clone https://github.com/username/repository.git

   # venv
   python3 -m venv venv
   source venv/bin/activate

   # requirements
   pip install -r requirments.txt

2. Enviorment variables
    <br>
    Create a .env file and store your enviorment variables
    ```sh
    # Flask
    FLASK_SECRET_KEY=

    # API
    tripadv_api_k=
    serp_api_k=

    # Database
    mongo_pw=
    mongo_user=

    auth_db=
    user_credentials=

3. Other setup

    <br>
    You will need to setup APIs, Google cloud, MongoDB, and Docker

## Local Deployment

    python3 main.py

## DEMO

<a href="https://www.youtube.com/watch?v=bSPoh7LoUU0" target="_blank">
  <img src="https://i.imgur.com/R4ttXrQ.png" alt="Watch the video" width="640" height="360">
</a>