from django.shortcuts import render
from django.shortcuts import redirect, reverse
from . import models
from . import forms
import hashlib
# Create your views here.


def detail_passwd(passwd, salt='add'):
    # 将密码加密
    dp = hashlib.sha256()
    passwd += salt
    # dp只接受字节类型
    dp.update(passwd.encode())
    return dp.hexdigest()


def login(request):
    print(request.path)
    print('session:', request.session, type(request.session))
    if request.session.get('is_login', None):
        print('1')
        return redirect(reverse('movie:home'))
    message = '请输入信息登录'
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

            if user.password == detail_passwd(password):
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
    if request.session.get('is_login', None):
        return redirect(reverse('movie:home'))

    message = "请填写信息注册账号"
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'user/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'user/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'user/register.html', locals())

                models.User.objects.create(name=username, password=detail_passwd(password1), email=email, sex=sex)

                return redirect(reverse('user:login'))
        else:
            return render(request, 'user/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'user/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果没有登录,跳转到登录页面
        return redirect(reverse('user:login'))
    request.session.flush()
    return redirect(reverse('movie:home'))
