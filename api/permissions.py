from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    ''' Allow user to edit their own profile '''
    def has_object_permission(self, request, view, obj):
        '''Check user has permission to edit their own profile'''
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id

class UpdateOwnSatus(permissions.BasePermission):
    ''' Allow user to update their own satuts '''
    def has_object_permission(self, request, view, obj):
        ''' Check user has permission to edit their own status '''
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_profile.id == request.user.id

class SalesOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        print(view)
        if request.user.groups.filter(name="Sales").exists() and request.method in ['GET', 'POST']:
            return True
        return False