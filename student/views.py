from django.shortcuts import render
from django.views.generic import View


class IndexView(View):
    temp_dir = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        return render(request, self.temp_dir, {'test':'test'})
