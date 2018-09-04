import pytest

from .models import (
    Album,
    Musician,
    warn_function,
)


@pytest.fixture
def warn():
    warn_function.reset()
    return warn_function


@pytest.mark.django_db
def test_should_return_the_same_value_as_the_aliased_field():
    musician = Musician.objects.create(name='foo')
    assert musician.title == musician.name


@pytest.mark.django_db
def test_should_set_value_to_the_aliased_field():
    musician = Musician.objects.create(name='foo')
    musician.title = 'bar'
    assert musician.name == 'bar'


@pytest.mark.django_db
def test_should_warn_when_accessing_it(warn):
    musician = Musician.objects.create(name='foo')
    assert warn.counter == 0
    assert musician.title
    assert warn.counter == 1


@pytest.mark.django_db
def test_should_warn_when_setting_it(warn):
    musician = Musician.objects.create(name='foo')
    assert warn.counter == 0
    musician.title = 'bar'
    assert warn.counter == 1


@pytest.mark.django_db
def test_should_warn_when_setting_it_while_creating(warn):
    Musician.objects.create(title='foo')
    assert warn.counter == 1


@pytest.mark.django_db
def test_should_work_as_a_filter_parameter_when_aliased_field_is_a_char_field():
    musician = Musician.objects.create(name='foo')
    search_musician = Musician.objects.filter(title='foo').first()
    assert search_musician == musician


@pytest.mark.django_db
def test_should_work_as_a_filter_parameter_when_aliased_field_is_a_foreign_field():
    musician = Musician.objects.create(name='foo')
    album = Album.objects.create(artist=musician)
    search_album = Album.objects.filter(musician=musician).first()
    assert search_album == album
