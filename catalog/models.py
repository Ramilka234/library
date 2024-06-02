from django.db import models

# Create your models here.

from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower

class Genre(models.Model):

    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)",
        verbose_name='Название'
    )

    def __str__(self):

        return self.name

    def get_absolute_url(self):

        return reverse('genre-detail', args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='genre_name_case_insensitive_unique',
                violation_error_message = "Genre already exists (case insensitive match)"
            ),
        ]

class Language(models.Model):

    name = models.CharField(max_length=200,
                            unique=True,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)",
                            verbose_name='Название')

    def get_absolute_url(self):

        return reverse('language-detail', args=[str(self.id)])

    def __str__(self):

        return self.name

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='language_name_case_insensitive_unique',
                violation_error_message = "Language already exists (case insensitive match)"
            ),
        ]

class Book(models.Model):

    title = models.CharField(max_length=200, verbose_name='Название')
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True, verbose_name='Автор')

    summary = models.TextField(
        max_length=1000, help_text="Напишите описание книги", verbose_name='Описание')
    isbn = models.CharField('ISBN', max_length=13,
                            unique=True,
                            help_text='13 Символов <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN номера</a>')
    genre = models.ManyToManyField(
        Genre, help_text="Выберите жанр для книги")

    language = models.ForeignKey(
        'Language', on_delete=models.SET_NULL, null=True, verbose_name='язык')

    class Meta:
        ordering = ['title', 'author']

    def display_genre(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def get_absolute_url(self):

        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):

        return self.title


import uuid
from datetime import date

from django.conf import settings


class BookInstance(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True, verbose_name='Книга')
    imprint = models.CharField(max_length=200, verbose_name='Печать')
    due_back = models.DateField(null=True, blank=True, verbose_name='Дата возврата')
    borrower = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='заемщик')

    @property
    def is_overdue(self):

        return bool(self.due_back and date.today() > self.due_back)

    LOAN_STATUS = (
        ('d', 'Обслуживание'),
        ('o', 'В долг'),
        ('a', 'Доступный'),
        ('r', 'Зарезервирован'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='d',
        help_text='Книга доступна')

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def get_absolute_url(self):

        return reverse('bookinstance-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.id} ({self.book.title})'


class Author(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):

        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'
