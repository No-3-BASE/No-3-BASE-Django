from django.contrib.auth.models import User

def toolbar_context(request):
    print(f"目前登入狀態 {request.user.is_authenticated}")
    if request.user.is_authenticated:
        return {
            'toolBar': {
                'isLogin': True,
                'name': request.user.first_name
            }
        }
    return {
        'toolBar': {
            'isLogin': False,
            'name': "訪客"
        }
    }