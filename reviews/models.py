from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Publisher(models.Model):
    name = models.CharField(max_length=50, help_text="The name of the Publisher.")
    website = models.URLField(help_text="The Publisher's website.")
    email = models.EmailField(help_text="The Publisher's email address.")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=70, help_text="The title of the book.")
    publication_date = models.DateField(verbose_name="Date the book was published.")
    isbn = models.CharField(max_length=20, verbose_name="ISBN number of the book.")
    cover = models.ImageField(null=True, blank=True, upload_to='book_covers')
    sample = models.FileField(null=True, blank=True, upload_to='book_sample')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    contributors = models.ManyToManyField('Contributor', through='BookContributor')
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk': self.pk})


class Contributor(models.Model):
    first_names = models.CharField(max_length=50, help_text="The Contributor's first name or names.")
    last_names = models.CharField(max_length=50, help_text="The Contributor's last name or names.")
    email = models.EmailField(help_text="The contact email for the contributor.")

    def __str__(self):
        return self.first_names

    def number_contributions(self):
        return self.bookcontributor_set.count()


class BookContributor(models.Model):
    class ContributionRole(models.TextChoices):
        AUTHOR = "AUTHOR", "Author"
        CO_AUTHOR = "CO_AUTHOR", "Co-Author"
        EDITOR = "EDITOR", "Editor"

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    role = models.CharField(verbose_name="The role this contributor had in the book.",
                            choices=ContributionRole.choices, max_length=20)


class Review(models.Model):
    content = models.TextField(help_text="The Review text.")
    rating = models.IntegerField(help_text="The rating the reviewer has given")
    date_created = models.DateTimeField(auto_now_add=True,
                                        help_text="The Date and Time the review was created.")
    date_edited = models.DateTimeField(null=True, help_text="The date and time the review was last edited.")
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE,
                             help_text="The Book that this review is for")