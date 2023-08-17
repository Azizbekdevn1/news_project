from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Category, News
from .forms import ContactForm
from django.views.generic import TemplateView



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

