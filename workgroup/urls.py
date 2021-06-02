from django.urls import path
from .views import workgroup, membership, mentoring

# workgroup
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

# membership
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

# mentoring
urlpatterns += [
    path("mentoring/", mentoring.mentoring_home, name="mentoring_home"),
    path(
        "mentoring/<int:pk>/detail/",
        mentoring.mentoring_group_detail,
        name="mentoring_group_detail",
    ),
    path(
        "mentoring/<int:group_pk>/member/<uuid:person_pk>/detail/",
        mentoring.mentoring_member_detail,
        name="mentoring_member_detail",
    ),
    path(
        "mentoring/<int:group_pk>/member/<uuid:person_pk>/frequencies/",
        mentoring.mentoring_member_frequencies,
        name="mentoring_member_frequencies",
    ),
    path(
        "mentoring/<int:group_pk>/member/<uuid:person_pk>/historics/",
        mentoring.mentoring_member_historics,
        name="mentoring_member_historics",
    ),
]
