from django.urls import path
from .views import news_list, news_detail,homePageView,ContactPageView,HomePageView

urlpatterns = [
    path('',HomePageView.as_view(),name='home_page'),
    path('all/', news_list, name='news_list'),
    path('news/<slug:news>', news_detail, name='news_detail'),
    path('contact-us/', ContactPageView.as_view(),name='contact_page'),
]

