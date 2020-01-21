### Installing

A step by step series of examples that tell you how to get a development env running.

First of all clone the project to any directory:
```
git clone https://github.com/0x55AAh/hn.git
```
Now cd to home of the project:
```
cd hn
```
Next run docker builders:
```
docker build .
docker-compose build
docker-compose up
```
Now we can log in http://127.0.0.1/admin:
* **login**: admin
* **password**: admin

After that we can manually run startparser for fetching
and saving HackerNews posts.
```
docker-compose run --rm app python manage.py startparser
```
In case of need for periodical running the script, we can
create cron task or even celery task.

For manual testing run this:
```
docker-compose run --rm app python manage.py test posts
```
Public server:
* http://185.65.246.204:8000