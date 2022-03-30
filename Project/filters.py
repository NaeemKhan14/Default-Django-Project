import django_filters
from django_filters import FilterSet
from _helpers.forms import CustomFiltersForm

from Project.models import Project


class ProjectsFilter(FilterSet):
    project_admin = django_filters.CharFilter(field_name='project_admin__username', lookup_expr='exact')

    class Meta:
        model = Project
        fields = {
            'project_code': ['icontains'],
            'project_name': ['icontains'],
            'project_desc': ['icontains'],
            'geo_area': ['icontains'],
        }
        form = CustomFiltersForm
