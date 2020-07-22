from django.shortcuts import render, HttpResponse, redirect
from .models import Top250
from .search import search_movie
from .models import SearchResult, SearchTitle, SearchRecord
from django.views.generic import TemplateView, ListView, RedirectView
from django.urls import reverse
from urllib import parse
from user.models import User

# Create your views here.

#
# def home(request):
#     return render(request, 'movie/home.html')


class Top250View(ListView):
    template_name = 'movie/top250.html'
    model = Top250
    paginate_by = 25
    context_object_name = 'movies'
    ordering = 'rank'
    # def get_context_data(self, **kwargs):
    #     movies = super().get_context_data(**kwargs)
    #     # movies['movies'] = Top250.objects.all()
    #     movies['movies'] = movies['page_obj']
    #     print(movies['page_obj'], type(movies['page_obj']))
    #     print(movies['movies'], type(movies['movies']))
    #     print('movies:', movies)
    #     return movies

    def get_queryset(self):
        return Top250.objects.all()


def search(request):
    if request.method == 'POST':
        print(request.POST.dict())
        try:
            is_success = False
            if request.POST['title'] == '':
                message = '请输入搜索的关键字'
                raise ValueError
            title = request.POST['title'][0:30]
            print(title)
            num = int(request.POST['num'])
            print(num)
            if title and num:
                search_title, created = SearchTitle.objects.get_or_create(
                    title=title,
                    defaults={'title': title}
                )
                exists_result = search_title.searchresult_set.all()
                if num > exists_result.count():
                    for i in range(exists_result.count(), num, 15):
                        data_per_page = search_movie.get_content(i, title)
                        if not data_per_page:
                            break
                        movie_per_page = search_movie.detail_data(data_per_page)
                        # movies_data += movie_per_page
                        for data in movie_per_page:
                            movie_obj = SearchResult(name=data[0][0:200], href=data[1][0:100], workers=data[2][0:200],
                                                     abstract=data[3][0:200],
                                                     score=data[4],
                                                     title=search_title)
                            movie_obj.save()
                    search_result = exists_result[0:num]
                    # print(search_result)
                is_success = True
                return redirect(reverse('movie:search_result') + '?' + parse.urlencode({'title': title, 'num': num}))
        except ValueError:
            return render(request, 'movie/home.html', {'message': message, })
        finally:
            title = title
            num = num
            user_id = request.session['user_id']
            user = User.objects.get(id=user_id)
            print('user_id:', user_id)
            SearchRecord.objects.create(title=title, user=user, num=num, result=is_success)


class SearchResultView(ListView):
    template_name = 'movie/result.html'
    model = SearchResult
    paginate_by = 15
    context_object_name = 'movies'
    http_method_names = 'get'

    def get_queryset(self):
        keys = self.request.GET.dict()
        title = keys['title']
        search_title = SearchTitle.objects.get(title=title)
        num = int(keys['num'])
        return SearchResult.objects.filter(title=search_title)[0:num]

    def get_context_data(self, *, object_list=None, **kwargs):
        result = super().get_context_data(**kwargs)
        result['params'] = self.request.GET.dict()
        print(result)
        return result
    # def get_context_data(self, **kwargs):
    #     movies = super().get_context_data(**kwargs).filter
    # #     # movies['movies'] = Top250.objects.all()
    # #     movies['movies'] = movies['page_obj']
    # #     print(movies['page_obj'], type(movies['page_obj']))
    # #     print(movies['movies'], type(movies['movies']))
    #     print('movies:', movies)
    #     return movies
# class SearchView(ListView):
#
#     def post(self):
#         title = request.GET.get('title')
#         print('title:', title, type(title))
#         page_num = int(request.GET.get('page_num'))
