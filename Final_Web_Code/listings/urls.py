from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='listings'),
    path('<int:listing_id>', views.listing, name='listing'),
    path('listing_old/<int:listing_id>', views.listing_old, name='listing_old'),

    path('search', views.search, name='search'),

    path('listing_div', views.index_div, name='listing_div'),
    path('listing_div/<int:listing_div_id>', views.listing_div, name='listing_div'),
    path('search_div/<int:listing_div_id>/',views.search_div, name='search_div'),

    path('listing_div_old', views.index_div_old, name='listing_div_old'),
    path('listing_div_old/<int:listing_div_id>', views.listing_div_old, name='listing_div_old'),
    path('search_div_old/<int:listing_div_id>/', views.search_div_old, name='search_div_old')


]
