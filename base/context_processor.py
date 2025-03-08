from .models import Profile

def avatar(request):
    if request.user.is_authenticated:
        return {'avatar': request.user.profile.avatar.url}
    return {'avatar': '/media/profile_pics/default.png'}
