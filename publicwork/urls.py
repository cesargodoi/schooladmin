from django.urls import path

from .views import seeker, lecture, listener, report, historic

# publicwork
urlpatterns = [
    path("", report.publicwork_home, name="publicwork_home"),
]

# seeker
urlpatterns += [
    path("seeker/", seeker.seeker_home, name="seeker_home"),
    path(
        "seeker/<int:pk>/detail/", seeker.seeker_detail, name="seeker_detail"
    ),
    path("seeker/create/", seeker.seeker_create, name="seeker_create"),
    path(
        "seeker/<int:pk>/update/", seeker.seeker_update, name="seeker_update"
    ),
    path(
        "seeker/<int:pk>/delete/", seeker.seeker_delete, name="seeker_delete"
    ),
    path(
        "seeker/<int:pk>/reinsert/",
        seeker.seeker_reinsert,
        name="seeker_reinsert",
    ),
    path(
        "seeker/<int:pk>/frequencies/",
        seeker.seeker_frequencies,
        name="seeker_frequencies",
    ),
    path(
        "seeker/<int:pk>/historics/",
        seeker.seeker_historics,
        name="seeker_historics",
    ),
]

# lecture
urlpatterns += [
    path("lecture/", lecture.lecture_home, name="lecture_home"),
    path(
        "lecture/<int:pk>/detail/",
        lecture.lecture_detail,
        name="lecture_detail",
    ),
    path("lecture/create/", lecture.lecture_create, name="lecture_create"),
    path(
        "lecture/<int:pk>/update/",
        lecture.lecture_update,
        name="lecture_update",
    ),
    path(
        "lecture/<int:pk>/delete/",
        lecture.lecture_delete,
        name="lecture_delete",
    ),
]

# listener
urlpatterns += [
    path(
        "lecture/<int:lect_pk>/add-listener",
        listener.add_listener,
        name="add_listener",
    ),
    path(
        "lecture/<int:lect_pk>/update-listener/<int:lstn_pk>/",
        listener.update_listener,
        name="update_listener",
    ),
    path(
        "lecture/<int:lect_pk>/remove-listener/<int:lstn_pk>/",
        listener.remove_listener,
        name="remove_listener",
    ),
    path(
        "seeker/<int:pk>/add-frequency/",
        listener.add_frequency,
        name="add_frequency",
    ),
    path(
        "seeker/<int:seek_pk>/update-frequency/<int:freq_pk>",
        listener.update_frequency,
        name="update_frequency",
    ),
    path(
        "seeker/<int:seek_pk>/remove-frequency/<int:freq_pk>/",
        listener.remove_frequency,
        name="remove_frequency",
    ),
]

# historics
urlpatterns += [
    path(
        "seeker/<int:pk>/create-historic/",
        historic.create_historic,
        name="create_historic",
    ),
    path(
        "seeker/<int:seek_pk>/update-historic/<int:hist_pk>",
        historic.update_historic,
        name="update_historic",
    ),
    path(
        "seeker/<int:seek_pk>/delete-historic/<int:hist_pk>",
        historic.delete_historic,
        name="delete_historic",
    ),
]

# reports
urlpatterns += [
    path(
        "report/frequencies-per-period/",
        report.frequencies_per_period,
        name="frequencies_per_period",
    ),
    path(
        "report/lectures-per-period/",
        report.lectures_per_period,
        name="lectures_per_period",
    ),
]
