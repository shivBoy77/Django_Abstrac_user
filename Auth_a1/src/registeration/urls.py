from django.urls import path
from registeration.views import ProfileTemplateView, StaffTemplateView
from registeration import views
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
urlpatterns = [
    path('profile/', login_required(ProfileTemplateView.as_view()), name='profile'),
    path('staff/', staff_member_required(StaffTemplateView.as_view()), name='staff'),
]
