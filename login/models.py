from django.db import models

    
class User(models.Model):
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    created_time = models.DateTimeField(auto_now_add=True)
    has_confirmed = models.BooleanField(default=False)
    authority = models.CharField(max_length=10, default='user')
    interns = models.ManyToManyField('Interns',blank=True)
    ras = models.ManyToManyField('RAs', blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + ":" + self.code

    class Meta:
        ordering = ['-created_time']
        verbose_name = '确认码'
        verbose_name_plural = '确认码'


class Interns(models.Model):
    index = models.CharField(max_length=64)
    job = models.CharField(max_length=128)
    job_link = models.CharField(max_length=128)
    company_name = models.CharField(max_length=128)
    city = models.CharField(max_length=64)
    duration = models.CharField(max_length=64)
    frequency = models.CharField(max_length=64)
    salary = models.CharField(max_length=64)

    def __str__(self):
        return self.job
    
    class Meta:
        ordering = ['index']
        verbose_name = '实习'
        verbose_name_plural = '实习'


class RAs(models.Model):
    index = models.CharField(max_length=64)
    title = models.CharField(max_length=128)
    location = models.CharField(max_length=128)
    link = models.CharField(max_length=256)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['index']
        verbose_name = '研究助理'
        verbose_name_plural = '研究助理'

class Forum(models.Model):
    forum_name = models.CharField(max_length=128, unique=True)
    time = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=128)

class Favorite(models.Model):
    id_name = models.CharField(max_length=128, unique=True)
    forum_name = models.CharField(max_length=128, unique=True)