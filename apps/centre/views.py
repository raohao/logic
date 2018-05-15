from django.views.generic import ListView
from centre.models import RiskClosure
from django.http import HttpResponse


# Create your views here.
def home(response, *args, **kwargs):
    return HttpResponse('Hello world!')


class ArticleListView(ListView):
    queryset = RiskClosure.object.all()
    context_object_name = 'posts'
    paginate_by = 10
    template_name = 'submit_line.html'
