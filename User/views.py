from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic.edit import FormMixin, DeleteView
from django_filters.views import FilterView
from view_breadcrumbs import BaseBreadcrumbMixin

from Project.forms import CreateProjectForm
from Project.models import Project
from User.filters import ProjectUsersFilter
from User.forms import CreateUserForm, ProjectRemoveUserForm
from User.models import UserAccount


class CreateNewUser(LoginRequiredMixin, CreateView):
    form_class = CreateUserForm

    def get_form_kwargs(self):
        """
        Passes the required url parameter to the form (request.user object)
        """
        kwargs = super(CreateNewUser, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    # Redirect to this page after success
    def get_success_url(self):
        return reverse('management')

    def form_valid(self, form):
        # If both password fields match
        if form.cleaned_data['password'] == form.cleaned_data['password2']:
            form.save(commit=False)
            form.instance.set_password(form.cleaned_data['password'])
            user = form.save()
            # Add user to projects list selected from the choice field
            for project in form.cleaned_data['projects']:
                try:
                    proj = Project.objects.get(project_code=project)
                    user.projects.add(proj)
                    proj.users.add(user)
                except Project.DoesNotExist:
                    messages.error(self.request, 'Could not add user to the {name} project'.format(name=project))
                    return redirect('users_management')

            # Add user to department list selected from the choice field
            for department in form.cleaned_data['departments']:
                try:
                    group = Group.objects.get(pk=department)
                    group.user_set.add(user)
                except Group.DoesNotExist:
                    messages.error(self.request, 'Could not add user to the {name} department'.format(name=department))
                    return redirect('users_management')
            # Add a success message when User and Group objects are created
            messages.success(request=self.request, message='User added successfully!')
            return super().form_valid(form)

        # If both password fields do not match
        else:
            messages.error(self.request, 'Passwords do not match')
            return redirect('management')

    def form_invalid(self, form):

        for field, errors in form.errors.items():
            messages.error(self.request, '{}'.format(''.join(errors)))

        return redirect('management')


class ManagementView(LoginRequiredMixin, BaseBreadcrumbMixin, FormMixin, FilterView):
    model = UserAccount
    filterset_class = ProjectUsersFilter
    template_name = 'management_page.html'
    form_class = CreateUserForm
    crumbs = [("Admin Management", '')]
    context_object_name = 'users'
    paginate_by = 10

    def get_form_kwargs(self):
        """
        Passes the required url parameter to the form (request.user object)
        """
        kwargs = super(ManagementView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_queryset(self):
        """
        Prepare queryset for the Django Filters.
        :return: QuerySet of PipelineSpecs model
        """
        order_by = 'username'
        if self.request.GET.get('sort'):
            order_by = self.request.GET.get('sort')
        u = UserAccount.objects.get(pk=1)

        query_set = UserAccount.objects.filter(projects__project_admin=self.request.user).order_by(order_by).exclude(
            username=self.request.user.username).distinct()

        filter = self.filterset_class(self.request.GET, query_set)
        return filter.qs

    def get_context_data(self, **kwargs):
        context = super(ManagementView, self).get_context_data(**kwargs)

        unwanted_cols = ['id', 'logentry', 'project_users', 'password', 'user_permissions', 'is_active', 'is_staff',
                         'is_admin', 'date_joined', 'is_superuser', 'groups', 'users', 'project_admin']
        columns_list = [f.name for f in UserAccount._meta.get_fields() if f.name not in unwanted_cols]
        columns_verbose_name = [UserAccount._meta.get_field(col).verbose_name.title() for col in columns_list]

        context['columns'] = zip(columns_list, columns_verbose_name)
        context['add_user_form'] = CreateUserForm(user=self.request.user)
        context['projects_list'] = Project.objects.all()
        context['add_projects_form'] = CreateProjectForm

        return context


class DeleteUser(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = UserAccount
    success_message = 'User removed from project'

    def get_success_url(self):
        return reverse('management')

    def get(self, request, *args, **kwargs):
        user = UserAccount.objects.get(pk=self.kwargs['pk'])
        user_obj = user.__dict__

        fields = ['Username', 'Email', 'First Name', 'Last Name', 'Salary Number', 'Last Login']
        data_obj = [[UserAccount._meta.get_field(x).verbose_name.title(), y] for x, y in
                    zip(user_obj.keys(), user_obj.values()) if
                    x != '_state' and UserAccount._meta.get_field(x).verbose_name.title() in fields]

        user_projects_form = ProjectRemoveUserForm(user=user, admin=self.request.user)

        return render(request, 'partials/htmx/delete_modal.html', {'data_obj': data_obj,
                                                                   'obj_id': user.id,
                                                                   'user_projects_form': user_projects_form,
                                                                   'user_projects': Project.objects.all(),
                                                                   'delete_url': reverse('delete_user',
                                                                                         args=[user.id])})

    def form_valid(self, form):
        project = Project.objects.get(pk=self.request.POST['project'])
        user = UserAccount.objects.get(pk=self.kwargs['pk'])
        project.users.remove(user)
        user.projects.remove(project)
        messages.success(self.request,
                         'Successfully removed {} from project: {}'.format(user.username, project.project_name))
        return redirect(reverse('management'))
