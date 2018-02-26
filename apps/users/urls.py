from django.conf.urls import url
from .views import UserCenterView, MyartcileView, UpdatearticleView, AddarticleView, SearchArticleView, MessageView, CategoryView
from .views import OtherSearchView, OtherCenterView, OtherartcileView, OtherMessageView
from article.views import CateView

urlpatterns = [
    url(r'^center/$', UserCenterView.as_view(), name='usercenter'),
    url(r'^article/$', MyartcileView.as_view(), name='myarticle'),
    url(r'^update/(?P<article_id>[0-9]+)$', UpdatearticleView.as_view(), name='update'),
    url(r'^add/$', AddarticleView.as_view(), name='add'),
    url(r'^message/$', MessageView.as_view(), name='message'),
    url(r'^category/$', CategoryView.as_view(), name='category'),
    url(r'^article_search/$', SearchArticleView.as_view(), name='search_article'),

    url(r'^(?P<author_id>[0-9]+)/cate/(?P<category_id>[0-9]+)$', CateView.as_view(), name='cate'),
    url(r'^(?P<author_id>[0-9]+)/usercenter/$', OtherCenterView.as_view(), name='othercenter'),
    url(r'^(?P<author_id>[0-9]+)/myarticle/$', OtherartcileView.as_view(), name='otherarticle'),
    url(r'^(?P<author_id>[0-9]+)/message/$', OtherMessageView.as_view(), name='othermessage'),
    url(r'^art_search/$', OtherSearchView.as_view(), name='othersearch'),
]




