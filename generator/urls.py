from django.urls import path, include
from . import views

#Change URL paths here:

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:band_id>/', views.BandSongsView.as_view(), name='bandsongs'),
    path('<int:band_id>/songs/<int:num_songs>/slow_songs/<int:num_slow_songs>/encores/<int:num_encores>/start_song/<str:start_song>', views.SetlistView.as_view(), name='setlists'),
    ###########---NEW VIEW---###############
    path('band/', views.band_list),
    path('band/<int:band_id>', views.band_detail),
]
