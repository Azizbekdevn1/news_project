from django.urls import path
from .views import*

urlpatterns = [
    path('',HomePageView.as_view(),name='home_page'),
    path('all/', news_list, name='news_list'),
    path('news/<slug:news>', news_detail, name='news_detail'),
    path('contact-us/', ContactPageView.as_view(),name='contact_page'),
    path('local/',LocalNewsView.as_view(),name='local_news_page'),
    path('sport/', SportNewsView.as_view(), name='sport_news_page'),
    path('xorij/', XorijNewsView.as_view(), name='xorij_news_page'),
    path('techno/', TechnoNewsView.as_view(), name='techno_news_page'),
]

