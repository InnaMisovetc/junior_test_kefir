from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('user_session.urls')),
    path('admin/', admin.site.urls),
    path('users', include('users.urls')),
    path('private/users', include('users_administration.urls'))
]
