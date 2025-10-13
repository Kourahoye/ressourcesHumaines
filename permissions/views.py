from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.
# 1 -get users except me
# 2- get all perms after check addperm
#check add or remove perms for me
#add or remove perms if check true

class Permissions(TemplateView):
    template_name = 'permissons/perms.html'

    def post(self, request, *args, **kwargs):
        from Users.models import User
        try:
            user_id = self.request.POST.get('user')
            perm_id = self.request.POST.get('perm')
            
            if not user_id or not perm_id:
                return JsonResponse({'error': 'Missing user or permission'}, status=400)
            
            # Prevent self-permission assignment
            if int(user_id) == self.request.user.id:
                return JsonResponse({'error': 'Cannot assign permissions to yourself'}, status=403)
            
            user = User.objects.get(id=user_id)
            permission = Permission.objects.get(id=perm_id)
            
            # Check if permission already exists
            if user.has_perm(f"{permission.content_type.app_label}.{permission.codename}"):
                return JsonResponse({'error': 'Permission already exists'}, status=400)
            
            user.user_permissions.add(permission)
            return JsonResponse({'success': True})
            
        except Permission.DoesNotExist:
            return JsonResponse({'error': 'Invalid permission'}, status=404)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid user'}, status=404)
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
    users = User.object.all().exclude(id=request.user.id)
    users_data = [{'id': user.id, 'username': user.username} for user in users]
    return JsonResponse({'users': users_data})