from django.views.generic import ListView
from centre.models import Article


# Create your views here.
class ArticleListView(ListView):
    queryset = Article.objects.all()
    context_object_name = 'posts'
    paginate_by = 10
    template_name = 'submit_line.html'
