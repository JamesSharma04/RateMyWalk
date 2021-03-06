# WAD2 - Team 8F - RateMyWalk

## External Sources Used

* [Authentication](https://github.com/django/django/tree/main/django/contrib/admin/templates/registration)

* [Bootstrap](https://getbootstrap.com/)

* [Feather Icons](https://feathericons.com/)

* [Bing Search API](https://docs.microsoft.com/en-us/azure/cognitive-services/bing-web-search/)

* [Django Documentation](https://docs.djangoproject.com/en/2.2/)

## Installation

* Python 3.7+ and Git must be installed and added to PATH, then:
```term
$ git clone  https://github.com/JamesSharma04/RateMyWalk
```
Then install the dependences:
```term
$ python -m pip install -r requirements.txt --user
```
In order to run our application fully, a bing search key is required. 

## Execution

Database stuff:
```term
$ python manage.py makemigrations rate_my_walk
```
```term
$ python manage.py migrate
```
Set up initial data:
```term
$ python populate_RateMyWalk.py
```

Browse to `https://127.0.0.1:8000/` and then type:
```term
$ python manage.py runserver
```

## Tests

```term
$ python manage.py test rate_my_walk
```
 
