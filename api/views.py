from django.shortcuts import render
from django.core import serializers
from .models import AllMovie
from django.views.generic import View
import json
from django.http import JsonResponse
import jieba
import time


# Create your views here.


class AllMovieView(View):

    def get(self, request):
        """接收get请求，返回数据"""
        start_time = time.clock()
        result = {}
        print(request.session['start'])
        # 判断请求是否是ajax
        if request.is_ajax():
            title = request.session['title'].strip()
            # 先查询包含输入的title
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
            count = len(movies)
            result['count'] = count
            start = int(request.session['start'])
            # movies = AllMovie.objects.filter(title__contains=title)[start:5+start]
            # print(len(movies), type(movies), type(movies))
            # 序列化输出json字符串格式数据
            return_movies = movies[start: start + 5]
            json_data = serializers.serialize('json', return_movies, fields=('id', 'title', 'url',
                                                                             'directors', 'casts', 'rate', 'tags'))
            # 将json字符串转换为python字典
            json_data = json.loads(json_data)
            result['data'] = json_data
            request.session['start'] = start + 5
            result['has_next'] = True if count > start + 5 else False

            # print(json_data)
            # res = JsonResponse(result, safe=False, content_type='application/json')
            # print(res, type(res), res.items())
            end_time = time.clock()
            print('程序运行时间：{} s'.format(end_time - start_time))
            return JsonResponse(result, safe=False, content_type='application/json')

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
        return render(request, 'api/movie.html', )


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
