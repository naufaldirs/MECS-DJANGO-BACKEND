from rest_framework.permissions import BasePermission, SAFE_METHODS


class HasGroup(BasePermission):
    group_name = None

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            self.group_name and
            request.user.groups.filter(name=self.group_name).exists()
        )


class IsAdmin(HasGroup):
    group_name = 'admin'


class IsPPC(HasGroup):
    group_name = 'ppc'


class IsOperator(HasGroup):
    group_name = 'operator'


class IsLeader(HasGroup):
    group_name = 'leader'


class IsSupervisor(HasGroup):
    group_name = 'supervisor'


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsPPCOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return (
            request.user.is_authenticated and
            request.user.groups.filter(name='ppc').exists()
        )


class IsLeaderOrSupervisor(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.groups.filter(
                name__in=['leader', 'supervisor']
            ).exists()
        )
class IsLeaderOrSupervisorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return (
            request.user.is_authenticated and
            request.user.groups.filter(
                name__in=['leader', 'supervisor']
            ).exists()
        )