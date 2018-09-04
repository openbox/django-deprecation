from django.db import models
from django_deprecation import DeprecatedField


class WarnFunction(object):
    def __init__(self):
        self.reset()

    def __call__(self, message):
        self.message = message
        self.counter += 1

    def reset(self):
        self.message = ''
        self.counter = 0


warn_function = WarnFunction()
DeprecatedField.warn = warn_function


class Musician(models.Model):
    name = models.CharField(max_length=50)
    title = DeprecatedField('name')

    def __str__(self):
        return self.name


class Album(models.Model):
    artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
    musician = DeprecatedField('artist')

    def __str__(self):
        return self.artist and self.artist.name
