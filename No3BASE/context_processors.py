from django.contrib.auth.models import User

def toolbar_context(request):
    if request.user.is_authenticated:
        return {
            'toolBar': {
                'isLogin': True,
                'name': request.user.username
            }
        }
    return {
        'toolBar': {
            'isLogin': False,
            'name': "訪客"
        }
    }