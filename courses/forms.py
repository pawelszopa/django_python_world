from django.forms import inlineformset_factory

from courses.models import Course, Module


ModuleFormsSet = inlineformset_factory(
    Course,
    Module,
    fields=['title', 'description'],
    extra=2,
    can_delete=True)


