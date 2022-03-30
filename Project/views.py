from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView

from Project.forms import CreateProjectForm


class CreateProject(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = CreateProjectForm
    success_message = 'Project created successfully'
    success_url = None

    def get_success_url(self):
        return reverse('management')

    def form_valid(self, form):
        saved_data = form.save()
        saved_data.project_admin.add(self.request.user)
        saved_data.users.add(self.request.user)
        return super(CreateProject, self).form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            messages.error(self.request, '{}'.format(''.join(errors)))

        return redirect(reverse('management'))
