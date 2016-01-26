# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.hashers import *
from django.core.paginator import Paginator

import hashlib, random, string, re
import datetime, time
#import json, netsnmp
import json

from mysql.models import *

def user_signup(request):
  if 'act' in request.POST and request.POST['act'] == "signup":
    account = request.POST['username']
    passwd = make_password(request.POST['password'], None, 'pbkdf2_sha256')
    date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    try:
      obj = Account(account=account,
                    secpasswd=passwd,
                    status=1,
                    regist_time=date,
                    )
      obj.save()
      result = {}
      result['code'] = 1
      result['message'] = date
    except:
      result = {}
      result['code'] = -1
      result['message'] = "注册失败"
    return HttpResponse(json.dumps(result), content_type="application/json")
  else:
    return HttpResponseRedirect('/')

def user_signin(request):
  if 'loginToken' in request.session:
    return HttpResponseRedirect('/user/summary')
  else:
    if 'act' in request.POST and request.POST['act'] == "signin":
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
        request.session['loginToken'] = "LoginAccess"
        request.session['logoutAuth'] = "".join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], 4)).replace(' ','').upper()
        request.session['user_id'] = user_query[0].uid
        request.session['user_name'] = user_query[0].account
        #判断后台进入权限
        if user_query[0].uid == 1:
          request.session['user_admin'] = 1
        else:
          request.session['user_admin'] = 0
      else:
        result = {}
        result['code'] = -1
        result['message'] = "用户验证出错，请联系管理员"
      return HttpResponse(json.dumps(result), content_type="application/json")
    else:
      return HttpResponseRedirect('/user/summary')

def user_signout(request):
  if 'key' in request.GET and 'logoutAuth' in request.session and request.GET['key'] == request.session['logoutAuth']:
    request.session.clear()
    return HttpResponseRedirect('/')
  else:
    return HttpResponse('There is a wrong signout operation')

def user_dashboard(request):
  if 'loginToken' in request.session:
    return HttpResponseRedirect('/user/summary')
  else:
    timestamp = time.time()
    request.session['loginTime'] = timestamp

    rsp = render(request, 'login.html', locals())
    return HttpResponse(rsp)

def user_module(request, module, sid):
  if 'loginToken' in request.session:
    if module == "groups":
      group_list = Group.objects.filter(uid = request.session['user_id'])
      grpauth_list = GroupAuthorize.objects.select_related().filter(uid = request.session['user_id'])
      rsp = render(request, 'user_groups.html', locals())
      return HttpResponse(rsp)
    elif module == "assets":
      group_list = Group.objects.all()
      rsp = render(request, 'developing.html', locals())
      return HttpResponse(rsp)
    else:
      rsp = render(request, 'developing.html', locals())
      return HttpResponse(rsp)
  else:
    return HttpResponseRedirect('/')

def admin_module(request, module, sid):
  rsp = render(request, 'developing.html', locals())
  return HttpResponse(rsp)
