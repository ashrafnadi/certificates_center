from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    if request.user.is_superuser:
        request.user.is_admin = True
    elif hasattr(request.user, 'profile'):
        if request.user.profile.role == 'director':
            request.user.is_director = True
        elif request.user.profile.role == 'supervisor':
            request.user.is_supervisor = True
        elif request.user.profile.role == 'auditor':
            request.user.is_auditor = True
        elif request.user.profile.role == 'employee':
            request.user.is_employee = True
        else:
            request.user.is_student = False
    else:
        request.user.is_student = False
    
    return render(request, "graduate/index.html")
