from django.shortcuts import render
from django.views.generic.base import View
from .models import Article, Comment, Category
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from users.models import UserProfile
from django.contrib.auth.decorators import login_required
# Create your views here.


class IndexView(View):
    def get(self, request):
        # 文章
        articles = Article.objects.all()
        hot_article = articles.order_by('-Click_Num')
        articles = articles.order_by('-Create_Time')
        new_article = articles[:8]
        page = request.GET.get('page', '')
        paginator = Paginator(articles, 6)
        if not page:
            articles = paginator.page(1)
        else:
            try:
                articles = paginator.page(page)
            except EmptyPage:
                articles = paginator.page(1)
            except PageNotAnInteger:
                articles = paginator.page(1)

        # 文章分类
        category = Category.objects.all()

        return render(request, 'index.html', {
            'articles': articles,
            'category': category,
            'new_article': new_article,
            'range': paginator.page_range,
            'cur_page': articles.number,
            'page_num': paginator.num_pages,
            'hot_article': hot_article
        })


class ArticleView(View):
    def get(self, request, article_id):
        article = Article.objects.get(pk=article_id)
        if request.user != article.Author:
            article.Click_Num = int(article.Click_Num) + 1
            article.save()
        comments = Comment.objects.filter(Comment_Article=article).order_by('-Create_Time')
        author = article.Author
        article_author = Article.objects.filter(Author=author).order_by('-Create_Time')[:10]
        article_count = Article.objects.filter(Author=author).count()
        comment_count = Comment.objects.filter(Comment_User=author).count()
        cate = Category.objects.filter(User=author)
        return render(request, 'Article.html', locals())


class CommentView(View):
    """
    用户添加客户评论
    """
    def post(self, request):
        if not request.user.is_authenticated():
            return render(request, 'login.html')
        article_id = request.POST.get('article_id', 0)
        comment_content = request.POST.get('comment_cont', "")
        if int(article_id) > 0 and comment_content:
            comment = Comment()
            article = Article.objects.get(pk=int(article_id))
            comment.Comment_Article = article
            comment.Content = comment_content
            comment.Comment_ComId = article.Author.id
            comment.Comment_User = request.user
            comment.save()
            return HttpResponse('{"status": "success", "msg": "评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "评论失败"}', content_type='application/json')


class SearchView(View):
    def get(self, request):
        search = request.GET.get('keywords', "")
        search_article = Article.objects.all()
        if search:
            search_article = search_article.filter(Q(Tittle__icontains=search) | Q(Content__icontains=search))
        return render(request, 'Search.html', {'articles': search_article, 'keywords': search})


class CateView(View):
    def get(self, request, author_id, category_id):
        category = Category.objects.get(pk=category_id)
        author = UserProfile.objects.get(pk=author_id)
        article_author = Article.objects.filter(Author=author).order_by('-Create_Time')[:10]
        article_count = Article.objects.filter(Author=author).count()
        comment_count = Comment.objects.filter(Comment_User=author).count()
        cate = Category.objects.filter(User=author)
        articles = ''
        if category.Article_Num != 0:
            articles = Article.objects.filter(Author=author)
        return render(request, 'Category.html', locals())


