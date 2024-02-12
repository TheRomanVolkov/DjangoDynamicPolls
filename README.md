# Django Dynamic Polls Application

This project is a Django-based web application for creating and conducting dynamic polls where questions can branch based on previous answers.

## Features

* Create polls with branching logic.
* Conduct polls with dynamic navigation through questions based on user responses.
* View results with detailed statistics for each poll.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/TheRomanVolkov/DjangoDynamicPolls.git
   ```
2. Navigate into the project directory:
   ```
   cd DjangoDynamicPolls
   ```
3. Install the requirements:
   ```
   pip install -r requirements.txt
   ```
4. Run migrations to create database schema:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

## Running the Application

1. Start the Django development server:
   ```
   python manage.py runserver
   ```
2. Open a web browser and navigate to `http://127.0.0.1:8000/polls/` to start taking polls.


