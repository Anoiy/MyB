from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


# 继承原有user模板类
class UserProfile(AbstractUser):
    Avatar = models.ImageField(upload_to="image/%Y/%m", default=u"image/default.png", max_length=100, verbose_name=u'头像')
    Birthday = models.DateField(verbose_name='生日', null=True, default='1111-11-11')
    Sex = models.CharField(choices=(('男', 'male'), ('女', 'female')), max_length=6, default='男')
    Nickname = models.CharField(verbose_name='昵称', max_length=8, null=True, default='')
    Job = models.CharField(verbose_name='工作', max_length=25, null=True, default='')
    Education = models.CharField(verbose_name='教育经历', max_length=25, null=True, default='')
    Familiar = models.CharField(verbose_name='熟悉领域', max_length=25, null=True, default='')
    Interview_Num = models.IntegerField(verbose_name='访问量', default=0)

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username



