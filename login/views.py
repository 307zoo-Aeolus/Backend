from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import hashlib, datetime, pytz, json, csv, time, validators
from . import models


def myJsonResponse(ret):
    json_data = json.dumps(ret, ensure_ascii=False)
    response = HttpResponse(json_data)
    return response


def dictFailLogin(s):
    """
    fail login message dictionary
    """
    return {'status': 'error',
            'type': s,
            'currentAuthority': 'guest'}


def dictFail(s):
    """fail status"""
    return {'status': 'error',
            'type': s}


def hash_code(s, salt='login_hash'):
    """
    encode password
    """
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def makeConfrimString(user):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user,)
    return code


def sendRegisterEmail(email, username, code):
    subject = 'Registration Confirm for {}'.format(username)
    textContent = 'This is a registration confirmation.'
    htmlContent = '''<p>Click <a href="http://{}/user/confirm/?code={}" target="blank">confirm link</a>
                    to accomplish the confirmation.</p>'''.format('localhost:8000', code, 1) # CONFIRM_DAYS
    message = EmailMultiAlternatives(subject, textContent, settings.DEFAULT_FROM_EMAIL, [email])
    message.attach_alternative(htmlContent, 'text/html')
    message.send()


def sendResetEmail(email, username, newpsw):
    subject = 'Reset Password for: {}'.format(username)
    textContent = 'This includes a reset password for user {}'.format(username)
    htmlContent = '''<p>This includes a reset password for user {}.</p>
                    <p>Your temporary password is {}. Please change it after login.</p>'''.format(username, newpsw)
    message = EmailMultiAlternatives(subject, textContent, settings.DEFAULT_FROM_EMAIL, [email])
    message.attach_alternative(htmlContent, 'text/html')
    message.send()


def userConfirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = 'Invalid confirm request!'
        return render(request, 'login/confirm.html', locals())
    
    created_time = confirm.created_time
    now = datetime.datetime.now()
    now = now.replace(tzinfo=pytz.timezone('UTC'))
    old = created_time + datetime.timedelta(1) # CONFIRM_DAYS
    if now>old:
        confirm.user.delete()
        message = 'Your email expired. Please register again.'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = 'Successfully confirmed.'
        return render(request, 'login/confirm.html', locals())


@csrf_exempt
def login(request):
    """
    login function
    """
    if request.session.get('is_login', None):
        return myJsonResponse(dictFailLogin('Already login.'))
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        try:
            user = models.User.objects.get(name=username)
            if user.has_confirmed == False:
                message = 'The account named {} has not accomplished email confirmation'.format(username)
                return myJsonResponse(dictFailLogin(message))
            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                ret = {'status': 'ok',
                       'type': 'account',
                       'currentAuthority': user.authority}
                return myJsonResponse(ret)
            else:
                message = 'Wrong password for user {}'.format(username)
                return myJsonResponse(dictFailLogin(message))
        except:
            message = 'Username not existed.'
            return myJsonResponse(dictFailLogin(message))
    else:
        return myJsonResponse(dictFailLogin('Request method is not POST'))


@csrf_exempt
def register(request):
    """
    register function
    """
    request.session.clear_expired()
    if request.session.get('is_login', None):
        return myJsonResponse(dictFail('Already login.'))
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']
        email = data['email']
        authority = data['authority']
        if username == '':
            message = 'Username cannot be null.'
            return myJsonResponse(dictFail(message))
        same_username = models.User.objects.filter(name=username)
        if same_username:
            message = 'Username \"{}\" has been used.'.format(username)
            return myJsonResponse(dictFail(message))
        if password1 != password2:
            message = 'Two password inputs do not match.'
            return myJsonResponse(dictFail(message))
        elif password1 == '':
            message = 'Password cannot be null.'
            return myJsonResponse(dictFail(message))
        if not validators.email(email):
            message = 'Invalid email address.'
            return myJsonResponse(dictFail(message))
        if authority not in {'user', 'admin'}:
            message = 'Invalid authority.'
            return myJsonResponse(dictFail(message))
        same_email_user = models.User.objects.filter(email=email)
        if same_email_user:
            message = 'Email address \"{}\" has been used.'.format(email)
            return myJsonResponse(dictFail(message))
        else:
            new_user = models.User.objects.create(
                name = username,
                password = hash_code(password1),
                email = email,
                has_confirmed = False,
                authority = authority,
            )
            code = makeConfrimString(new_user)
            sendRegisterEmail(email, username, code)
            return myJsonResponse({'status': 'ok',
                                   'type': 'register'})
    else:
        return myJsonResponse(dictFailLogin('Request method is not POST'))


@csrf_exempt
def logout(request):
    if not request.session.get('is_login', None):
        return myJsonResponse(dictFail('Already logout.'))
    request.session.flush()
    return myJsonResponse({'status': 'ok',
                           'type': 'logout'})


@csrf_exempt
def getCurrentUser(request):
    if not request.session.get('is_login', None):
        return myJsonResponse(dictFail('Already logout.'))
    return myJsonResponse({'status': 'ok',
                            'username': request.session['user_name']})


@csrf_exempt
def changePassword(request):
    if not request.session.get('is_login', None):
        return myJsonResponse(dictFail('Already logout.'))
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        oldpsw, newpsw = data['oldpsw'], data['newpsw']
        if newpsw == '':
            return myJsonResponse(dictFail('Invalid new password'))
        if newpsw == oldpsw:
            return myJsonResponse(dictFail('New password cannot be the same with old password.'))
        try:
            user = models.User.objects.get(name=username)
        except:
            return myJsonResponse(dictFail('Username {} not existed.'.format(username)))
        if user.password == hash_code(oldpsw):
            user.password = hash_code(newpsw)
            user.save()
            request.session.flush()
            return myJsonResponse({'status': 'ok',
                                    'type': 'changePassword'})
        else:
            return myJsonResponse(dictFail('Wrong password.'))
    else:
        return myJsonResponse(dictFail('Request method is not POST.'))


@csrf_exempt
def resetPassword(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        try:
            user = models.User.objects.get(name=username)
        except:
            return myJsonResponse(dictFail('Username {} not existed.'.format(username)))
        if user.has_confirmed == False:
            return myJsonResponse(dictFail('This account {} has not accomplished email confirmation.'.format(username)))
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%M')
        newpsw = hash_code(username, now)[:16]
        sendResetEmail(user.email, username, newpsw)
        user.password = hash_code(newpsw)
        user.save()
        return myJsonResponse({'status': 'ok',
                               'type': 'resetPassword'})
    else:
        return myJsonResponse(dictFail('Request method is not POST.'))


def postContentInterns(user, content):
    internsSet = set([x for x in user.interns.all()])
    internsPostSet = set()
    for index in content:
        try:
            interns = models.Interns.get(index=index)
        except:
            return False
        internsPostSet.add(region)
    for i in internsPostSet-internsSet: user.interns.add(i)
    for i in internsSet-internsPostSet: user.interns.remove(i)
    return True


@csrf_exempt
def getInterns(request):
    if not request.session.get('is_login', None):
        return myJsonResponse(dictFail('Already logouted'))
    username = request.session['username']
    try:
        user = models.User.objects.get(name=username)
    except:
        return myJsonResponse(dictFail('User {} not existed.'.format(username)))
    internsList = [{'index': x.index, 'job': x.job, 'job_link': x.job_link, 
                    'company_name': x.company_name, 'city': x.city, 'duration': x.duration, 
                    'frequency': x.frequency, 'salary': x.salary} for x in user.interns.all()]
    return myJsonResponse({'status': 'ok',
                           'type': 'interns',
                           'content': internsList})


@csrf_exempt
def postInterns(request):
    if not request.session.get('is_login', None):
        return myJsonResponse(dictFail('Already logout.'))
    if request.method == 'POST':
        data = json.loads(request.body)
        username = request.session['user_name']
        content = data['content']
        try:
            user = models.User.get(name=username)
        except:
            return myJsonResponse(dictFail('User {} not existed.'.format(username)))
        postContentInterns(user, content)
        internsList = [{'index': x.index, 'job': x.job, 'job_link': x.job_link, 
                        'company_name': x.company_name, 'city': x.city, 'duration': x.duration, 
                        'frequency': x.frequency, 'salary': x.salary} for x in user.interns.all()]
        return myJsonResponse({'status': 'ok',
                               'type': 'interns',
                               'content': internsList})
    else:
        return myJsonResponse(dictFail('Request method is not POST.'))


def postContentRAs(user, content):
    RAsSet = set([x for x in user.ras.all()])
    RAsPostSet = set()
    for index in content:
        try:
            ras = models.RAs.get(index=index)
        except:
            return False
        RAsPostSet.add(region)
    for i in RAsPostSet-RAsSet: user.ras.add(i)
    for i in RAsSet-RAsPostSet: user.ras.remove(i)
    return True


@csrf_exempt
def getRAs(request):
    if not request.session.get('is_login', None):
        return myJsonResponse(dictFail('Already logouted'))
    username = request.session['user_name']
    try:
        user = models.User.objects.get(name=username)
    except:
        return myJsonResponse(dictFail('User {} not existed.'.format(username)))
    RAsList = [{'index': x.index, 'title': x.title, 'location': x.location,
                'link': x.link} for x in user.ras.all()]
    return myJsonResponse({'status': 'ok',
                           'type': 'ras',
                           'content': RAsList})


@csrf_exempt
def postRAs(request):
    if not request.session.get('is_login', None):
        return myJsonResponse(dictFail('Already logout.'))
    if request.method == 'POST':
        data = json.loads(request.body)
        username = request.session['user_name']
        content = data['content']
        try:
            user = models.User.get(name=username)
        except:
            return myJsonResponse(dictFail('User {} not existed.'.format(username)))
        postContentRAs(user, content)
        RAsList = [{'index': x.index, 'title': x.title, 'location': x.location,
                    'link': x.link} for x in user.ras.all()]
        return myJsonResponse({'status': 'ok',
                               'type': 'ras',
                               'content': RAsList})
    else:
        return myJsonResponse(dictFail('Request method is not POST.'))

def getForum(request):
    if not request.session.get('is_login', None):
        return myJsonResponse(dictFail('Already logout.'))
    frmname = request.session['frmname']
    if request.method == 'GET':
        try:
            forum = models.Forum.objects.get(forum_name=frmname)
        except:
            return myJsonResponse(dictFail('Forum {} not existed.'.format(frmname)))
        rst = models.Forum.get(forum_name = frmname)
        forumInfo = {'forum_name':rst.forum_name,'time':rst.time,'link':rst.link}
        
        return myJsonResponse({'status': 'ok',
                            'type': 'forums',
                            'content': forumInfo})
    
def getFavourite(request):
    if not request.session.get('is_login', None):
        return myJsonResponse(dictFail('Already logout.'))
    username = request.session['username']
    if request.method == 'GET':
        try:
            favourites = models.Favourite.objects.get(username=username)
        except:
            return myJsonResponse(dictFail('User {} doesn\'t have a favourite.'.format(username)))
        favouritelist = [ {'forum_name':x.forum.forum_name,'time':x.forum.time,'link':x.forum.link} for x in favourites]
        return myJsonResponse({'status': 'ok',
                            'type': 'favourites',
                            'content': favouritelist})

def addFavourite(request):
    if not request.session.get('is_login', None):
        return myJsonResponse(dictFail('Already logout.'))
    if request.method == 'POST':
        data = json.loads(request.body)
        username = request.session['username']
        forum = data['forum_name']
        foruminfo = models.Forum.get(forum_name=forum)
        models.Favorite.objects.create(
            username = username,
            forum = foruminfo
        )
        
        

def deleteFavourite(request):
    if not request.session.get('is_login', None):
        return myJsonResponse(dictFail('Already logout.'))
    if request.method == 'POST':
        data = json.loads(request.body)
        username = request.session['username']
        forum = data['forum_name']
        foruminfo = models.Forum.get(forum_name=forum)
        models.Favorite.objects.get(username=username,forum=foruminfo).delete()

