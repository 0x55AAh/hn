### Installing

A step by step series of examples that tell you how to get a development env running

```
git clone git@github.com:0x55AAh/hn.git
```
```
cd hn
```
```
docker build .
```
```
docker-compose build
```
```
docker-compose up
```
Now we can log in http://127.0.0.1/admin
login: admin
password: admin

After that we can manually run startparser for fetching
and saving HackerNews posts.
```
docker-compose run --rm app python manage.py startparser
```

## Authors

* **Lysenko Vladimir**