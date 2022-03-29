from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from view_breadcrumbs import BaseBreadcrumbMixin


class Dashboard(LoginRequiredMixin, BaseBreadcrumbMixin, TemplateView):
    template_name = 'partials/base_template.html'
    crumbs = [("Dashboard", '')]
