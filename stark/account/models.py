#-*- coding:utf-8 -*-
from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile
from userena.managers import UserenaBaseProfileManager
from userena.managers import UserenaManager
from friend.models import FriendShip
from bookmark.models import Tag,Bookmark
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.base import ObjectDoesNotExist

class MyProfileManager(UserenaBaseProfileManager):
    def is_fans(self,**kwargs):
        username = kwargs['username']
        try:
            user_id = User.objects.get(username = username)
        except:
            user_id = None
        
        ex_username = kwargs['ex_username']
        try:
            ex_id = User.objects.get(username = ex_username)
        except:
            ex_id = None
        if ex_id and user_id:
            try:
                a  = FriendShip.objects.get(to_friend = user_id,from_friend = ex_id)
                return True
            except ObjectDoesNotExist:
                return False
        else:
            return False

    def is_follows(self,**kwargs):
        username = kwargs['username']
        ex_username = kwargs['ex_username']
        try:
            ex_id = User.objects.get(username = ex_username)
        except:
            ex_id = None
        try:
            id = User.objects.get(username = username)
        except:
            id = None
        if id and ex_id:
            try:
                a = FriendShip.objects.get(to_friend = ex_id,from_friend = id)
                return True
            except ObjectDoesNotExist:
                return False
        else:
            return False        


    def fans_follows(self,**kwargs):
        pass


    def get_fans_count(self,**kwargs):
        username = kwargs.get('username')
        ex_username = kwargs.get('ex_username')  
        if username:
            try:
                user = User.objects.get(username = username )
            except:
                user = None
        elif ex_username:
            try:
                user = User.objects.get(username = ex_username )
            except:
                user = None
        else:
            return 0
        
        fans_count = user.friend_set.all().count()
        return fans_count
            
    def get_follows_count(self,**kwargs):
        username = kwargs.get('username')
        ex_username = kwargs.get('ex_username')
        
        if username:
            try:
                user = User.objects.get(username = username )
            except:
                user = None
        elif ex_username:
            try:
                user = User.objects.get(username = ex_username )
            except:
                user = None
        else:
            return 0
        
        follow_count = user.to_friend_set.all().count()
        return follow_count
    
    def get_info(self,**kwargs):
        username = kwargs.get('username')
        ex_username = kwargs.get('ex_username')
        return {'fans_count':self.get_fans_count(username = ex_username),
                'follows_count':self.get_follows_count(username = ex_username),
                'is_follows':self.is_follows(username = username,ex_username = ex_username),
                'is_fans':self.is_fans(username = username,ex_username = ex_username),
                'tag_count':Tag.objects.user_tag_counts(ex_username),
                'bookmark_count':Bookmark.objects.get_user_bookmark_count(ex_username),
                }

    def get_fans_list(self,**kwargs):
        username = kwargs.get('username',None)
        ex_username = kwargs.get('ex_username',None)
        if ex_username:
            try:
                user = User.objects.get(username = ex_username)
            except ObjectDoesNotExist:
                user = None
        else :
            try:
                user = User.objects.get(username = username)
            except ObjectDoesNotExist:
                user = None
        if user:
            fans = user.friend_set.all()
            if fans.count() > 0:
                return ({'user':item.to_friend,'info':self.get_info(username = username,ex_username = item.to_friend.username)
                                               } for item in fans) 
        
    def get_follows_list(self,**kwargs):
        username = kwargs.get('username')
        ex_username = kwargs.get('ex_username')
        if kwargs.has_key('ex_username'):
            try:
                user = User.objects.get(username = ex_username)
            except ObjectDoesNotExist:
                user = None
        else:
            try:
                user = User.objects.get(username = username)
            except ObjectDoesNotExist:
                user = None
        if user:
            follows = user.to_friend_set.all()
            if follows.count() > 0:
                return ({'user':item.from_friend,'info':self.get_info(username = username,ex_username = item.from_friend.username)} for item in follows)


    def get_same_follows_list(self,**kwargs):
        if kwargs.has_key('username') and kwargs.has_key('ex_username'):
            username,ex_username = [item for item in kwargs.itervalues()]
            list1 = self.get_follows_list(username = username)
            list2 = self.get_follows_list(ex_username = ex_username)
            same_follows = ({'user':item,'info':self.get_info(username = username,ex_username = item.username)} for item in list1 if item in list2 )
            if len(list(same_follows)) >0 :
                return same_follows
        else:
            pass

    #我关注的人也关注他
    def get_second_follows_list(self,**kwargs):
        if kwargs.has_key('username') and kwargs.has_key('ex_username'):
            username,ex_username = [item for item in kwargs.itervalues()]
            list1 = self.get_follows_list(username = username)
            list2 = self.get_fans_list(ex_username = ex_username)
            second_follows = ({'user':item,'info':self.get_info(username = username,ex_username = item.username)} for item in list1 if item in list2)
            if len(list(second_follows)) > 0:
                return second_follows
        else:
            pass

class MyProfile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='my_profile')
    favourite_snack = models.CharField(_('favourite snack'),
                                       max_length=5)
    objects = MyProfileManager()

