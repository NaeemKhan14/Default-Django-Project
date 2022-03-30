from django import template

register = template.Library()


@register.filter
def reset_filter_btn(url):
    """
    Shows the reset filter button when there are pagination or filter parameters
    present in the url.

    :param url: request.GET obj
    :return: True if pagination or filter in url, else False
    """
    return True if url.GET or url.resolver_match.kwargs else False


@register.filter
def make_sort_col(url, col_name):
    """
    Read the url parameters and creates table class for the column either
    ascending or descending. Also creates the URL for the sort button depending
    on the value found in url parameter.

    :param url: kwargs containing URL parameters
    :param col_name: make of the column that is going to be sorted
    :return: list [css class name, 'sort=col_name']
    """
    # If url is not empty and has 'sort' keyword in it

    if url and 'sort' in url:
        param = url['sort']  # parameter is always going to be '?sort=keyword'
        # If the parameter's name is same as the given col name or col_name starting
        # from index 1 instead of 0. This is to prevent other columns from changing
        # their style when once button is clicked.
        if col_name == param or col_name == param[1:]:
            # If the first letter is -, it means it's in descending order, and we show
            # the descending btn and change the value of sort button.
            if param[0] == '-':
                return ['orderable desc', 'sort=%s' % col_name]
            # Otherwise sort is called, and table is in ascending order.
            return ['orderable asc', 'sort=-%s' % col_name]
    # This is the general case of when the page is loaded and no sort filter is requested.
    return ['orderable', 'sort=%s' % col_name]


@register.filter
def get_sort_url(url):
    return url.split('sort', 1)[0]


@register.filter
def process_null_value(val):
    return '-' if not val or val is None else val


@register.filter
def get_reset_url(url):
    return url.path.split('/')[2]


@register.filter
def get_user_projects(user):
    """
    Takes a user instance and gets all their projects
    """
    return user.project_users.all()
