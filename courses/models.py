from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.loader import render_to_string
from django.utils.text import slugify

from courses.fields import OrderField


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # db trigger
        if not self.slug:
            self.slug = slugify(self.title)
            super(Subject, self).save(*args, **kwargs)
            # przekazujemy instancje klasy i obiekt, bardziej explisity polimorfism


class Course(models.Model):
    owner = models.ForeignKey(get_user_model(),
                              related_name='courses_created',
                              on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    # text field bo kilka linijek
    created = models.DateTimeField(auto_now_add=True)
    # relacja wiele do wielu
    students = models.ManyToManyField(get_user_model(),
                                      related_name='courses_joined',
                                      blank=True)  # blannk inicjalizuje to nie jest ten sam blank co w texfield
    course_image = models.ImageField(upload_to='images')

    class Meta:
        # - created jako descenging
        ordering = ['-created']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # db trigger
        if not self.slug:
            self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)


class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    def __str__(self):
        return f'{self.order}. {self.title}'

    class Meta:
        ordering = ['order']


class Content(models.Model):
    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE)
    # Content Type ! important read in doc what i s COntent Type
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': (
                                         'text',
                                         'video',
                                         'image',
                                         'file'
                                     )})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')  # pozwala na relacje do kilku
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    owner = models.ForeignKey(get_user_model(),
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    # %(class)s_related podmienia w klasach ktore dziedzicza to zmiane wiec w file bedzie Files_related
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        return render_to_string(f'courses/content/{self._meta.model_name}.html', {'item': self})


class File(ItemBase):
    content = models.FileField(upload_to='files')


class Image(ItemBase):
    content = models.ImageField(upload_to='content_images')


class Text(ItemBase):
    content = models.TextField()


class Video(ItemBase):
    content = models.URLField()
