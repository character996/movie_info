from django.core.mail import send_mail
import os
import django
# os.environ['DJANGO_SETTINGS_MODULE'] = 'showmovie.settings'
os.environ.setdefault('DJANGO_SETTING_MODULE', 'movie_git.settings')
# django.setup()
if __name__ == '__main__':

    send_mail(
        '来自www.liujiangblog.com的测试邮件',
        '欢迎访问www.liujiangblog.com，这里是刘江的博客和教程站点，本站专注于Python、Django和机器学习技术的分享！',
        '870418012@qq.com',
        ['870418012@qq.com'],
    )
