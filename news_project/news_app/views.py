from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from .models import Category, News
from .forms import ContactForm,NewsForm
from django.views.generic import TemplateView, ListView,UpdateView, DeleteView,CreateView


def news_list(request):
    news_lists = News.published.all()  # 2-usul
    context = {
        "news_lists": news_lists
    }
    return render(request, 'news/news_list.html', context=context)


def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {
        'news': news
    }
    return render(request, 'news/news_detail.html', context=context)


def homePageView(request):
    news_lists=News.published.all().order_by('-published_time')[:15]
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


class LocalNewsView(ListView):
    model = News
    template_name = 'news/local.html'
    context_object_name = 'local_news'

    def get_queryset(self):
        news=self.model.published.all().filter(category__name="Mahalliy")
        return news


class XorijNewsView(ListView):
    model = News
    template_name = 'news/xorij.html'
    context_object_name = 'xorij_news'

    def get_queryset(self):
        news=self.model.published.all().filter(category__name="Xorij")
        return news


class TechnoNewsView(ListView):
    model = News
    template_name = 'news/techno.html'
    context_object_name = 'techno_news'

    def get_queryset(self):
        news=self.model.published.all().filter(category__name="Texnologiya")
        return news


class SportNewsView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_news'

    def get_queryset(self):
        news=self.model.published.all().filter(category__name="Sport")
        return news


class NewsUpdateView(UpdateView):
    model = News
    fields = ('title', 'image', 'category', 'body', 'status',)
    template_name = 'crud/news_edit.html'


class NewsDeleteView(DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')