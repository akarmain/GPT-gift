from django.contrib import admin
from django.urls import path, re_path

from main import views
from django.contrib.auth import views as auth_views

from main.views import LoginUser, logout_user, RegisterUser
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as mediaserve

urlpatterns = [
    path('admin', admin.site.urls),
    path('', views.index_page, name='index'),
    path('time', views.time_page, name='time'),
    path('my_polls', views.user_polls, name='user_polls'),
    path('new_poll/', views.new_poll, name='new_poll'),
    path('poll_creation/<poll_number>', views.poll_creation, name='poll_creation'),
    path('poll_results/<poll_number>', views.poll_results, name='poll_results'),
    path('delete_poll/<poll_number>', views.delete_poll, name='delete_poll'),
    path('polls/<poll_slug>', views.poll_completion, name="poll_completion"),

    path('login/', LoginUser.as_view(), name='login'),
    path('logout', logout_user, name='logout'),
    path('register', RegisterUser.as_view(), name='register'),
    path('all_gifts', views.all_gifts, name='all_gifts'),
]
if settings.DEBUG:
       urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   
