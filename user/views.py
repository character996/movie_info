from django.shortcuts import render
from django.shortcuts import redirect, reverse
from . import models
from . import forms
import hashlib
import datetime
from django.conf import settings
# Create your views here.


def detail_passwd(passwd, salt='add'):
    # 将密码加密
    dp = hashlib.sha256()
    passwd += salt
    # dp只接受字节类型
    dp.update(passwd.encode())
    return dp.hexdigest()


def make_confirm_email(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = detail_passwd(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user)
    return code


def send_email(email, code):
    from django.core.mail import EmailMultiAlternatives

    subject = '注册确认邮件'

    text_content = '''
                        如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                        <p>感谢注册<a href="http://{}/user/confirm/?code={}" target=blank>movie</a>，\
                        </p>
                        <p>请点击站点链接完成注册确认！</p>
                        <p>此链接有效期为{}天！</p>
                        '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


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
                request.session['has_confirm'] = user.has_confirmed
                print(request.session['has_confirm'])
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
                # if same_email_user:
                #     message = '该邮箱已经被注册了！'
                #     return render(request, 'user/register.html', locals())

                new_user = models.User.objects.create(name=username, password=detail_passwd(password1),
                                                      email=email, sex=sex)
                code = make_confirm_email(new_user)
                send_email(email, code)
                message = '前往邮箱去确认'
                # return redirect(reverse('user:login'))
                return render(request, 'user/confirm.html', locals())
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


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'user/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'user/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        request.session['has_confirm'] = True
        message = '感谢确认，请使用账户登录！'
        return render(request, 'user/confirm.html', locals())
