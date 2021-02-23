from django.forms import inlineformset_factory

from courses.models import Course, Module

# factory tworzy rodzine obiektow
ModuleFormsSet = inlineformset_factory(
    Course,
    Module,
    fields=['title', 'description'],
    extra=2,
    can_delete=True)

# Formset zestaw formularzy na podstawie modeli
