from django.urls import path
from rate_my_walk import views

app_name = 'rate_my_walk'

urlpatterns = [
    #general urls
    path('', views.index, name='index'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('about/', views.about, name='about'),
    #walk urls
    path('walks/', views.walks, name='walks'),
    path("walks/<slug:walk_name_slug>/", views.showWalk, name='showWalk'),
    path("walks/<slug:walk_name_slug>/more-images/", views.moreImages, name='more_images'),
    path("walks/<slug:walk_name_slug>/rate-walk/", views.rateWalk, name='rateWalk'),
    path("upload/", views.uploadWalk, name='uploadWalk'),
    path("walks/edit/<slug:walk_name_slug>/", views.editWalk, name='edit_walk'),
    #profile urls
    path('register_profile/', views.register_profile,name='register_profile'),
    path('profile/<username>/',views.ProfileView.as_view(),name='profile'),
    path('walkers/',views.ListProfilesView.as_view(), name='list_walkers'),
    #like button url
    path('like_walk/', views.LikeWalk.as_view(), name='like_walk'),
]