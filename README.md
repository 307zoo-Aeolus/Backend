# Backend

## 使用说明
* 安装 mysql 并启动，建一个新的 database：
```
create database ${your database name}
```
* 将 mysql 的用户名、密码、database名记录下来，并替换 aelous/settings.py 中的 Databases 配置
* 建立 virtualenv 并启动服务：
```
pip3 install virtualenv
cd Backend
virtualenv --no-site-packages venv
source venv/bin/activate
pip install django
pip install django-cors-headers
pip install djangorestframework
pip install validators
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 8000
```
* 可能的 bugs 和解决方案：
https://blog.csdn.net/lijing742180/article/details/91966031

## 登录注册

### 路径

Backend/login

### 完成进度

登录、注册和登出的接口已写好

修改密码和忘记密码的接口已写好

注册邮箱验证和重置（忘记）密码邮箱验证接口已写好

### 调用方法

#### 登录

URL：http://127.0.0.1:8000/user/login/

http方法：POST

前端需要提供的json数据参数，格式如下：

```json
{
    "username": "",		/*用户名*/
    "password": "",		/*密码*/
}
```

当登录成功时，后端返回的json数据格式如下：

```json
{
    "status": "ok",	/*ok和error分别对应登录成功与登录失败*/
    "type": "account",	/*当status为error时，type显示具体错误信息；ok则为account*/
    "currentAuthority": "user/admin"	/*用户权限分为user和admin*/
}
```

#### 注册

URL：http://127.0.0.1:8000/user/register/

http方法：POST

前端需要提供的json数据参数，格式如下：

```json
{
    "username": "",	/*用户名*/
    "password1": "",	/*密码*/
    "password2": "",	/*重复密码，需要两次密码一致才可成功注册*/
    "email": "",	/*邮箱，一个邮箱只能注册一个账号*/
    "authority": "",	/*用户权限，分为user和admin*/
}
```

当注册成功时，后端返回的json数据格式如下：

```json
{
    "status": "ok",		/*ok和error分别对应注册成功与注册失败*/
    "type": "register",		/*当status为error时，type显示具体错误信息；ok则为register*/
}
```

后端会生成一个验证码，并向该账号注册的邮箱发送一封包含验证链接的邮件。用户点击链接后即可完成验证。

#### 登出

URL：http://127.0.0.1:8000/user/logout/

http方法：POST

前端调用该接口时，需要处于登录状态，并将登录状态下的cookie传给后端。

登出成功时，后端返回的json数据格式如下：

```json
{
    "status": "ok",		/*ok和error分别对应登出成功与登出失败*/
    "type": "logout",		/*当status为error时，type显示具体错误信息；ok则为logout*/
}
```

#### 修改密码

URL：http://127.0.0.1:8000/user/change/

http方法：POST

前端在调用该接口时，用户应当处于登录状态，并将登录状态下的cookies传给后端。前端需要提供的json数据参数，格式如下：

```json
{
    "oldpsw": "",	/*现有密码，用来验证*/
    "newpsw": "",	/*修改后的密码*/
}
```

**注：新旧密码不能相同，新密码不能为空。**

当修改成功时，后端返回的json数据格式如下：

```json
{
    "status": "ok",		/*ok和error分别对应修改成功与修改失败*/
    "type": "changePassword",		/*当status为error时，type显示具体错误信息；ok则为changePassword*/
}
```

#### 忘记密码

URL：http://127.0.0.1:8000/reset/

http方法：POST

当登录时选择忘记密码，后端会随机生成重置密码发送给用户绑定的邮箱。前端需要提供的json数据参数，格式如下：

```json
{
    "username": "",	/*重置密码的账号用户名*/
}
```

当重置成功时，后端返回的json数据格式如下：

```json
{
    "status": "ok",		/*ok和error分别对应重置成功与重置失败*/
    "type": "changePassword",		/*当status为error时，type显示具体错误信息；ok则为resetPassword*/
}
```

## 信息订阅

### 路径

Aeolus/login

### 完成进度

实习添加收藏、查看收藏、删除收藏的接口已写好

研究助理添加收藏、查看收藏、删除收藏的接口已写好

### 调用方法

#### 查看实习收藏

URL：http://127.0.0.1:8000/user/interns/get/

http方法：GET

前端调用该接口时，用户应当处于登录状态，并将用户登录时的cookie传给后端。

当查看成功时，后端返回的json参数为：

```json
{
    "status": "ok",		/*ok和error分别对应查看成功与查看失败*/
    "type": "interns",		/*当status为error时，type字段显示错误信息；否则为interns*/
    "content": [{"index": "", "job": "", "job_link": "", "company_name": "", "city": "", "duration": "", "frequency": "", "salary": "",}]	/*当status为error时无content字段；否则返回收藏实习列表*/
}
```

#### 修改实习收藏

URL：http://127.0.0.1:8000/user/interns/post/

http方法：POST

前端需要提供的json参数格式为：

```json
{
    "content": ["",]	/*该用户新的收藏研究助理index号码列表*/
}
```

前端在调用该接口时，用户应处于登录状态，并将用户登录时的cookie传给后端。

当修改成功时，后端返回的json参数为：

```json
{
    "status": "ok",		/*ok和error分别对应修改成功与修改失败*/
    "type": "interns",	/*当status为error时，type字段显示错误信息；否则为interns*/
    "content": [{"index": "", "job": "", "job_link": "", "company_name": "", "city": "", "duration": "", "frequency": "", "salary": "",}]	/*当status为error时无content字段；否则返回收藏实习列表*/
}
```

#### 查看研究助理收藏

URL：http://127.0.0.1:8000/user/ras/get/

http方法：GET

前端调用该接口时，用户应当处于登录状态，并将用户登录时的cookie传给后端。

当查看成功时，后端返回的json参数为：

```json
{
    "status": "ok",		/*ok和error分别对应查看成功与查看失败*/
    "type": "ras",	/*当status为error时，type字段显示错误信息；否则为ras*/
    "content": [{"index": "", "title": "", "location": "", "link": "",}]	/*当status为error时无content字段；否则返回收藏研究助理列表*/
}
```

#### 修改研究助理收藏

URL：http://127.0.0.1:8000/user/ras/post/

http方法：POST

前端需要提供的json参数格式为：

```json
{
    "content": ["",]	/*该用户新的收藏实习index号码列表*/
}
```

前端在调用该接口时，用户应处于登录状态，并将用户登录时的cookie传给后端。

当修改成功时，后端返回的json参数为：

```json
{
    "status": "ok",		/*ok和error分别对应修改成功与修改失败*/
    "type": "ras",	/*当status为error时，type字段显示错误信息；否则为ras*/
    "content": [{"index": "", "title": "", "location": "", "link": "",}]	/*当status为error时无content字段；否则返回收藏研究助理列表*/
}
```

