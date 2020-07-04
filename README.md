# Backend

## 登录注册

### 路径

Backend/login

### 完成进度

登录、注册和登出的接口已写好

修改密码和忘记密码的接口已写好

注册邮箱验证和重置（忘记）密码邮箱验证接口已写好

### 调用方法

#### 登录

URL：

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
    "status": "ok",						/*ok和error分别对应登录成功与登录失败*/
    "type": "account",					/*当status为error时，type显示具体错误信息；ok则为account*/
    "currentAuthority": "user/admin"	/*用户权限分为user和admin*/
}
```

#### 注册

URL：

http方法：POST

前端需要提供的json数据参数，格式如下：

```json
{
    "username": "",		/*用户名*/
    "password1": "",	/*密码*/
    "password2": "",	/*重复密码，需要两次密码一致才可成功注册*/
    "email": "",		/*邮箱，一个邮箱只能注册一个账号*/
    "authority": "",	/*用户权限，分为user和admin*/
}
```

当注册成功时，后端返回的json数据格式如下：

```json
{
    "status": "ok",						/*ok和error分别对应注册成功与注册失败*/
    "type": "register",					/*当status为error时，type显示具体错误信息；ok则为register*/
}
```

后端会生成一个验证码，并向该账号注册的邮箱发送一封包含验证链接的邮件。用户点击链接后即可完成验证。

#### 登出

URL：

http方法：POST

前端调用该接口时，需要处于登录状态，并将登录状态下的cookie传给后端。

登出成功时，后端返回的json数据格式如下：

```json
{
    "status": "ok",						/*ok和error分别对应登出成功与登出失败*/
    "type": "logout",					/*当status为error时，type显示具体错误信息；ok则为logout*/
}
```

#### 修改密码

URL：

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
    "status": "ok",						/*ok和error分别对应修改成功与修改失败*/
    "type": "changePassword",			/*当status为error时，type显示具体错误信息；ok则为changePassword*/
}
```

#### 忘记密码

URL：

http方法：POST

当登录时选择忘记密码，后端会随机生成重置密码发送给用户绑定的邮箱。前端需要提供的json数据参数，格式如下：

```json
{
    "username": "",	/*重置密码的账号用户名*/
}
```

后端返回的json数据格式如下：

```json
{
    "status": "ok",						/*ok和error分别对应重置成功与重置失败*/
    "type": "changePassword",			/*当status为error时，type显示具体错误信息；ok则为resetPassword*/
}
```