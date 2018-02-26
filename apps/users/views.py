from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View
from .models import UserProfile
from django.db.models import Q
from django.http import HttpResponseRedirect
from .forms import LoginForm, RegisterForm
from article.forms import AddArticleForm
from django.contrib.auth.hashers import make_password
from article.models import Article, Category, Comment
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class TestView(View):
    def get(self, request):
        return render(request, 'text.html')


# 复写authenticate方法
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated():
            logout(request)
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.POST.get('next', '/') or '/')
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = UserProfile()
            user.username = username
            user.password = make_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            login(request, user)
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
            return render(request, 'index.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


class UserCenterView(View):
    def get(self, request):
        user = request.user
        article_count = Article.objects.filter(Author=user).count()
        comment_count = Comment.objects.filter(Comment_User=user).count()
        return render(request, 'center/index.html', locals())

    def post(self, request):
        userprofile = request.user
        nickname = request.POST.get('nickname', '')
        sex = request.POST.get('sex', '男')
        birthday = request.POST.get('birthday', '')
        job = request.POST.get('job', '')
        familiar = request.POST.get('familiar', '')
        education = request.POST.get('education', '')
        if 'avatar' in request.FILES:
            userprofile.Avatar = request.FILES['avatar']
        userprofile.Nickname = nickname
        userprofile.Sex = sex
        userprofile.Birthday = birthday
        userprofile.Job = job
        userprofile.Familiar = familiar
        userprofile.Education = education
        userprofile.save()
        return render(request, 'center/index.html', {'user': userprofile})


class OtherCenterView(View):
    def get(self, request, author_id):
        user = UserProfile.objects.get(pk=author_id)
        if request.user != user:
            user.Interview_Num = int(user.Interview_Num) + 1
            user.save()
        article_count = Article.objects.filter(Author=user).count()
        comment_count = Comment.objects.filter(Comment_User=user).count()
        return render(request, 'Other/index.html', locals())


class MyartcileView(View):
    def get(self, request):
        user = request.user
        articles = Article.objects.filter(Author=user)
        return render(request, 'center/article.html', {'articles': articles})

    def post(self, request):
        article_id = request.POST.get('article_id', '')
        if article_id:
            article = Article.objects.get(pk=article_id)
            article.delete()
        user = request.user
        articles = Article.objects.filter(Author=user)
        return render(request, 'center/article.html', {'articles': articles})


class OtherartcileView(View):
    def get(self, request, author_id):
        user = UserProfile.objects.get(pk=author_id)
        articles = Article.objects.filter(Author=user)
        return render(request, 'Other/article.html', {'articles': articles, 'author': user})


class UpdatearticleView(View):
    def get(self, request, article_id):
        article = Article.objects.get(pk=article_id)
        category = Category.objects.filter(User=request.user)
        return render(request, 'center/update-article.html', {'article': article, 'category': category})

    def post(self, request, article_id):
        article = Article.objects.get(pk=article_id)
        tittle = request.POST.get('title', '')
        content = request.POST.get('editor1', '')
        if 'cover_img' in request.FILES:
            cover_img = request.FILES['cover_img']
            article.Cover_img = cover_img
        category_id = request.POST.get('category', '')
        label = request.POST.get('tags', '')

        if category_id:
            category = Category.objects.get(pk=category_id)
            if article.Article_Category:
                old_cate = Category.objects.get(Category=article.Article_Category.Category)
                old_cate.Article_Num = int(old_cate.Article_Num) - 1
                old_cate.save()
            category.Article_Num = int(category.Article_Num) + 1
            category.save()
            article.Article_Category = category
        article.Tittle = tittle
        article.Content = content
        article.Label = label
        user = request.user
        article.Author = user
        article.save()
        articles = Article.objects.filter(Author=user)
        return render(request, 'center/article.html', {'articles': articles})


class AddarticleView(View):
    def get(self, request):
        now = datetime.now()
        user = request.user
        category = Category.objects.filter(User=user)
        return render(request, 'center/add-article.html', {'now': now, 'category': category})

    def post(self, request):
        article_form = AddArticleForm(request.POST, request.FILES)
        user = request.user
        if 'cover_img' in request.FILES:
            article = Article()
            tittle = request.POST.get('title', '')
            content = request.POST.get('editor1', '')
            cover_img = request.FILES['cover_img']
            category_id = request.POST.get('category', '')
            label = request.POST.get('tags', '')
            if category_id:
                category = Category.objects.get(pk=category_id)
                article.Article_Category = category
                category.Article_Num = int(category.Article_Num) + 1
                category.save()
            article.Tittle = tittle
            article.Content = content
            article.Cover_img = cover_img
            article.Author = user
            article.Label = label
            article.save()
            articles = Article.objects.filter(Author=user)
            return render(request, 'center/article.html', {'articles': articles})
        else:
            now = datetime.now()
            category = Category.objects.filter(User=user)
            return render(request, 'center/add-article.html', {'now': now, 'category': category})


class MessageView(View):
    def get(self, request):
        user = request.user
        comment = Comment.objects.filter(Comment_ComId=user.id).order_by('-Create_Time')
        return render(request, 'center/comment.html', {'comment': comment})

    def post(self, request):
        comment_id = request.POST.get('id', '')
        if comment_id:
            Comment.objects.get(pk=comment_id).delete()
        user = request.user
        comment = Comment.objects.filter(Comment_ComId=user.id).order_by('-Create_Time')
        return render(request, 'center/comment.html', {'comment': comment})


class OtherMessageView(View):
    def get(self, request, author_id):
        user = UserProfile.objects.get(pk=author_id)
        comment = Comment.objects.filter(Comment_ComId=user.id).order_by('-Create_Time')
        return render(request, 'Other/comment.html', {'comment': comment, 'author': user})


class CategoryView(View):
    def get(self, request):
        user = request.user
        category = Category.objects.filter(User=user)
        return render(request, 'center/notice.html', {'category': category})

    def post(self, request):
        send_type = request.POST.get('type', '')
        user = request.user
        if send_type == 'delete':
            cate_id = request.POST.get('id', '')
            Category.objects.get(pk=cate_id).delete()
            category = Category.objects.filter(User=user)
            return render(request, 'center/notice.html', {'category': category})
        elif send_type == 'see':
            cate_id = request.POST.get('id', '')
            cate = Category.objects.get(pk=cate_id)
            articles = cate.Article_Category.filter(Author=user)
            category = Category.objects.filter(User=user)
            return render(request, 'center/cate.html', {'category': category, 'articles': articles})
        elif send_type == 'update':
            old = request.POST.get('old', '')
            new = request.POST.get('new', '')
            category = Category.objects.get(pk=old)
            category.Category = new
            category.save()
            category = Category.objects.filter(User=user)
            return render(request, 'center/notice.html', {'category': category})
        else:
            cate = request.POST.get('cate', '')
            category = Category()
            category.Category = cate
            category.User = user
            category.save()
            category = Category.objects.filter(User=user)
            return render(request, 'center/notice.html', {'category': category})


class SearchArticleView(View):
    def post(self, request):
        keyword = request.POST.get('keyword', '')
        articles = Article.objects.filter(Author=request.user, Tittle__contains=keyword)
        return render(request, 'center/search_article.html', {'articles': articles})


class OtherSearchView(View):
    def post(self, request):
        keyword = request.POST.get('keyword', '')
        articles = Article.objects.filter(Author=request.user, Tittle__contains=keyword)
        return render(request, 'Other/search_article.html', {'articles': articles})


