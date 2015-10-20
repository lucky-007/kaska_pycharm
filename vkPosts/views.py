import random
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader, RequestContext
from vkPosts.models import Post


N = 2


# Функция получения списка N рандомных постов.
# Передать нужно все объекты и N (по умолчанию 1)
# возвращает список рандмоных постов
# если ввести N больше чем количество постов в базе - то выведутся все посты

def get_N_random_posts(list_of_posts, n = 1):
    list_of_posts = list(list_of_posts).copy()
    count = list_of_posts.__len__()
    new_list = []

    if (n > count):
        n = count
    for i in range(0, n):
        k = random.randint(0, count - i - 1)
        new_list.append(list_of_posts[k])
        del list_of_posts[k]
    return new_list

def index(request):
    post_list = get_N_random_posts(Post.objects.all(), N)
    #p = Post.objects.get(id = 6)
    context = RequestContext(request, {
        'post_list' : post_list
    })
    return render(request, 'vkPosts/index.html', context)