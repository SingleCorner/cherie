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
      group_list = GroupAuthorize.objects.select_related().filter(uid = request.session['user_id'])
      if sid == "":
        grpauth_list = group_list
      else:
        grpauth_list = GroupAuthorize.objects.select_related().filter(gid = sid)
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

def hmc_demo(request):
  return HttpResponse("Hello world")

def data_execute(request):
  result = {}
  try:
    module = request.POST['module']
    action = request.POST['action']  
  except:
    module = ""
    action = ""
    result['code'] = 0
    result['message'] = "拒绝非法访问"
  if module == "group":
    if action == "create":      
      try:
        name = request.POST['addGroup_name']
        group = Group(name=name,
                      uid=Account.objects.get(uid = request.session['user_id']),
                      status=1,
                    )
        group.save()
        inserted_gid = group.gid
        groupauth = GroupAuthorize(gid = Group.objects.get(gid = inserted_gid),
                                   uid = Account.objects.get(uid = request.session['user_id']),
                                   privilege = 0,
                                   )
        groupauth.save()
        result['code'] = 0
        result['message'] = "创建组成功"
      except:
        result['code'] = 1
        result['message'] = "创建组失败"
    else:
      pass
  else:
    pass
  return HttpResponse(json.dumps(result), content_type="application/json")

def rpc_api(request):
  result = {}
  if 'wechat_key' in request.POST and 'request' in request.POST:
    api_token = request.POST['wechat_key']
    api_request = request.POST['request']
    api_command = api_request.split(' ')
    if api_command[0] == "group":
      if len(api_command) > 1:
        api_subcommand = api_command[1]
        try:
          user = Account.objects.filter(wechat_token = api_token, status = 1)
          user_id = user[0].uid
          user_name = user[0].account
        except:
          user_id = ""
        if user_id == "":
          result['code'] = 1
          result['message'] = "尚未绑定平台用户\n[绑定指令]bind account password"
        else:
          if api_subcommand == "list":
            try:
              group_list = GroupAuthorize.objects.select_related().filter(uid = user_id)
              result['code'] = 0
              result['group'] = {}
              i = 0
              for group in group_list:
                if group.privilege == 0:
                  group_auth = "管理"
                elif group.privilege == 1:
                  group_auth = "运维"
                else:
                  group_auth = "查看"
                result['group'][i] = group.gid.name + " - " + group_auth
                i = i + 1
            except:
              result['code'] = 1
              result['message'] = "获取用户组失败，请确定是否已经创建用户组\n联系CSZ9227获取帮助"
          else:
            result['code'] = 1
            result['message'] = "尚未支持的参数"
      else:
        result['code'] = 1
        result['message'] = "group未带有参数\n详细帮助请输入 ?"
    elif api_command[0] == "bind":
      if len(api_command) == 3:
        cherie_account = api_command[1]
        cherie_password = api_command[2]
        try:
          user = Account.objects.filter(account = cherie_account, wechat_token__isnull = True)
          user_id = user[0].uid
        except:
          user = ""
        if user == "":
          result['code'] = 1
          result['message'] = "绑定失败：已绑定，账号不存在"
        else:
          if check_password(cherie_password,user[0].secpasswd):
            try:
              Account.objects.filter(uid = user_id).update(wechat_token = api_token)
              result['code'] = 1
              result['message'] = cherie_account + "用户绑定成功\n欢迎使用本平台"
            except:
              result['code'] = 1
              result['message'] = "绑定失败：多账号绑定"
          else:
            result['code'] = 1
            result['message'] = "绑定失败：密码错误"
      else:
        result['code'] = 1
        result['message'] = "绑定参数出错,输入\nbind 运维平台用户名 运维平台密码"
    else:
      result['code'] = 1
      result['message'] = "尚未支持的指令"
  else:
    result['code'] = 1
    result['message'] = "非法操作"
  return HttpResponse(json.dumps(result),content_type="application/json")

def rpc_api_test(request):
  result = {}
  if 'wechat_key' in request.POST and 'request' in request.POST:
    api_token = request.POST['wechat_key']
    api_request = request.POST['request']
    api_command = api_request.split(' ')
    if api_command[0] == "group":
      if len(api_command) > 1:
        api_subcommand = api_command[1]
        try:
          user = Account.objects.filter(wechat_token = api_token, status = 1)
          user_id = user[0].uid
          user_name = user[0].account
        except:
          user_id = ""
        if user_id == "":
          result['code'] = 1
          result['message'] = "尚未绑定平台用户\n[绑定指令]bind account password"
        else:
          if api_subcommand == "list":
            try:
              group_list = GroupAuthorize.objects.select_related().filter(uid = user_id)
              result['code'] = 0
              result['group'] = {}
              i = 0
              for group in group_list:
                if group.privilege == 0:
                  group_auth = "管理"
                elif group.privilege == 1:
                  group_auth = "运维"
                else:
                  group_auth = "查看"
                result['group'][i] = group.gid.name + " - " + group_auth
                i = i + 1
            except:
              result['code'] = 1
              result['message'] = "获取用户组失败，请确定是否已经创建用户组\n联系CSZ9227获取帮助"
          else:
            result['code'] = 1
            result['message'] = "尚未支持的参数"
      else:
        result['code'] = 1
        result['message'] = "group未带有参数\n详细帮助请输入 ?"
    elif api_command[0] == "bind":
      pass
    else:
      result['code'] = 1
      result['message'] = "尚未支持的指令"
  else:
    result['code'] = 1
    result['message'] = "非法操作"
  return HttpResponse(json.dumps(result),content_type="application/json")
