from django.contrib.auth import login
from django.db import models
from django.contrib.auth.models import Group, User
from datetime import date, time
from django.utils import timezone

class People(User):
    gend=[(0,'男'), (1,'女')]
    phone = models.CharField(max_length = 30, null=True)
    emailcheck =models.CharField(max_length = 10, null=True)
    emailcheckcode=models.CharField(max_length = 30, null=True)
    name=models.CharField(max_length = 30, null=True)
    birthday=models.CharField(max_length = 30, null=True)
    height=models.CharField(max_length = 30, null=True)
    Weight=models.CharField(max_length = 30, null=True)
    gender=models.CharField(max_length = 2,choices=gend,null=True)
    fcm_id=models.CharField(max_length = 30, null=True)
    address=models.CharField(max_length = 30, null=True)
    token=models.CharField(max_length = 30, default="$token")
    fb_id=models.CharField(max_length = 30, null=True,default=0)
    group=models.CharField(max_length = 30,null=True)
    verified=models.CharField(max_length = 30,default=1)
    must_change_password=models.CharField(max_length = 30,default=0)
    badge=models.CharField(max_length = 30,default=87)
    status=models.CharField(max_length = 30,default="Normal")
    unread_records=models.CharField(max_length = 30,default=0)
    login_times=models.CharField(max_length = 30,default=0)
    privacy_policy=models.CharField(max_length = 30,default=1)
    created_at=models.DateTimeField(auto_now=False, auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=False, auto_now_add=True,null=True)

class bloodduck(models.Model):
    user_id=models.CharField(max_length = 30, null=True)
    systolic=models.CharField(max_length = 30, null=True)
    diastolic=models.CharField(max_length = 30, null=True)
    pulse=models.CharField(max_length = 30, null=True)
    recorded_at=models.DateTimeField(auto_now=False, auto_now_add=False,null=True)

class weight(models.Model):
    user_id=models.CharField(max_length = 30, null=True)
    waight=models.CharField(max_length = 30, null=True)
    body_fat=models.CharField(max_length = 30, null=True)
    bmi=models.CharField(max_length = 30, null=True)
    recorded_at=models.DateTimeField(auto_now=False, auto_now_add=False,null=True)

class bloodsugar(models.Model):
    time=[(0,'晨起'), (1,'早餐前'), (2,'早餐後'), (3,'午餐前'), (4,'午餐後'), (5,'晚餐前'), (6,'晚餐後'), (7,'睡前')]
    user_id=models.CharField(max_length = 30, null=True)
    sugar=models.CharField(max_length = 30, null=True)
    time_period=models.CharField(max_length = 2,choices=time,null=True)
    recorded_at=models.DateTimeField(auto_now=False, auto_now_add=False,null=True)

class default(models.Model):
    user_id=models.CharField(max_length = 30, null=True, unique=True)
    sugar_delta_max=models.CharField(max_length = 30, null=True)
    sugar_delta_min=models.CharField(max_length = 30, null=True)
    sugar_morning_max=models.CharField(max_length = 30, null=True)
    sugar_morning_min=models.CharField(max_length = 30, null=True)
    sugar_evening_max=models.CharField(max_length = 30, null=True)
    sugar_evening_min=models.CharField(max_length = 30, null=True)
    sugar_before_max=models.CharField(max_length = 30, null=True)
    sugar_before_min=models.CharField(max_length = 30, null=True)
    sugar_after_max=models.CharField(max_length = 30, null=True)
    sugar_after_min=models.CharField(max_length = 30, null=True)
    systolic_max=models.CharField(max_length = 30, null=True)
    systolic_min=models.CharField(max_length = 30, null=True)
    diastolic_max=models.CharField(max_length = 30, null=True)
    diastolic_min=models.CharField(max_length = 30, null=True)
    pulse_max=models.CharField(max_length = 30, null=True)
    pulse_min=models.CharField(max_length = 30, null=True)
    weight_max=models.CharField(max_length = 30, null=True)
    weight_min=models.CharField(max_length = 30, null=True)
    bmi_max=models.CharField(max_length = 30, null=True)
    bmi_min=models.CharField(max_length = 30, null=True)
    body_fat_max=models.CharField(max_length = 30, null=True)
    body_fat_min=models.CharField(max_length = 30, null=True)

class diet(models.Model):
    time=[(0,'早餐'), (1,'午餐'), (2,'晚餐')]
    user_id=models.CharField(max_length = 30, null=True)
    description=models.TextField(max_length = 30, null=True)
    meal=models.CharField(max_length = 2,choices=time,null=True)
    tag=models.TextField(max_length = 30, null=True)
    image=models.IntegerField(null=True)
    location=models.CharField(max_length = 50, null=True)
    recorded_at=models.DateTimeField(auto_now=False, auto_now_add=False,null=True)

class caremessage(models.Model):
    user_id=models.CharField(max_length = 30, null=True)
    member_id=models.TextField(max_length = 30, null=True)
    reply_id=models.TextField(max_length = 30, null=True)
    message=models.TextField(max_length = 30, null=True)
    created_at=models.DateTimeField(auto_now=False, auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=False, auto_now_add=True,null=True)

class news(models.Model):
    member_id=models.TextField(max_length = 30, null=True)
    group=models.TextField(max_length = 30, null=True)
    message=models.TextField(max_length = 30, null=True,default='456')
    pushed_at=models.TextField(max_length = 30, null=True)
    created_at=models.DateTimeField(auto_now=False, auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=False, auto_now_add=True,null=True)

class medical(models.Model):
    sicktype=[(0,'無'), (1,'糖尿病前期'), (2,'第一型'), (3,'第二型'), (4,'妊娠')]
    user_id=models.CharField(max_length = 30, null=True)
    diabetes_type=models.CharField(max_length = 2,choices=sicktype,null=True)
    oad=models.BooleanField(max_length = 30, null=True)
    insulin=models.BooleanField(max_length = 30, null=True)
    anti_hypertensives=models.BooleanField(max_length = 30, null=True)
    created_at=models.DateTimeField(auto_now=False, auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=False, auto_now_add=True,null=True)

class alc(models.Model):
    user_id=models.CharField(max_length = 30, null=True)
    a1c=models.TextField(max_length = 30, null=True)
    recorded_at=models.DateTimeField(auto_now=False, auto_now_add=False,null=True)
    created_at=models.DateTimeField(auto_now=False, auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=False, auto_now_add=True,null=True)

class setting(models.Model):
    user_id=models.CharField(max_length = 30, null=True, unique=True)
    after_recording=models.BooleanField(max_length = 30, null=True)
    no_recording_for_a_day=models.BooleanField(max_length = 30, null=True)
    over_max_or_under_min=models.BooleanField(max_length = 30, null=True)
    after_meal=models.BooleanField(max_length = 30, null=True)
    unit_of_sugar=models.BooleanField(max_length = 30, null=True)
    unit_of_weight=models.BooleanField(max_length = 30, null=True)
    unit_of_height=models.BooleanField(max_length = 30, null=True)
    created_at=models.DateTimeField(auto_now=False, auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=False, auto_now_add=True,null=True)

class badge(models.Model):
    badge=models.CharField(max_length = 30,default=87)

class drug_useds(models.Model):
    med=[(0,'糖尿病藥物'),(1,'高血壓藥物')]
    user_id=models.CharField(max_length = 30, null=True)
    type=models.CharField(max_length = 2, choices=med,null=True)
    name=models.CharField(max_length = 2,null=True)
    recorded_at=models.DateTimeField(auto_now=False, auto_now_add=False,null=True)

class friendlist(models.Model):
    gend=[(0,'男'), (1,'女')]
    ret=[(0,'醫師團'),(1,'親友團'),(2,'糖友團')]
    name=models.CharField(max_length = 30, null=True)
    account=models.CharField(max_length = 30, null=True)
    email =models.CharField(max_length = 10, null=True)
    phone = models.CharField(max_length = 30, null=True)
    fb_id=models.CharField(max_length = 30, null=True,default=0)
    status=models.CharField(max_length = 30,default="Normal")
    group=models.CharField(max_length = 30,null=True)
    birthday=models.CharField(max_length = 30, null=True)
    height=models.CharField(max_length = 30, null=True)
    gender=models.CharField(max_length = 2,choices=gend,null=True)
    verified=models.CharField(max_length = 30,default=1)
    privacy_policy=models.CharField(max_length = 30,default=1)
    must_change_password=models.CharField(max_length = 30,default=0)
    badge=models.CharField(max_length = 30,default=87)
    relation_type=models.CharField(max_length = 30,choices=ret)
    created_at=models.DateTimeField(auto_now=False, auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=False, auto_now_add=True,null=True)

class requestlist(models.Model):    
    ret=[(0,'醫師團'),(1,'親友團'),(2,'糖友團')]
    statu=[(0,'未確認'), (1,'接受'),(2,'拒絕')]
    user_id=models.CharField(max_length = 30, null=True)
    relation_id=models.CharField(max_length = 30,null=True)
    type=models.CharField(max_length = 30,choices=ret)
    status=models.CharField(max_length = 2,choices=statu,default=0)
    read=models.CharField(max_length = 2,default="false")
    created_at=models.DateTimeField(auto_now=False, auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=False, auto_now_add=True,null=True)
    whoami=models.CharField(max_length = 30,null=True)

class invite_code(models.Model):
    user_id=models.CharField(max_length = 30, null=True)
    user_name=models.CharField(max_length = 30,default=0,primary_key=True)
    code=models.CharField(max_length = 30,default=0)

class record(models.Model):
    user_id=models.CharField(max_length = 30, null=True)
    report_id=models.CharField(max_length = 30, null=True)
    created_at=models.DateTimeField(auto_now=False, auto_now_add=True,null=True)
    type=models.CharField(max_length = 3, null=True)
    relation_type=models.CharField(max_length = 3, null=True)
    
class uid_id_friend(models.Model):
    my_id=models.CharField(max_length = 30, null=True)
    friend_id=models.CharField(max_length = 30, null=True)
    relation_type=models.CharField(max_length = 3, null=True)

