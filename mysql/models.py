# -*- coding: utf-8 -*-
# coding:utf8
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Account(models.Model):
  uid = models.IntegerField(primary_key=True)
  account = models.CharField(unique=True, max_length=15, blank=True)
  secpasswd = models.CharField(max_length=80, blank=True)
  tel = models.CharField(max_length=11, blank=True)
  mail = models.CharField(max_length=40, blank=True)
  status = models.IntegerField(blank=True, null=True)
  regist_time = models.CharField(max_length=20, blank=True)
  class Meta:
      db_table = 'Account'

class Group(models.Model):
  gid = models.IntegerField(primary_key=True)    
  name = models.CharField(max_length=10, blank=True)
  uid = models.ForeignKey(Account, db_column='uid')
  class Meta:
      db_table = 'Group'

class GroupAuthorize(models.Model):
  id = models.IntegerField(primary_key=True)    
  gid = models.ForeignKey(Group, db_column='gid')
  uid = models.ForeignKey(Account, db_column='uid')
  privilege = models.IntegerField()
  class Meta:
      db_table = 'GroupAuthorize'

