from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Category, News
from .forms import ContactForm
from django.views.generic import TemplateView, ListView


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
    news_lists=News.published.all().order_by('-published_time')[:5]
    categories=Category.objects.all()
    local_one=News.published.filter(category__name="Mahalliy").order_by("-published_time")[:1]
    local_news=News.published.all().filter(category__name="Mahalliy").order_by("-published_time")[1:6]
    context={
        'news_lists': news_lists,
        'categories': categories,
        'local_news':local_news,
        'local_one':local_one,
    }
    return render(request,'news/index.html',context=context)


class HomePageView(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        context['categories']=Category.objects.all()
        context['news_lists']=News.published.all().order_by('-published_time')[:5]
        context['mahalliy_xabarlar']=News.published.all().filter(category__name="Mahalliy").order_by("-published_time")[:5]
        context['xorij_xabarlar']=News.published.all().filter(category__name="Xorij").order_by("-published_time")[:5]
        context['sport_xabarlar']=News.published.all().filter(category__name="Sport").order_by("-published_time")[:5]
        context['texnologiya_xabarlar']=News.published.all().filter(category__name="Texnologiya").order_by("-published_time")[:5]


        return context

# def contactPageView(request):
#     print(request.POST)
#     form=ContactForm(request.POST or None)
#     if request.method=="POST" and form.is_valid():
#         form.save()
#         return HttpResponse("<h2> bilan bog'langaniz uchun tashakkur")
#
#     context={
#         'form':form
#     }
#     return render(request,'news/contact.html',context)


class ContactPageView(TemplateView):
    template_name = "news/contact.html"
    def post(self,request,*args,**kwargs):
        form=ContactForm(request.POST)
        if request.method == "POST" and form.is_valid():
            form.save()
            return HttpResponse("<h2> bilan bog'langaniz uchun tashakkur")
        context = {
            'form': form
        }
        return render(request, 'news/contact.html',context)

