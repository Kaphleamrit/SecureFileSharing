user_roles = {
    'admin': ['upload', 'download', 'manage'],
    'user': ['download']
}

def check_permission(role, action):
    return action in user_roles.get(role, [])
