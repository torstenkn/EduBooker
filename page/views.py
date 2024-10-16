from django.shortcuts import render
from django.views import View

# Create your views here.
class MainView(View):
    # noinspection PyMethodMayBeStatic
    def get(self, request):

        context = {
        #    'response': airesponse,
        }

        return render(request, 'page/home.html', context)
