from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.urls import reverse
from schooladmin.common import paginator

from ..forms import PayTypeForm
from ..models import PayTypes


@login_required
@permission_required("treasury.view_paytypes")
def paytypes(request):
    queryset = PayTypes.objects.all()
    object_list = paginator(queryset, page=request.GET.get("page"))

    context = {"object_list": object_list, "title": "PayTypes"}
    return render(request, "treasury/paytypes.html", context)


@login_required
@permission_required("treasury.add_paytypes")
def paytype_create(request):
    if request.method == "POST":
        form = PayTypeForm(request.POST)
        if form.is_valid():
            form.save()
            message = "The PayType has been created!"
            messages.success(request, message)
            return redirect("paytypes")

    context = {
        "form": PayTypeForm(),
        "form_name": "Paytype",
        "form_path": "treasury/forms/paytype.html",
        "goback": reverse("payments"),
        "to_create": True,
        "title": "Create PayType",
    }
    return render(request, "base/form.html", context)


@login_required
@permission_required("treasury.change_paytypes")
def paytype_update(request, pk):
    object = PayTypes.objects.get(pk=pk)
    if request.method == "POST":
        form = PayTypeForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            message = "The PayType has been updated!"
            messages.success(request, message)
            return redirect("paytypes")

    context = {
        "form": PayTypeForm(instance=object),
        "form_name": "Paytype",
        "form_path": "treasury/forms/paytype.html",
        "goback": reverse("payments"),
        "title": "Update PayType",
    }
    return render(request, "base/form.html", context)


@login_required
@permission_required("treasury.delete_paytypes")
def paytype_delete(request, pk):
    object = PayTypes.objects.get(pk=pk)
    if request.method == "POST":
        if object.payment_set.all():
            object.is_active = False
            object.save()
            message = "The PayType has been inactivated!"
        else:
            object.delete()
            message = "The PayType has been deleted!"
        messages.success(request, message)
        return redirect("paytypes")

    context = {"object": object, "title": "confirm to delete"}
    return render(request, "base/confirm_delete.html", context)
