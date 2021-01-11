from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


@method_decorator(login_required, name='dispatch')
class ProfileTemplateView(TemplateView):
    template_name = "registration/profile.html"

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)


class AboutTemplateView(TemplateView):
    template_name = "home/about.html"


@method_decorator(staff_member_required, name='dispatch')
class StaffTemplateView(TemplateView):
    template_name = "registration/staff.html"
    # @method_decorator(staff_member_required)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)


# EXETRA
decorators = [never_cache, login_required, staff_member_required]
@method_decorator(decorators, name='dispatch')
class ClassViewsArePro(TemplateView):
    template_name = "howareyou.html"


# Classes


# def my_view(request):
#     # if request.method == 'GET':
#     #     # <view logic>
#     return HttpResponse('result')
