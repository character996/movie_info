from django.shortcuts import render
from django.core import serializers
from .models import AllMovie
from django.views.generic import View
import json
from django.http import JsonResponse
# Create your views here.


class AllMovieView(View):

    def get(self, request):
        result = {}
        print(request.session['start'])
        if request.is_ajax():
            title = request.session['title']
            start = int(request.session['start'])
            # 查看查询结果有多少
            count = AllMovie.objects.filter(title__contains=title[0]).count()
            result['count'] = count

            start = int(request.session['start'])
            movies = AllMovie.objects.filter(title__contains=title[0])[start:5+start]
            # 序列化输出json字符串格式数据
            json_data = serializers.serialize('json', movies, fields=('id', 'title', 'url', 'directors', 'casts',
                                                                      'rate', 'tags'))
            # 将json字符串转换为python字典
            json_data = json.loads(json_data)
            result['data'] = json_data
            request.session['start'] = start+5
            result['has_next'] = True if count > start + 5 else False

            print(json_data)
            res = JsonResponse(result, safe=False, content_type='application/json')
            print(res, type(res), res.items())
            return JsonResponse(result, safe=False, content_type='application/json')

    def post(self, request):
        print('zhixing post')
        dicts = request.POST.dict()
        request.session['title'] = dicts.get('title')
        request.session['start'] = 0
        print(request.body)
        result = {}
        print(dicts)
        movies = AllMovie.objects.filter(title__contains=dicts['title'][0])
        json_data = serializers.serialize('json', movies, fields=('id', 'title', 'url', 'directors'))
        json_data = json.loads(json_data)
        # print(json_data)
        json_data = json.dumps(json_data, ensure_ascii=False)
        # print(json_data)
        result['data'] = json_data
        # return JsonResponse(result, safe=False, content_type='application/json')
        return render(request, 'api/movie.html', result)


def get_intro(request):
    title = request.GET.get('title')
    movie = AllMovie.objects.get(title=title)
    intro = movie.intro
    data = {'data': intro}
    return JsonResponse(data, safe=False)

