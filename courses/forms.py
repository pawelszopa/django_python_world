from django.forms import inlineformset_factory

from courses.models import Course, Module
# factory tworzy rodzine obiektow
ModuleFormsSet = inlineformset_factory(
    Course,
    Module,
    field=['title', 'description'],
    extra=2,
    can_delete=True)