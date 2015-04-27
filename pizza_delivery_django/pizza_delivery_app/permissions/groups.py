from django.contrib.auth.models import Group
from permissions import MENU_READ_PERMISSIONS, MENU_CHANGE_PERMISSIONS, VENUE_CRUD_PERMISSIONS

CHIEF_GROUP = Group.objects.get_or_create(name='chief')[0]
MANAGER_GROUP = Group.objects.get_or_create(name='manager')[0]
COOK_GROUP = Group.objects.get_or_create(name='cook')[0]