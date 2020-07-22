from django.http import JsonResponse
from django.shortcuts import redirect, reverse

LOGIN_REQUIRED_URLS = {'/search/', }


def check_login_middleware(get_resp):

    def wrapper(request, *args, **kwargs):
        if request.path in LOGIN_REQUIRED_URLS:
            # 会话中包含userid则视为已经登录
            if 'userid' not in request.session:
                return redirect(reverse('user:login'))
        return get_resp(request, *args, **kwargs)
    return wrapper
