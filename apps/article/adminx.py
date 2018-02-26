import xadmin
from xadmin import views
from .models import Article, Category, Comment


class BassSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "Blog"
    site_footer = "Blog"
    menu_style = "accordion"


class ArticleAdmin(object):
    pass


class CategoryAdmin(object):
    pass


class CommentAdmin(object):
    pass


xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(Comment, CommentAdmin)
xadmin.site.register(views.BaseAdminView, BassSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)











