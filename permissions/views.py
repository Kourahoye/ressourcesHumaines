from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib.auth.models import Permission
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.decorators.http import require_POST
from Users.models import User


class Permissions(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'permissions/perms.html'
    permission_required = 'auth.add_permission'

    def post(self, request, *args, **kwargs):
        try:
            user_id = request.POST.get('user_id')
            perm_ids = request.POST.getlist('permissions[]')
            if not user_id or not perm_ids:
                return JsonResponse({'error': 'Missing user or permissions'}, status=400)

            # Prevent self-permission assignment
            if int(user_id) == self.request.user.id:
                return JsonResponse({'error': 'Cannot assign permissions to yourself'}, status=403)

            user = User.objects.get(id=user_id)
            permissions = Permission.objects.filter(id__in=perm_ids)

            current_user_perms = set(user.get_all_permissions())
            existing_perms = [
                perm.codename for perm in permissions
                if f"{perm.content_type.app_label}.{perm.codename}" in current_user_perms
            ]

            if existing_perms:
                return JsonResponse({
                    'error': f'Permissions already exist: {", ".join(existing_perms)}'
                }, status=400)

            user.user_permissions.add(*permissions)
            return JsonResponse({'success': True})

        except Permission.DoesNotExist:
            return JsonResponse({'error': 'Invalid permission'}, status=404)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid user'}, status=404)
        except ValueError:
            return JsonResponse({'error': 'Invalid user ID format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@permission_required('auth.add_permission', raise_exception=True)
@login_required
def get_permissions(request):
    permissions = Permission.objects.all().values('id', 'name', 'codename')
    return JsonResponse({'permissions': list(permissions)})


@permission_required('Users.list_users', raise_exception=True)
@login_required
def get_users(request):
    users = User.objects.all()
    users_data = [{'id': user.id, 'username': user.username} for user in users]
    return JsonResponse({'users': users_data})


@permission_required('auth.add_permission', raise_exception=True)
@login_required
def get_user_permissions(request):
    user_id = request.GET.get('user_id')
    try:
        user = User.objects.get(id=user_id)
        if not user:
            return JsonResponse({'error': 'User not found'})
        if user and not user.is_active:
            return JsonResponse({"error": "Permissions disabled for inactive users"})
        perm_strings = user.get_all_permissions()
        permissions = Permission.objects.filter(
            codename__in=[p.split('.')[-1] for p in perm_strings]
        ).values('id', 'name', 'codename')
        return JsonResponse({'permissions': list(permissions)})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)


@permission_required('auth.delete_permission', raise_exception=True)
@login_required
def remove_all_user_permissions(request):
    user_id = request.POST.get('user_id')
    try:
        user = User.objects.get(id=user_id)
        if user.is_superuser:
            return JsonResponse({'error': 'Cannot remove permissions from a superuser'}, status=403)
        if not request.user.is_staff and user.is_staff:
            return JsonResponse({'error': 'Insufficient permissions to modify this user'}, status=403)
        user.user_permissions.clear()
        return JsonResponse({'success': True})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)


@permission_required('auth.delete_permission', raise_exception=True)
@login_required
@require_POST
def remove_user_permissions(request):
    user_id = request.POST.get('user_id')
    perm_ids = request.POST.getlist('permissions[]')
    try:
        user = User.objects.get(id=user_id)
        if user.is_superuser:
            return JsonResponse({'error': 'Cannot remove permissions from a superuser'}, status=403)
        if not request.user.is_staff and user.is_staff:
            return JsonResponse({'error': 'Insufficient permissions to modify this user'}, status=403)
        permissions = Permission.objects.filter(id__in=perm_ids)
        user.user_permissions.remove(*permissions)
        return JsonResponse({'success': True})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Permission.DoesNotExist:
        return JsonResponse({'error': 'One or more permissions not found'}, status=404)
