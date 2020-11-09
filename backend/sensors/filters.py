from dry_rest_permissions.generics import DRYPermissionFiltersBase


class SensorFilterBackend(DRYPermissionFiltersBase):
    action_routing = True

    def filter_list_queryset(self, request, queryset, view):
        if not request.user.is_superuser:
            queryset = queryset.filter(owner=request.user)
        return queryset

    def filter_my_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)


class SpeedRecordFilterBackend(DRYPermissionFiltersBase):
    action_routing = True

    def filter_list_queryset(self, request, queryset, view):
        if not request.user.is_superuser:
            queryset = queryset.filter(sensor__owner=request.user)
        return queryset
