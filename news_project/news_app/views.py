from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from hitcount.utils import get_hitcount_model
from .forms import ContactForm, CommentForm
from .models import Category, News
from news_project.custom_permessions import OnlyloggedSuperUser

def news_list(request):
    news_lists = News.published.all()  # 2-usul
    context = {
        "news_lists": news_lists
    }
    return render(request, 'news/news_list.html', context=context)



from hitcount.views import HitCountDetailView, HitCountMixin


#@login_required
def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {

    }#hit count logic
    hit_count=get_hitcount_model().objects.get_for_object(news)
    hits=hit_count.hits
    hitcontext=context['hitcount']={'pk': hit_count.pk}
    hit_count_response=HitCountMixin.hit_count(request,hit_count)
    if hit_count_response.hit_counted:
        hits=hits+1
        hitcontext['hit_counted']=hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits


    comments=news.comments.filter(active=True)
    comment_count=comments.count()
    new_comment=None
    if request.method == "POST":
        comment_form =CommentForm(data=request.POST)
        if comment_form.is_valid():
            #Yangi komment obketini yaratamiz lekin DB ga saqlamaymiz
            new_comment=comment_form.save(commit=False)
            new_comment.news=news
            new_comment.user=request.user
            #izoh egasini so'rov yuborayotgan userga bog'ladik
            new_comment.save()
            #ma'lumotlar bazasiga saqladik
            comment_form=CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        'news': news,
        'comments':comments,
        'comment_count': comment_count,
        'new_comment':new_comment,
        'comment_form':comment_form
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


class NewsUpdateView(OnlyloggedSuperUser,UpdateView):
    model = News
    fields = ('title', 'image', 'category', 'body', 'status',)
    template_name = 'crud/news_edit.html'

class NewsDeleteView(LoginRequiredMixin,DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')


class NewsCreateView(OnlyloggedSuperUser,CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title','slug', 'image', 'category', 'status','body' )
    success_url = reverse_lazy('home_page')



@user_passes_test(lambda u: u.is_superuser)
#Faqat super userlar admin pageni kora olishi uchun dekorator
@login_required
def admin_page(request):
    admin_users=User.objects.filter(is_superuser=True)
    context={
        'admin_users': admin_users
    }
    return render(request, 'pages/admin_page.html',context)

class SearchResultListView(ListView):
    model=News
    template_name='news/search_results.html'
    context_object_name = "Barcha_yangiliklar"

    def queryset(self):
        query=self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )

