from django.shortcuts import render, HttpResponse
from .models import Top250
from django.core.paginator import Paginator
from .search import search_movie
from .models import SearchResult, SearchTitle
# Create your views here.


def home(request):
    return render(request, 'movie/home.html')


def top250(request):
    movies = Top250.objects.all()
    paginator = Paginator(movies, 25)
    page = request.GET.get('page')

    movie = paginator.get_page(page)
    return render(request, 'movie/top250.html', {'movies': movie})


def search(request):
    title = request.GET.get('title')
    print('title:', title, type(title))
    page_num = int(request.GET.get('page_num'))
    print('page:', page_num, type(page_num))
    start = 0
    title_is_exists = False
    try:
        title_exists = SearchTitle.objects.get(title=title)
        title_is_exists = True
        exists_result_num = title_exists.searchresult_set.all().count()
        print('exists_result_num ：', exists_result_num)
        if page_num*15 > exists_result_num:
            print('page*15 :', page_num*15)
            start = exists_result_num
            raise Exception
    except Exception as e:
        print(e)
        # movies_data = []
        if title_is_exists is False:
            search_title = SearchTitle()
            search_title.title = title
            search_title.save()
        title_exists = SearchTitle.objects.get(title=title)
        print('title exists:', title_exists)
        for i in range(start, page_num*15, 15):
            data_per_page = search_movie.get_content(i, title)
            if data_per_page is None:
                break
            movie_per_page = search_movie.detail_data(data_per_page)
            # movies_data += movie_per_page

            for data in movie_per_page:
                movie_obj = SearchResult(name=data[0], href=data[1], workers=data[2], abstract=data[3], score=data[4],
                                         title=title_exists)
                movie_obj.save()
    finally:
        movies_all = title_exists.searchresult_set.all().order_by('id')[0: page_num*15]
        paginator = Paginator(movies_all, 15)
        movies = paginator.get_page(page_num)
        return render(request, 'movie/result.html', {'movies': movies, 'title': title})

