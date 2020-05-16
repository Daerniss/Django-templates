from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField
from model_utils.models import TimeStampedModel
from model_utils import Choices


class Article(TimeStampedModel):
    slug = models.SlugField()
    title = models.CharField(_('Title'), max_length=100)
    content = RichTextField(_('Content'))
    image = models.ImageField(_('Image'), null=True, blank=True)

    class Meta:
        ordering = ['slug']
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('flatpages:article', kwargs={'slug': self.slug})


class FlatPage(TimeStampedModel):
    slug = models.SlugField()
    title = models.CharField(_('Title'), max_length=100)
    content = RichTextField(_('Content'))

    class Meta:
        ordering = ['slug']
        verbose_name = _('Flat Page')
        verbose_name_plural = _('Flat Pages')

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('flatpages:flatpage', kwargs={'slug': self.slug})


class SupportCenterCategory(models.Model):
    slug = models.SlugField()
    title = models.CharField(_('Title'), max_length=100)

    class Meta:
        ordering = ['slug']
        verbose_name = _('Support Center')
        verbose_name_plural = _('Support Center')

    def __str__(self):
        return self.title


class SupportCenterElement(models.Model):
    category = models.ForeignKey(
        'SupportCenterCategory', on_delete=models.CASCADE, related_name='elements', related_query_name='element'
    )
    question = RichTextField(_('Question content'))
    answer = RichTextField(_('Answer text'))
    order = models.PositiveSmallIntegerField(_('Order'))

    class Meta:
        ordering = ('category', 'order')
        verbose_name = _('Support Center Element')
        verbose_name_plural = _('Support Center Elements')


class ContactUsRequest(TimeStampedModel):
    CATEGORIES = Choices(
        ('questions', _('Questions')),
        ('suggestions', _('Suggestions'))
    )
    email = models.EmailField(_('Email'))
    title = models.CharField(_('Title'), max_length=250)
    category = models.CharField(_('Category'), max_length=250, choices=CATEGORIES)
    description = models.TextField(_('Description'))

    class Meta:
        ordering = ['id']
        verbose_name = _('Contact Us Request')
        verbose_name_plural = _('Contact Us Requests')

    def __str__(self):
        return f'Request {self.id} by {self.email}'
