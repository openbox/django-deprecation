# django-deprecation

Deprecate django fields and make migrations without breaking existing code.


## Install

```bash
pip install django-deprecation
```


## Usage

Let's suppose we have the following models:

```py
from django.db import models


class Musician(models.Model):
    name = models.CharField(max_length=50)


class Album(models.Model):
    musician = models.ForeignKey(Musician, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
```


Now, for some reason, let's suppose we want to rename the field `Album#musician` to `Album#artist`.

So we make the migration using the
[RenameField](https://docs.djangoproject.com/en/1.11/ref/migration-operations/#renamefield)
operation. The problem is that any existing code that used the old field would break.

We could create a property as an alias:

```py
class Album(models.Model):
    artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    @property
    def musician(self):
        return self.artist

    @musician.setter
    def musician(self, value):
        self.artist = value
```

But any code using
[QuerySet#filter](https://docs.djangoproject.com/en/2.0/ref/models/querysets/#filter)
would break if it uses the `musician` field.

This is where `django-deprecation` comes handy.
We set the `musician` field as a `DeprecatedField` and point it to the `artist` field:

```py
from django_deprecation import DeprecatedField


class Album(models.Model):
    artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
    musician = DeprecatedField('artist')
    name = models.CharField(max_length=100)
```


Now, the following code snippet will work:

```py
from .models import Album, Musician

album = Album.objects.first()
assert album.musician == album.artist

new_musician = Musician.objects.create(
    first_name='John',
    last_name='Doe',
    instrument='Guitar',
)
album.musician = new_musician
assert album.artist == new_musician

new_musician_album = Album.objects.filter(
    musician=new_musician,
).first()
new_artist_album = Album.objects.filter(
    artist=new_musician,
).first()
assert new_musician_album == new_artist_album
```

If you want to control how to report the error,
replace the `DeprecatedField.warn` function with a custom one:

```py
from django_deprecation import DeprecatedField


def warn_function(message):
    # do stuff
    import warnings
    warnings.warn(message, DeprecationWarning)


DeprecatedField.warn = warn_function
```
