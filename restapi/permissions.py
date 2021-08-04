from rest_framework.permissions import BasePermission

class SalesOnly(BasePermission):
    def has_permission(self, request, view):
        print(view)
        if request.user.groups.filter(name="Sales").exists() and request.method in ['GET', 'POST']:
            return True
        return False