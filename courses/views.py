from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from courses.models import Course


class CreateCourse(CreateView):
    model = Course
    fields = ['title', 'subject', 'slug', 'overview', 'course_image']
    template_name = 'courses/create_course.html'
    permission_required = 'courses.add_course'
    login_url = reverse_lazy('user:login')  # dlatego ze jak ktos zmieni config to nie trzeba bylo tyutaj mzmieniac
    raise_exceptions = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.owner = self.request.user  # jak we flasku form.data
        return super().form_valid(form)


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'  # dane z modelu trafia pod nazwa object a tak to mamy course
