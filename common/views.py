# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.hashers import *

import hashlib, random, string, re
import datetime, time
#import json, netsnmp
import json

from mysql.models import Account

def USER_LOGIN(request):
    if 'loginToken' in request.session:
      rsp = render(request, 'user_index.html', locals())
      return HttpResponse(rsp)
    else:
        if 'act' in request.GET and request.GET['act'] == "login":
          user = request.POST['username']
          passwd = request.POST['password']
          user_query = Account.objects.filter(account = user, status = 1)
          if user_query:
            local_passwd = user_query[0].secpasswd
          else:
            local_passwd = ""
          if check_password(passwd,local_passwd):
            result = {}
            result['code'] = 0
            request.session['loginToken'] = "True"
            request.session['logoutAuth'] = "".join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], 4)).replace(' ','').upper()
            request.session['user_id'] = user_query[0].id
            request.session['user_name'] = user_query[0].name
            #判断后台进入权限
            if user_query[0].authorize == "1":
              request.session['user_admin'] = True
            else:
              request.session['user_admin'] = False
            #判断项目权限
            if user_query[0].module == "-1":
              request.session['user_sys'] = True
            else:
              request.session['user_sys'] = False
              request.session['user_proj'] = user_query[0].module
          else:
            result = {}
            result['code'] = -1
            result['message'] = "用户验证出错，请联系管理员"
          return HttpResponse(json.dumps(result), content_type="application/json")
          #return HttpResponse(local_passwd)
        else:
          timestamp = time.time()
          request.session['loginTime'] = timestamp

          rsp = render(request, 'login.html', locals())
          return HttpResponse(rsp)

def USER_LOGOUT(request):
  if 'key' in request.GET and 'logoutAuth' in request.session and request.GET['key'] == request.session['logoutAuth']:
    request.session.clear()
  return HttpResponseRedirect('/')