from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


GROUPS = {
    "TeamLead":{
        "user" : ["add","delete","change","view"],
        "document": ["view"]
    },
    "HR":{
        "user" : ["add","delete","change","view"],
        "document": ["add","delete","change","view"]
    }
}

class Command(BaseCommand):
    help = "Create groups"

    def handle(self, *args, **options):
        for group_name in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group_name)

            for app_model in GROUPS[group_name]:
                for permission_name in GROUPS[group_name][app_model]:
                    name = "Can {} {}".format(permission_name, app_model)

                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except Permission.DoesNotExist:
                        continue

                    new_group.permissions.add(model_add_perm)

                    self.stdout.write("Adding {} to {}".format(model_add_perm,new_group))