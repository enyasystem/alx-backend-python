from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


User = get_user_model()


@require_POST
@login_required
def delete_user(request):
    user = request.user
    # delete user will trigger post_delete signal
    user.delete()
    return JsonResponse({'status': 'deleted'})
