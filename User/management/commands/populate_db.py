from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError
from django.utils.datetime_safe import datetime


class Command(BaseCommand):
    help = 'Creates initial database entries'

    def handle(self, *args, **options):

        # Create groups
        groups_list = ['Materials  Department', 'Engineering Department',
                       'Quality Control Department', 'Construction Team']
        for group in groups_list:
            try:
                Group.objects.get(name=group)
                self.stdout.write(self.style.ERROR('Group %s already exists' % group))
            except Group.DoesNotExist:
                Group.objects.create(name=group)
                self.stdout.write(self.style.SUCCESS('Group %s created.' % group))
