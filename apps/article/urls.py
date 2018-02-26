from django.conf.urls import url
from article.views import ArticleView, CommentView, SearchView

urlpatterns = [
    url(r'(?P<article_id>[0-9]+)$', ArticleView.as_view(), name='article'),
    url(r'^comment/$', CommentView.as_view(), name='comment'),
    url(r'^search/$', SearchView.as_view(), name='search'),
]




