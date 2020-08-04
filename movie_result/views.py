from django.shortcuts import render

# Create your views here.


def search_subjects(request):
    title = request.GET.get('title')
    result = {'title': title}

    return render(request, 'movie_result/movie.html', {'result': result})


def tags(request):
    tag = request.GET.get('tag') if request.GET.get('tag') else ''
    result = {'tag': tag}
    print(tag)
    return render(request, 'movie_result/tag.html', {'result': result})


def types(request):
    type_value = request.GET.get('type')
    value = request.GET.get('value')
    result = {'type': type_value, 'value': value}
    return render(request, 'movie_result/types.html', {'result': result})
