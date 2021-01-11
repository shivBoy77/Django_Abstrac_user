from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from accounts.views import login_view, register_view, HomeView, logout_view
# from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(HomeView.as_view()), name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name="logout"),
    path('register/', register_view, name='register'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
