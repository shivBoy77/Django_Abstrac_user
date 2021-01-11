from django.urls import path
from registeration.views import ProfileTemplateView, StaffTemplateView

urlpatterns = [
    path('profile/', ProfileTemplateView.as_view(), name='profile'),
    path('staff/', StaffTemplateView.as_view(), name='staff'),
]
