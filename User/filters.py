from django_filters import CharFilter, FilterSet, ChoiceFilter

from User.models import UserAccount
from _helpers.forms import CustomFiltersForm


class ProjectUsersFilter(FilterSet):
    is_moderator = ChoiceFilter(choices=((False, 'Normal User'), (True, 'Moderator')))
    projects = CharFilter(field_name='projects__project_name', lookup_expr='icontains')

    class Meta:
        model = UserAccount
        fields = {
            'username': ['icontains'],
            'email': ['icontains'],
            'first_name': ['icontains'],
            'last_name': ['icontains'],
            'salary_num': ['icontains'],
            'last_login': ['exact'],
            'is_moderator': ['exact'],
        }
        form = CustomFiltersForm
