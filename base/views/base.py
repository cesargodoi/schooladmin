from datetime import datetime, timedelta
from django.http.response import Http404
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from center.models import Center


@login_required
def home(request):
    try:
        center = get_object_or_404(Center, id=request.user.person.center.id)
    except:
        raise Http404

    context = {"object": center}
    return render(request, "base/home.html", context)


# @login_required
# def home(request):
#     if request.session.get("search"):
#         del request.session["search"]
#     try:
#         center = get_object_or_404(Center, id=request.user.person.center.id)
#     except:
#         raise Http404
#     # persons of center
#     persons = center.person_set.all()
#     PW = len([p.id for p in persons if p.aspect == "PW"])
#     YW = len([p.id for p in persons if p.aspect == "YW"])
#     A1 = len([p.id for p in persons if p.aspect == "A1"])
#     A2 = len([p.id for p in persons if p.aspect == "A2"])
#     A3 = len([p.id for p in persons if p.aspect == "A3"])
#     A4 = len([p.id for p in persons if p.aspect == "A4"])
#     GR = len([p.id for p in persons if p.aspect == "GR"])
#     A5 = len([p.id for p in persons if p.aspect == "A5"])
#     A6 = len([p.id for p in persons if p.aspect == "A6"])
#     # events of center
#     today = datetime.now().date()
#     l30d = today - timedelta(30)
#     n30d = today + timedelta(30)
#     events = center.event_set.all()
#     lasts = len([ev for ev in events if ev.date <= today and ev.date >= l30d])
#     nexts = len([ev for ev in events if ev.date >= today and ev.date <= n30d])
#     # workgroups of center
#     workgroups = center.workgroup_set.all()
#     ASP = len([wg.id for wg in workgroups if wg.workgroup_type == "ASP"])
#     MNT = len([wg.id for wg in workgroups if wg.workgroup_type == "MNT"])
#     ADM = len([wg.id for wg in workgroups if wg.workgroup_type == "ADM"])
#
#     context = {
#         "object": center,
#         "persons": len(persons),
#         "aspects": [
#             ["Public Work", PW, "PW"],
#             ["Youth Work", YW, "YW"],
#             ["1st. Aspect", A1, "A1"],
#             ["2nd. Aspect", A2, "A2"],
#             ["3rd. Aspect", A3, "A3"],
#             ["4th. Aspect", A4, "A4"],
#             ["Grail", GR, "GR"],
#             ["5th. Aspect", A5, "A5"],
#             ["6th. Aspect", A6, "A6"],
#         ],
#         "events": len(events),
#         "lasts": lasts,
#         "nexts": nexts,
#         "workgroups": len(workgroups),
#         "workgroup_types": [
#             ["Aspect", ASP, "ASP"],
#             ["Maintenence", MNT, "MNT"],
#             ["Admin", ADM, "ADM"],
#         ],
#     }
#
#     return render(request, "base/home.html", context)


def error_404(request, exception):
    return render(request, "base/404.html")
