
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib.auth.models import Permission
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from Users.models import User


class Permissions(LoginRequiredMixin,PermissionRequiredMixin, TemplateView):
    template_name = 'permissions/perms.html'
    permission_required = 'auth.add_permission'
    
    def post(self, request, *args, **kwargs):
        try:
            user_id = request.POST.get('user_id')
            perm_ids = request.POST.getlist('permissions[]')
            if not user_id or not perm_ids:
                return JsonResponse({'error': 'Missing user or permissions'}, status=400)

            # Prevent self-permission assignment
            if user_id == self.request.user.id:
                return JsonResponse({'error': 'Cannot assign permissions to yourself'}, status=403)
            
            user = User.objects.get(id=user_id)
            permissions = Permission.objects.filter(id__in=perm_ids)
            
            # Check if any permission already exists - CORRECTED
            existing_perms = []
            current_user_perms = set(user.get_all_permissions())
            
            for permission in permissions:
                perm_string = f"{permission.content_type.app_label}.{permission.codename}"
                if perm_string in current_user_perms:
                    existing_perms.append(permission.codename)
            
            if existing_perms:
                return JsonResponse({
                    'error': f'Permissions already exist: {", ".join(existing_perms)}'
                }, status=400)
            
            # Add the permissions
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



@login_required
@permission_required('auth.add_permission, raise_exception=True)')
def get_permissions(request):
    permissions = Permission.objects.all().values('id', 'name', 'codename')
    return JsonResponse({'permissions': list(permissions)})

@login_required
@permission_required('User.list_users, raise_exception=True)')
def get_users(request):
    from Users.models import User
    users = User.objects.all()
    users_data = [{'id': user.id, 'username': user.username} for user in users]
    return JsonResponse({'users': users_data})

@login_required
@permission_required('auth.add_permission, raise_exception=True)')
def get_user_permissions(request):
    from Users.models import User
    user_id = request.GET.get('user_id')
    try:
        user = User.objects.get(id=user_id)
        perm_strings = user.get_all_permissions()
        permissions = Permission.objects.filter(codename__in=[p.split('.')[-1] for p in perm_strings]).values('id', 'name', 'codename')
        return JsonResponse({'permissions': list(permissions)})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)