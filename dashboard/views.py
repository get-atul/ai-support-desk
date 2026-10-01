from django.shortcuts import render


def admin_dashboard(request):

    return render(
        request,
        "dashboard/admin_dashboard.html",
    )


def user_dashboard(request):

    return render(
        request,
        "dashboard/user_dashboard.html",
    )