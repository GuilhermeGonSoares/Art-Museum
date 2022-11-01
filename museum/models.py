
from django.contrib.auth.models import User
from django.db import models


#pintura -> ManyToMany -> autor
class Author(models.Model):
    name = models.CharField(max_length=50)
    biography = models.TextField(blank=True)
    is_engraving = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.name

# igreja -> OneToMany -> pintura
# pintura -> ManyToOne -> igreja 
# Uma igreja pode possuir mais de uma pintura()
class Church(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)

    def __str__(self) -> str:
        return self.name

class Engraving(models.Model):
    name = models.CharField(max_length=50)
    book = models.CharField(max_length=50, blank=True)
    cover = models.ImageField(upload_to='engravings/cover/%Y/%m/%d/')
    
    author = models.ManyToManyField(
        Author, blank=True, default=None
    )

    def __str__(self) -> str:
        return self.name


class Painting(models.Model):
    name = models.CharField(max_length=50)
    date = models.CharField(max_length=10, null=True, blank=True)
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to='museum/cover/%Y/%m/%d/')
    post_date = models.DateField(auto_now=True)
    summary = models.CharField(max_length=250)
    is_published = models.BooleanField(default=False)

    author = models.ManyToManyField(
        Author, blank=True,
        default=None
    )

    church = models.ForeignKey(
        Church, on_delete=models.SET_NULL, null=True, blank=True,
        default=None
    )

    engraving = models.ManyToManyField(
        Engraving, blank=True,
        default=None
    )

    post_author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )

    def __str__(self) -> str:
        return self.name
    