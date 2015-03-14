
def add_permissions(user, permission_arrays):
    for permission_array in permission_arrays:
        for perm in permission_array:
            user.user_permissions.add(perm)
    user.save()


def delete_permissions(user, permission_arrays):
    for permission_array in permission_arrays:
        for perm in permission_array:
            user.user_permissions.remove(perm)
    user.save()


def add_group(user, group):
    user.groups.add(group)
    user.save()