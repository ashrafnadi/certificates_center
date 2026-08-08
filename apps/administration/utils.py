# Add this to apps/administration/views.py or a new utils file


def get_session_permissions(request):
    """استرجاع صلاحيات المدقق/الموظف من الجلسة."""
    return {
        "auth_user_id": request.session.get("auth_user_id"),
        "isadd": request.session.get("perm_isadd", False),
        "isedit": request.session.get("perm_isedit", False),
        "isdelete": request.session.get("perm_isdelete", False),
        "isprint": request.session.get("perm_isprint", False),
        "iscommit": request.session.get("perm_iscommit", False),
        "isview": request.session.get("perm_isview", False),
    }


def can_edit(request):
    """التحقق من صلاحية التعديل."""
    return request.session.get("perm_isedit", False) or request.session.get(
        "user_is_admin", False
    )


def can_delete(request):
    """التحقق من صلاحية الحذف."""
    return request.session.get("perm_isdelete", False) or request.session.get(
        "user_is_admin", False
    )


def can_print(request):
    """التحقق من صلاحية الطباعة."""
    return request.session.get("perm_isprint", False) or request.session.get(
        "user_is_admin", False
    )


def can_view(request):
    """التحقق من صلاحية العرض."""
    return request.session.get("perm_isview", False) or request.session.get(
        "user_is_admin", False
    )
