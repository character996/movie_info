from django.shortcuts import render
from django.core import serializers
from .models import AllMovie, AllMovieInfo, Actor, Tag, Director
from django.views.generic import View
import json
from django.http import JsonResponse
import jieba
import time


# Create your views here.
def tags(request):
    tag_li = Tag.objects.all()
    result = {'count': tag_li.count()}
    data = []
    for tag in tag_li:
        data.append(tag.tag)
    result['data'] = data
    return JsonResponse(result, safe=False)


def get_movie_for_type(request):
    start = request.GET.get('start') if request.GET.get('start') else 0
    start = int(start)
    num = request.GET.get('num') if request.GET.get('num') else 10
    num = int(num)
    type_info = request.GET.get('type') if request.GET.get('type') else ''
    value = request.GET.get('value') if request.GET.get('value') else ''
    print('value:', value, 'type:', type)
    result = {}
    if type_info == 'tag' and value:
        tag = Tag.objects.get(tag=value)
        movies = tag.allmovieinfo_set.all().order_by('-rate').only('id')
    elif type_info == 'director':
        director = Director.objects.get(name=value)
        movies = director.allmovieinfo_set.all().order_by('-rate')
    elif type_info == 'actor':
        actor = Actor.objects.get(name=value)
        movies = actor.allmovieinfo_set.all().order_by('-rate')
    else:
        movies = AllMovieInfo.objects.all().order_by('-rate')
    count = len(movies)
    print(movies.query)

    result['count'] = count
    return_movies = movies[start:start + num]
    json_data = []
    for movie in return_movies:
        json_data.append(movie_info(movie.id))
    result['data'] = json_data
    result['has_next'] = True if count > start + 10 else False
    return JsonResponse(result, safe=False, content_type='application/json')


class AllMovieView(View):

    def get(self, request):
        """接收get请求，返回数据"""
        title = request.GET.get('title')
        start = request.GET.get('start') if request.GET.get('start') else 0
        start = int(start)
        print('start:', start)
        num = request.GET.get('num') if request.GET.get('num') else 5
        num = int(num)
        print(title)
        start_time = time.clock()
        result = {}
        # 判断请求是否是ajax
        if request.is_ajax():
            # 先查询包含输入的title
            if title:
                movies = list(AllMovie.objects.filter(title__contains=title).order_by('-rate'))
                # 将输入的title进行分词，使用jieba库的搜索分词模式
                title_list = jieba.lcut_for_search(title)
                # 查看查询结果有多少
                if len(title) > 1:
                    # 将分词后的结果按照字符长度排序
                    title_list.sort(key=lambda i: len(i), reverse=True)
                    for ele in title_list:
                        print(ele)
                        # 如果分词项等于title，说明分词后的结果只有一个，打断循环。
                        if ele == title:
                            break
                        # 如果分词项是常用字，继续下一次循环
                        if ele in ['的', '了', '呢', '是', '我', '你', '他', ' ']:
                            continue
                        movies.extend((AllMovie.objects.filter(title__contains=ele)).order_by('-rate'))
                        # print(movies)
                    print('去重前:', len(movies))
                    # 查询结果去重，使用set去重会打乱顺序，自己编写
                    temp = []
                    for movie in movies:
                        if movie not in temp:
                            temp.append(movie)
                    movies = temp
                    print('去重后:', len(movies))
            else:
                movies = AllMovie.objects.all()
            count = len(movies)
            result['count'] = count
            # print(len(movies), type(movies), type(movies))
            # 序列化输出json字符串格式数据
            return_movies = movies[start:start+num]
            json_data = serializers.serialize('json', return_movies, fields=('id', 'title', 'url',
                                                                             'directors', 'casts', 'rate', 'tags'))
            # 将json字符串转换为python字典
            json_data = json.loads(json_data)
            result['data'] = json_data
            result['has_next'] = True if count > start + 5 else False

            # print(json_data)
            # res = JsonResponse(result, safe=False, content_type='application/json')
            # print(res, type(res), res.items())
            end_time = time.clock()
            print('程序运行时间：{} s'.format(end_time - start_time))
            return JsonResponse(result, safe=False, content_type='application/json')
        else:
            result['title'] = title
            print(result)
            print(11111111111111)
            return render(request, 'api/movie.html', {'result': result})
        return render(request, 'subjects.html', {'subjects': subjects})

    def post(self, request):
        """根据返回的title信息，用session存储，get请求返回具体的数据，在前端界面利用ajax发出get请求"""
        print('zhixing post')
        dicts = request.POST.dict()
        request.session['title'] = dicts.get('title')
        request.session['start'] = 0
        # print(request.body)
        # result = {}
        # print(dicts)
        # movies = AllMovie.objects.filter(title__contains=dicts['title'])
        # json_data = serializers.serialize('json', movies, fields=('id', 'title', 'url', 'directors'))
        # json_data = json.loads(json_data)
        # # print(json_data)
        # json_data = json.dumps(json_data, ensure_ascii=False)
        # # print(json_data)
        # result['data'] = json_data
        # return JsonResponse(result, safe=False, content_type='application/json')
        return render(request, 'api/movies.html', )


def get_intro(request):
    """返回电影简介信息"""
    url = request.GET.get('url')
    li = url.split('/')
    unique = li[-2]
    print(unique)
    movie = AllMovie.objects.get(id=unique)
    intro = movie.intro
    data = {'data': intro}
    return JsonResponse(data, safe=False)


def movie_info(movie_id):
    movie = AllMovieInfo.objects.get(id=movie_id)
    data = {'id': movie.id, 'title': movie.title, 'url': movie.url, 'cover': movie.cover,
            'rate': movie.rate, 'intro': movie.intro}
    actor_li = []
    for actor in movie.casts.all():
        actor_li.append(actor.name)
    data['casts'] = actor_li
    director_li = []
    for director in movie.directors.all():
        director_li.append(director.name)
    data['directors'] = director_li
    tag_li = []
    for tag in movie.tags.all():
        tag_li.append(tag.tag)
    data['tags'] = tag_li

    # print(movie.casts.all(), type(movie.casts))
    # print(data, type(data))

    return data


def get_movie(request):
    """接收get请求，返回数据"""
    start_time = time.clock()
    result = {}
    title = request.GET.get('title')
    start = request.GET.get('start') if request.GET.get('start') else 0
    start = int(start)
    print('start:', start)
    num = request.GET.get('num') if request.GET.get('num') else 5
    num = int(num)
    # title = movie_title.strip()
    # 先查询包含输入的title
    movies = AllMovieInfo.objects.filter(title__contains=title).order_by('-rate')
    print(movies.query)

    # 将输入的title进行分词，使用jieba库的搜索分词模式
    title_list = jieba.lcut_for_search(title)
    # 查看查询结果有多少
    if len(title) > 1:
        # 将分词后的结果按照字符长度排序
        title_list.sort(key=lambda i: len(i), reverse=True)
        for ele in title_list:
            print(ele)
            # 如果分词项等于title，说明分词后的结果只有一个，打断循环。
            if ele == title:
                break
            # 如果分词项是常用字，继续下一次循环
            if ele in ['的', '了', '呢', '是', '我', '你', '他', ' ']:
                continue
            movies.extend((AllMovie.objects.filter(title__contains=ele)).order_by('-rate'))
            # print(movies)
        print('去重前:', len(movies))
        # 查询结果去重，使用set去重会打乱顺序，自己编写
        temp = []
        for movie in movies:
            if movie not in temp:
                temp.append(movie)
        movies = temp
        print('去重后:', len(movies))
    count = len(movies)
    result['count'] = count
    movie_data = []
    for movie in movies[start: start+num]:
        data = movie_info(movie.id)
        movie_data.append(data)
    result['data'] = movie_data
    result['has_next'] = True if count > start + 10 else False
    # print(movie_data, type(movie_data))
    # print(json_data)
    # res = JsonResponse(result, safe=False, content_type='application/json')
    # print(res, type(res), res.items())
    end_time = time.clock()
    print('程序运行时间：{} s'.format(end_time - start_time))
    # print(result, type(result))
    print(result['count'])
    return JsonResponse(result, safe=False, content_type='application/json')
