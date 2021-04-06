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
$ python3 -m pip install -r requirements.txt --user
```

## Execution

Set up initial data
```term
$ python populate_RateMyWalk.py
```

Browse to `http://localhost:8000` and then type:
```term
$ python manage.py runserver
```

## Tests

```term
$ python manage.py test rate_my_walk
```
 
