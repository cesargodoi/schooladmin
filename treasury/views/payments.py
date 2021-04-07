from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render
from schooladmin.common import paginator

from ..forms import PaymentForm
from ..models import Payment


@login_required
@permission_required("treasury.view_payment")
def payments(request):
    queryset = Payment.objects.all()
    object_list = paginator(queryset, page=request.GET.get("page"))

    context = {"object_list": object_list, "title": "Payments"}
    return render(request, "treasury/payments.html", context)


@login_required
@permission_required("treasury.add_payment")
def payment_create(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            message = "The Payment has been created!"
            messages.success(request, message)
            return redirect("payments")

    context = {
        "form": PaymentForm(),
        "to_create": True,
        "title": "Create Payment",
    }
    return render(request, "treasury/payment_form.html", context)


@login_required
@permission_required("treasury.change_payment")
def payment_update(request, pk):
    object = get_object_or_404(Payment, pk=pk)
    if request.method == "POST":
        form = PaymentForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            message = "The Payment has been updated!"
            messages.success(request, message)
            return redirect("payments")

    context = {
        "form": PaymentForm(instance=object),
        "title": "Update Payment",
    }
    return render(request, "treasury/payment_form.html", context)


@login_required
@permission_required("treasury.delete_payment")
def payment_delete(request, pk):
    object = get_object_or_404(Payment, pk=pk)
    if request.method == "POST":
        if not object.order_set.all():
            object.delete()
            message = "The Payment has been deleted!"
            messages.success(request, message)
        return redirect("payments")

    context = {"object": object, "title": "confirm to delete"}
    return render(request, "treasury/confirm_delete.html", context)
