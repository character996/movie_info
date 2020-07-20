from django.shortcuts import render, HttpResponse, redirect
from .models import Top250
from .search import search_movie
from .models import SearchResult, SearchTitle
from django.views.generic import TemplateView, ListView, RedirectView
from django.urls import reverse
from urllib import parse

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
    # print('********')
    # def get_context_data(self, **kwargs):
    #     movies = super().get_context_data(**kwargs)
    #     # movies['movies'] = Top250.objects.all()
    #     movies['movies'] = movies['page_obj']
    #     print(movies['page_obj'], type(movies['page_obj']))
    #     print(movies['movies'], type(movies['movies']))
    #     print('movies:', movies)
    #     return movies

    def get_queryset(self):
        print('*****')
        return Top250.objects.all()


# def search(request):
#     title = request.GET.get('title')
#     print('title:', title, type(title))
#     page_num = int(request.GET.get('page_num'))
#     print('page:', page_num, type(page_num))
#     start = 0
#     title_is_exists = False
#     try:
#         title_exists = SearchTitle.objects.get(title=title)
#         title_is_exists = True
#         exists_result_num = title_exists.searchresult_set.all().count()
#         print('exists_result_num ：', exists_result_num)
#         if page_num*15 > exists_result_num:
#             print('page*15 :', page_num*15)
#             start = exists_result_num
#             raise Exception
#     except Exception as e:
#         print(e)
#         # movies_data = []
#         if title_is_exists is False:
#             search_title = SearchTitle()
#             search_title.title = title
#             search_title.save()
#         title_exists = SearchTitle.objects.get(title=title)
#         print('title exists:', title_exists)
#         for i in range(start, page_num*15, 15):
#             data_per_page = search_movie.get_content(i, title)
#             if data_per_page is None:
#                 break
#             movie_per_page = search_movie.detail_data(data_per_page)
#             # movies_data += movie_per_page
#
#             for data in movie_per_page:
#                 movie_obj = SearchResult(name=data[0], href=data[1], workers=data[2], abstract=data[3], score=data[4],
#                                          title=title_exists)
#                 movie_obj.save()
#     finally:
#         movies_all = title_exists.searchresult_set.all().order_by('id')[0: page_num*15]
#         paginator = Paginator(movies_all, 15)
#         movies = paginator.get_page(page_num)
#         return render(request, 'movie/result.html', {'movies': movies, 'title': title})
#
# class SearchRedirectView(RedirectView):
#
def search(request):
    if request.method == 'POST':
        title = request.POST['title']
        num = int(request.POST['num'])
        search_title, created = SearchTitle.objects.get_or_create(
            title=title,
            defaults={'title': title}
        )
        exists_result = search_title.searchresult_set.all()
        if num > exists_result.count():
            for i in range(exists_result.count(), num, 15):
                data_per_page = search_movie.get_content(i, title)
                if data_per_page is None:
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
            print(search_result)
        print('*'*10)
        return redirect(reverse('movie:search_result') + '?' + parse.urlencode({'title': title, 'num': num}))


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
