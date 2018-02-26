from django.db import models
from datetime import datetime
from users.models import UserProfile
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


class Category(models.Model):
    Create_Time = models.DateTimeField(verbose_name=u'创建时间', default=datetime.now)
    Category = models.CharField(verbose_name='分类', max_length=15)
    Article_Num = models.IntegerField(verbose_name='文章数', default=0)
    User = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='分类用户', null=True)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.Category


class Article(models.Model):
    Create_Time = models.DateTimeField(verbose_name=u'创建时间', default=datetime.now)
    Modify_Time = models.DateTimeField(verbose_name=u'修改时间', null=True, auto_now=True)
    Click_Num = models.IntegerField(verbose_name=u'点击量', default=0)
    Tittle = models.CharField(verbose_name=u'标题', null=True, max_length=20)
    Cover_img = models.ImageField(verbose_name=u'封面图片', upload_to="image/%Y/%m", default=u"image/default.png")
    Content = RichTextUploadingField(verbose_name='内容', default='')
    Author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='Author', verbose_name='作者')
    Article_Category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='Article_Category', null=True, verbose_name='文章分类')
    Label = models.CharField(verbose_name='标签', max_length=10, null=True)

    class Meta:
        verbose_name = u'文章'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.Tittle


class Comment(models.Model):
    Create_Time = models.DateTimeField(verbose_name=u'创建时间', null=True, auto_now=True)
    Content = models.CharField(verbose_name='评论内容', max_length=100)
    Comment_Article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='Article_id')
    Comment_ComId = models.IntegerField(verbose_name='被评论用户', default=0)
    Like_Num = models.IntegerField(verbose_name='点赞量', default=0)
    IP = models.CharField(verbose_name='Ip地址', max_length=15, null=True)
    Comment_Address = models.CharField(verbose_name='地址', max_length=10, null=True)
    Comment_User = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='评论用户', null=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.id


class RecommendArticle(models.Model):
    Recommend_Article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='推荐文章')
    Create_Time = models.DateTimeField(verbose_name=u'创建时间', default=datetime.now)

    class Meta:
        verbose_name = '推荐文章'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.Recommend_Article.Tittle






