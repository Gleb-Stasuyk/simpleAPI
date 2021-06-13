from django.db import models


class News(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return self.title


class Company(models.Model):
    company_name = models.CharField(max_length=100)
    bio = models.TextField()
    company_news = models.ManyToManyField(News, verbose_name='Новости компании', blank=True, null=True)

    def __str__(self):
        return f'Компания {self.company_name}'