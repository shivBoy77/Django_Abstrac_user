from django.contrib import admin
from django.urls import path, include
# for home view only
from registeration import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('registeration.urls')),
    # about view here.
    path('about/', views.AboutTemplateView.as_view(), name="about")
]
