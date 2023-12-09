from django.urls import path
from .views import*
from . import views
urlpatterns = [
    path('',HomePageView.as_view(),name='home_page'),
    path('all/', news_list, name='news_list'),
    path('news/<slug:news>', news_detail, name='news_detail'),
    path('news/<slug>/edit/', NewsUpdateView.as_view(), name='news_update'),
    path('news/<slug>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('contact-us/', ContactPageView.as_view(),name='contact_page'),
    path('local/',LocalNewsView.as_view(),name='local_news_page'),
    path('sport/', SportNewsView.as_view(), name='sport_news_page'),
    path('xorij/', XorijNewsView.as_view(), name='xorij_news_page'),
    path('techno/', TechnoNewsView.as_view(), name='techno_news_page'),
    path('adminpage/',admin_page,name='admin_page'),
    path('searchresult/', SearchResultListView.as_view(), name='search_result'),
]

