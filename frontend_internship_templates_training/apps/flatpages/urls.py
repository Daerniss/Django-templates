from django.urls import path

from flatpages import views


urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('sitemap/', views.SitemapView.as_view(), name='sitemap'),
    path('articles/', views.ArticleListView.as_view(), name='articles'),
    path('articles/<str:slug>/', views.ArticleDetailView.as_view(), name='article'),
    path('flatpages/<str:slug>/', views.FlatPageDetailView.as_view(), name='flatpage'),
    path('faq/', views.SupportCenterView.as_view(), name='support'),
    path('contact-us/', views.ContactUsView.as_view(), name='contact-us'),
    path('accounts/register/', views.RegisterView.as_view(), name='register'),
]
