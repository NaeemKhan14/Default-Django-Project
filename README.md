# Default Django Project

This is a Django project skeleton with essential tools installed for quick set up. It has bootstrap 5.1.3, HTMX, Google Material Icons, MDB bootstrap and font-awesome all installed for local hosting. All the required libraries to run these frameworks in the `base_template.html`. It also comes with `django-filters`, `django_view_breadcrumbs` and `crispyforms`.

A basic custom login system is already in place with its login, password-reset, password confirm token (with default email backend), and password change form, all fully functional and designed.

# Installation
- Clone the repository or download it as a .zip file.
- Add the following environmental variables:
  - ***secret_key*** : Secret key of the project. Value must be a long random string. [Can be generated from here.](https://djecrety.ir/)
  - ***db_user*** : PostgreSQL username.
  - ***db_pass*** : PostgreSQL password.
  - ***db_host*** : PostgreSQL host, most likely `localhost` or `127.0.0.1` if working on a local machine.
  - ***db_name*** : Database name under PostgreSQL.
  - ***db_port*** : Database port (default 5432).
  - ***DJANGO_DEVELOPMENT*** : Set to `True` to set `DEBUG = True`. In production, set this value to `False`.

- Install the required libraries using `pip install -r .\requirements\dev.txt` if working under development environment, or `pip install -r requirements.txt` if in production environment.
