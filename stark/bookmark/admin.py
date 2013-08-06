# __*__ coding:utf-8 __*__

from django.contrib import admin
from models import Bookmark
from models import Tag
from models import Link
from models import Test
from models import FriendShip
from models import Invitation
from models import CaptchaStorage
from models import RegistrationProfile
'''
class BookmarkAdmin(admin.ModelAdmin):
    pass

    list_display = {'title','link','user','date','description','shared'}
    search_fields = {'title',}

class TagAdmin(admin.ModelAdmin):
    list_display = {'name',}

class LinkAdmin(admin.ModelAdmin):
    list_display = {'url'}
    search_fields = {'url',}
'''
#admin.site.register(Test)



#将Model 在djangoAdmin中注册 （两个条件 1.在model中重写 Admin内部类,Meta内部类 2.编写 ModelManger方法）
admin.site.register(Tag)
admin.site.register(Link)
admin.site.register(Bookmark)
admin.site.register(Invitation)
admin.site.register(FriendShip)
#admin.site.register(CaptchaStorage)
#admin.site.register(RegistrationProfile)
