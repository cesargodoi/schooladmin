from django.urls import path
from .views import workgroup, membership

## workgroup
urlpatterns = [
    path("", workgroup.workgroup_home, name="workgroup_home"),
    path(
        "<int:pk>/detail/", workgroup.workgroup_detail, name="workgroup_detail"
    ),
    path("create/", workgroup.workgroup_create, name="workgroup_create"),
    path(
        "<int:pk>/update/", workgroup.workgroup_update, name="workgroup_update"
    ),
    path(
        "<int:pk>/delete/", workgroup.workgroup_delete, name="workgroup_delete"
    ),
]

## membership
urlpatterns += [
    path(
        "<int:workgroup_id>/membership/insert/",
        membership.membership_insert,
        name="membership_insert",
    ),
    path(
        "<int:workgroup_id>/membership/<int:pk>/update/",
        membership.membership_update,
        name="membership_update",
    ),
    path(
        "<int:workgroup_id>/membership/<int:pk>/delete/",
        membership.membership_delete,
        name="membership_delete",
    ),
]