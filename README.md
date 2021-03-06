#环境搭建须知
  由于本平台使用python3，使用pymysql作为mysql操作类，部署使用有任何问题，请邮件联系我。
  需要在django的配置包里面将mysql复制成pymysql，将base.py里面的MySQLdb改成pymysql，将introspection.py里面的MySQLdb改成pymysql。

[![Build Status](http://ops.siner.us:8080/buildStatus/icon?job=production_cherie_deploying)](http://ops.siner.us:8080/job/production_cherie_deploying)

# 平台介绍
  - 自动化运维平台，基于AutoO_with_django进行重写，并将本平台更名为cherie。为什么更名了呢？原因到时候将发布至博客，总之就是更名啦。
  - 从PHP版本到python2版本到现在为了能兼容目前的python3,这已经是第三次重写了。实际上也不能说是重写吧，前面2个版本都没开发完，只是在新版本上做了优化，加入了新功能，应该说是升级吧。
  - 本平台仅为了方便运维人员进行系统管理，并不能代替运维本身工作，而且也不打算替代运维人员。部分部署脚本需要运维人员自行编写。

# 开发语言及框架
  - HTML5
  - Bootstrap3.3.5 + CSS3
  - Jquery2.1.4
  - Python3.5
  - Django1.9

# 平台功能

## 用户与组中心
  - 用户创建后，可以创建运维管理组，并在组内邀请其他成员加入，邀请时，需授予权限。
  - 权限分为3个等级：管理权可有与创建者相同的权限，运维权可对组内服务器进行运维操作，查看权仅能查看服务器信息及运维记录。
  - 用户仅作为个人登录只用，所有权限来源于组。
  - 组与服务器相关，服务器的创建只能基于组。

## 资产调配中心
  - 管理服务器资产
  - 管理备件资产 
  - 查看资产流向

## 运维操作中心
  - 基于ansible进行管理，本平台已附带常用的运维操作。
  - 备件更换的记录（仅物理设备，非云设备）

## 实时监控中心
  - 利用C/S模式，查看设备当前运行状态
  - 部分功能结合监控数据进行自动运维操作
    
