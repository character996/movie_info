from django.shortcuts import render
from django.shortcuts import redirect, reverse
from . import models
from . import forms
# Create your views here.


def login(request):
    print(request.path)
    print('session:', request.session, type(request.session))
    if request.session.get('is_login', None):
        print('1')
        return redirect(reverse('movie:home'))
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.User.objects.get(name=username)
            except:
                print('2')
                message = '用户不存在！'
                return render(request, 'user/login.html', locals())

            if user.password == password:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect(reverse("movie:home"))
            else:
                message = '密码不正确！'
                print('3')
                return render(request, 'user/login.html', locals())
        else:
            print(4)
            return render(request, 'user/login.html', locals())

    login_form = forms.LoginForm()
    print(locals())
    print('5')
    return render(request, 'user/login.html', locals())


def register(request):
    pass


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect(reverse('user:login'))
    request.session.flush()
    return redirect(reverse('movie:home'))
