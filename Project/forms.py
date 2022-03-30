from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms
from django.urls import reverse

from .models import Project


class CreateProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        exclude = ['users', 'project_admin']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'needs-validation'
        self.helper.form_action = reverse('create_project')
        self.helper.layout = Layout(
            Row(
                Column(FloatingField('project_code')),
                Column(FloatingField('project_name')),
                Column(FloatingField('geo_area')),
            ),
            Row(
                Column(FloatingField('project_desc')),
            ),
            Row(
                Column(FormActions(Submit('create', 'Create Project')))
            ),
        )
