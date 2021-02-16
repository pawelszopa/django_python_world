from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.views.generic.base import TemplateResponseMixin, View

from courses.forms import ModuleFormsSet
from courses.models import Course


class CreateCourse(CreateView):
    model = Course
    fields = ['title', 'subject', 'slug', 'overview', 'course_image']
    template_name = 'courses/create_course.html'
    # permision mozna dodawac w panelu admina - ale tworzac model kazdy model ma 4 permision
    permission_required = 'courses.add_course'  # mozna edytowac czesc strony grupa moze miec czesc permision itp
    login_url = reverse_lazy('user:login')  # dlatego ze jak ktos zmieni config to nie trzeba bylo tyutaj mzmieniac
    raise_exceptions = True
    success_url = reverse_lazy('home')

    # wszczepienie uzytkownika
    def form_valid(self, form):
        form.instance.owner = self.request.user  # jak we flasku form.data
        print('------------------------------')
        print(form.cleaned_data)
        return super().form_valid(
            form)  # form valid musi zwracac http response, i jak nie chcemy to robumy super().form.valid(form)
        # oznacza to ze wywolujemy classe po ktorej dziedziczymy wywoujemy metode i obiekt


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'  # dane z modelu trafia pod nazwa object a tak to mamy course


class CourseUpdateView(UpdateView):
    template_name = 'courses/update_course.html'
    model = Course
    login_url = reverse_lazy('user:login')
    raise_exceptions = True
    context_object_name = 'course'
    permissions_required = 'courses.change_course'
    fields = ['title', 'subject', 'slug', 'overview', 'course_image']
    success_url = reverse_lazy('home')


class CourseDeleteView(DeleteView):
    model = Course
    permission_required = 'courses.delete_course'
    template_name = 'courses/delete_course.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('user:login')


class CourseModuleUpdateView(TemplateResponseMixin, View):
    # Mixin to klasa ktora moze dziedziczyc po innych klasach i ona zbiera kilka klas do siebie.
    template_name = 'courses/add_modules_course.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormsSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()  # tylko form na podsawie modela save w innym przypadku obj.create
            return redirect('home')
        return self.render_to_response({'course': self.course, 'formset': formset})
