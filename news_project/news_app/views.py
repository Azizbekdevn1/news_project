from django.shortcuts import render, get_object_or_404

from .models import Category, News


def news_list(request):
    news_lists = News.published.all()  # 2-usul
    context = {
        "news_lists": news_lists
    }
    return render(request, 'news/news_list.html', context=context)


def news_detail(request, id):
    news = get_object_or_404(News, id=id, status=News.Status.Published)
    context = {
        'news': news
    }
    return render(request, 'news/news_detail.html', context=context)

def homePageView(request):
    news=News.published.all()
    categories=Category.objects.all()
    context={
        'news': news,
        'categories': categories
    }

    return render(request,'news/index.html',context=context)

def contactPageView(request):
    context={

    }
    return render(request,'news/contact.html',context)