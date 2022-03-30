from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Row, Layout, Submit
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse

from Project.models import Project


class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'username'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'password'}
    ))


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'john.doe@example.com', 'type': 'email', 'name': 'email',
               'id': 'email', }))


class ChangePasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    new_password1 = forms.CharField(label='Password', required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'new_password1'}
    ))

    new_password2 = forms.CharField(label='Confirm Password', required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'new_password2'}
    ))


class ProfileChangePasswordForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(ProfileChangePasswordForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'needs-validation'
        self.helper.layout = Layout(
            Row(
                Column(FloatingField('old_password')),
            ),
            Row(

                Column(FloatingField('new_password1')),
            ),
            Row(
                Column(FloatingField('new_password2')),
            ),
            Row(
                Column(FormActions(Submit('change_password', 'Change Password'))),
            ),
        )


class CreateUserForm(forms.ModelForm):
    first_name = forms.CharField(label='Name')
    last_name = forms.CharField(label='Surname')
    salary_num = forms.CharField(label='Salary Number')
    password2 = forms.CharField(required=True, label='Confirm Password',
                                widget=forms.PasswordInput(attrs={'id': 'password'}))
    departments = forms.ModelChoiceField(required=True, queryset=Group.objects.all())
    is_moderator = forms.BooleanField(required=False, label='User is Moderator', widget=forms.CheckboxInput())

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'is_moderator', 'salary_num')
        widgets = {'password': forms.PasswordInput(), }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')

        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        project_choices = [(x.project_code, x.project_name) for x in user.project_admin.all()]
        self.fields['projects'] = forms.MultipleChoiceField(required=True, choices=project_choices)
        group_choices = [(x.pk, x.name) for x in Group.objects.all()]
        self.fields['departments'] = forms.MultipleChoiceField(required=True, choices=group_choices)
        self.helper.form_method = 'post'
        self.helper.form_class = 'needs-validation'
        self.helper.form_action = reverse('create_new_user')
        self.helper.layout = Layout(
            Row(
                Column(FloatingField('username')),
                Column(FloatingField('email')),
                Column(FloatingField('salary_num')),
            ),
            Row(
                Column(FloatingField('password')),
                Column(FloatingField('password2')),
            ),

            Row(
                Column(FloatingField('first_name')),
                Column(FloatingField('last_name')),
            ),
            Row(
                Column(FloatingField('projects', css_class='h-100'), css_class='h-100'),
                Column(FloatingField('departments', css_class='h-100'), css_class='h-100'),
            ),
            Row(
                Column('is_moderator', css_class='text-start'),
            ),
            Row(
                Column(FormActions(Submit('submit', 'Add New User'))),
            ),
        )


class ProjectRemoveUserForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        admin = kwargs.pop('admin')

        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['project'] = forms.ModelChoiceField(label='Project', required=True,
                                                        queryset=user.project_users.filter(project_admin=admin).distinct())
        self.helper.form_class = 'needs-validation'
        self.helper.layout = Layout(
            Row(
                Column(FloatingField('project')),
            ),
        )
