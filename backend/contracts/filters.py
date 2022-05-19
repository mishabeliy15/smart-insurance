from dry_rest_permissions.generics import DRYPermissionFiltersBase


class ContractFilterBackend(DRYPermissionFiltersBase):
    action_routing = True

    def filter_list_queryset(self, request, queryset, view):
        return queryset

    def filter_my_queryset(self, request, queryset, view):
        if request.user.DRIVER:
            queryset = queryset.filter(customer=request.user)
        else:
            queryset = queryset.filter(company__owner=request.user)
        return queryset

    def filter_my_detail_queryset(self, request, queryset, view):
        return self.filter_my_queryset(request, queryset, view)


class OfferFilterBackend(ContractFilterBackend):
    def filter_deny_queryset(self, request, queryset, view):
        if request.user.DRIVER:
            queryset = queryset.filter(customer=request.user)
        else:
            queryset = queryset.filter(company__owner=request.user)
        return queryset
