from collections import UserDict
from typing import Counter
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import User
from django.shortcuts import render
# Create your views here.
from django.http.response import JsonResponse
from register.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse, QueryDict
from django.contrib import auth
from django.contrib.sessions.models import Session
from register.forms import *
from .forms import RegisterForm
from django.core import serializers
from django.core.mail import EmailMessage, message
import random
import json

def same_key(body_data):#抓patch和重複欄位用
    b=[]
    c=[]
    d={}
    data = body_data.decode('utf-8')
    data2 = data.split('\r\n\r\n')
    for i in data2:
        a=i.split('\r\n')
        for i in a:
            b=i.split('=')
            c=c+b
            for i in range(len(c)):
                if i%4 == 3:
                    if c[i-1].replace('"','') in d and  c[i] not in d[c[i-1].replace('"','')]:
                        a=d[c[i-1].replace('"','')]
                        d[c[i-1].replace('"','')]=a,c[i]
                        
                    else:
                        d.update({c[i-1].replace('"',''):c[i]})
                        
    return d   

def real_pass(request,password):#抓密碼用
    a=request.COOKIES['sessionid']
    s=Session.objects.filter(session_key=a)[0]
    b=s.get_decoded()
    if password == b['real_password']: 
        secret_password = b['secret_password']
    return secret_password

def GetRequestBody(body_data):#patch專用函數
#body_data = request.body
    b=[]
    c=[]
    d={}
    data = body_data.decode('utf-8')
    data2 = data.split('\r\n\r\n')
    for i in data2:
        a=i.split('\r\n')
        for i in a:
            b=i.split('=')
            c=c+b
            for i in range(len(c)):
                if i%4 == 3:
                    d.update({c[i-1].replace('"',''):c[i]})
    return d   

def the24api_dic(id,uid,sharedata,typename):#24api的字典   #放入分享的id和uid,內容,分類
        #需求 報告內容＋報告者資料＋分享時間＋type 
        request_dic={'bloodduck':'0','weight':'1','bloodsugar':'2','diet':'3'}#type字典
        usern=list(invite_code.objects.filter(user_id=uid).values('user_name'))[0]["user_name"]#報告者名字抓資料
        requester=list(People.objects.filter(username=usern).values())[0]#報告者資料頭
        crtime=list(record.objects.filter(relation_type='0',type=typename,report_id=id).values('created_at'))#分享時間
        userDic={ #報告者資料字典
            "id":uid,"name":usern,"account":requester["username"],"email":requester["email"],
            "phone":requester["phone"],"fb_id":requester["fb_id"],"status":requester["status"],"group":requester["group"],
            "birthday":requester["birthday"],"height":requester["height"],"gender":requester["gender"],"verified":requester["verified"]
            ,"privacy_policy":requester["privacy_policy"],"must_change_password":requester["must_change_password"],
            "badge":requester["badge"],"created_at":requester["created_at"],"updated_at":requester["updated_at"]
            }
        type_dic={"type":request_dic[typename]}
        sharedata.setdefault("user",userDic)#加上報告者資料
        sharedata.update(crtime)#加上時間和類別
        sharedata.update(type_dic)#加上時間和類別
        return sharedata

def api24(request,kind):
    if request.method == 'GET':#retype是醫師的
        bd_list=[]
        wei_list=[]
        bs_list=[]
        diet_list=[]
        request_dic={'bloodduck':'0','weight':'1','bloodsugar':'2','diet':'3'}
        req_list=request_dic.keys()
        for i in req_list:#i=是哪個項目
            if i == 'bloodduck' and record.objects.filter(relation_type=kind,type=request_dic[i]).exists():
                id=list(record.objects.filter(relation_type=kind,type=request_dic[i]).values('report_id'))[0]['report_id']
                for t in range(50):#t是檢測id
                    if str(t) in id:#id是所有報告的id串列
                        if bloodduck.objects.filter(id=id).values().exists():
                            uid=list(bloodduck.objects.filter(id=id).values('user_id'))[0]["user_id"]#報告者uid抓名字
                            sharedata=list(bloodduck.objects.filter(id=id).values())[0]#報告者內容
                            bd_list.append(the24api_dic(t,uid,sharedata,i))#丟進去裡面將字典連接起來
            elif i == 'weight' and record.objects.filter(relation_type=kind,type=request_dic[i]).exists():
                id=list(record.objects.filter(relation_type=kind,type=request_dic[i]).values('report_id'))[0]['report_id']#1 2 3
                for t in range(50):#t是檢測id
                    if str(t) in id:#id是所有報告的id串列
                        if weight.objects.filter(id=id).values().exists():
                            uid=list(weight.objects.filter(id=id).values('user_id'))[0]["user_id"]#報告者uid抓名字
                            sharedata=list(weight.objects.filter(id=id).values())[0]#報告者內容
                            wei_list.append(the24api_dic(t,uid,sharedata,i))#丟進去裡面將字典連接起來
            elif i == 'bloodsugar'and record.objects.filter(relation_type=kind,type=request_dic[i]).exists():
                id=list(record.objects.filter(relation_type=kind,type=request_dic[i]).values('report_id'))[0]['report_id']#1 2 3
                for t in range(50):#t是檢測id
                    if str(t) in id:#id是所有報告的id串列
                        if bloodsugar.objects.filter(id=id).values().exists():
                            uid=list(bloodsugar.objects.filter(id=id).values('user_id'))[0]["user_id"]#報告者uid抓名字
                            sharedata=list(bloodsugar.objects.filter(id=id).values())[0]#報告者內容
                            bs_list.append(the24api_dic(t,uid,sharedata,i))#丟進去裡面將字典連接起來
            elif i == 'diet'and record.objects.filter(relation_type=kind,type=request_dic[i]).exists():
                id=list(record.objects.filter(relation_type=kind,type=request_dic[i]).values('report_id'))[0]['report_id']#1 2 3
                for t in range(50):#t是檢測id
                    if str(t) in id:#id是所有報告的id串列
                        if diet.objects.filter(id=id).values().exists():
                            uid=list(diet.objects.filter(id=id).values('user_id'))[0]["user_id"]#報告者uid抓名字
                            sharedata=list(diet.objects.filter(id=id).values())[0]#報告者內容
                            diet_list.append(the24api_dic(t,uid,sharedata,i))#丟進去裡面將字典連接起來
        status="0"
        all_list=bd_list+wei_list+bs_list+diet_list
        return all_list
    else:
        status = "1"
        return status




#第一個ＡＰＩ 註冊 post
@csrf_exempt
def Register(request):  
    status = "11"
    if request.method == 'POST':
        print(111)
        f = RegisterForm(request.POST)
        if f.is_valid():
            username=f.cleaned_data['account']
            phone=f.cleaned_data['phone']
            email=f.cleaned_data['email']
            password= f.cleaned_data['password']
            print(password)
            People.objects.create_user(username=username,phone=phone,email=email,password=password)
            c=People.objects.filter(username=username).values('password').get()
            # 確定uid是註冊時獲取的資料就創預設資料
            # uid=request.user.id
            # default.objects.create(user_id=uid)
            # medical.objects.create(user_id=uid)
            # setting.objects.create(user_id=uid)
            secret=c['password']
            request.session['secret_password']=secret
            request.session['real_password']=password
            status = "0"
            return JsonResponse({"status":status})
    else:
        print(123123)
        status = "1"
    return JsonResponse({"status":status})
#第二個ＡＰＩ 登入 post
@csrf_exempt
def Login(request):
    if request.user.is_authenticated:
        status = "1"
        return JsonResponse({"status":status})    
    elif request.method == 'POST':
        username = request.POST['account']
        password = request.POST['password']
        fb_id=request.POST['fb_id']
        print(username, password)
        user = auth.authenticate(username=username,password=password)
        if People.objects.filter(username=username,emailcheck=0).exists() is not True :
            status='2'
            return JsonResponse({"status":status})
        elif fb_id is not "0":
            status="3"
            return JsonResponse({"status":status})
        else:
            if user:
                auth.login(request,user)
                s=Session.objects.all()[0]
                request.session['username']=username
                token = s.session_data
                status="0"
                return JsonResponse({"status":status})
            else:
                status = "1"
        return JsonResponse({"status":status})
    else:
        status = "1"
        return JsonResponse({"status":status})


#第三個ＡＰＩ 發送驗證碼 post
#更改setting EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
@csrf_exempt
def Send(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        emailaddress = request.POST['email']
        if People.objects.filter(phone=phone,email=emailaddress).exists():
            randomcheck=random.randint(100,999)
            email = EmailMessage(body=str(randomcheck),  # 電子郵件內容
                to=[emailaddress]  # 收件者
            )
            email.fail_silently = False
            email.send()
            People.objects.filter(phone=phone).update(emailcheckcode=randomcheck)
            status = "0"
            return JsonResponse({"status":status})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt#第四個ＡＰＩ 確認驗證碼
def Check(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        code = request.POST['code']
        status = "1"
        if People.objects.filter(phone=phone).exists():
            truecode=People.objects.get(phone=phone).emailcheckcode
            if code == truecode:
                People.objects.filter(emailcheckcode=code).update(emailcheck=0)
                status="0"
                return JsonResponse({"status":status})
        return JsonResponse({"status":status})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt #第五個ＡＰＩ 忘記密碼
def Forget(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        emailaddress = request.POST['email']
        status = "1"
        if People.objects.filter(phone=phone,email=emailaddress).exists():
            password=People.objects.get(phone=phone).password
            email = EmailMessage(body=password,  # 電子郵件內容
                to=[emailaddress]  # 收件者
            )
            email.fail_silently = False
            email.send()
            status = "0"
            print(request.user.id)
            # uid=request.user.id
            # default.objects.create(user_id=uid)
            # setting.objects.create(user_id=uid)
            return JsonResponse({"status":status})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt #第六個ＡＰＩ 重設密碼
def Reset(request):
    if request.method == 'POST':
        password = request.POST['password']
        token = request.POST['token']
        status = "1"
        if People.objects.filter(token=token).exists():
            People.objects.filter(token=token).update(password=password)
            status = "0"
            return JsonResponse({"status":status})
        else:
            return JsonResponse({"status":status})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt #第七個和第十二個ＡＰＩ 個人資訊設定和獲取
def Userinfo(request):
    if request.method == 'GET':  #第12
        uid=request.user.id
        userdata = People.objects.values()
        user_dic=list(userdata)[0]
        user_defa=default.objects.filter(user_id=uid).values()
        user_defa_dic=list(user_defa)[0]
        user_setting=setting.objects.filter(user_id=uid).values()
        user_setting_dic=list(user_setting)[0]
        all_dic={
            'id':uid,'name':user_dic['name'],'account':user_dic['username'],'email':user_dic['email'],
            'phone':user_dic['phone'],'fb_id':user_dic['fb_id'],'status':user_dic['status'],
            'group':user_dic['group'],'birthday':user_dic['birthday'],'height':user_dic['height'],
            'weight':user_dic['Weight'],'gender':user_dic['gender'],'address':user_dic['address'],
            'unread_records':user_dic['unread_records'],'verified':user_dic['verified'],
            'privacy_policy':user_dic['privacy_policy'],'must_change_password':user_dic['must_change_password'],
            'fcm_id':user_dic['fcm_id'],'badge':user_dic['badge'],'login_times':user_dic['login_times'],
            'created_at':user_dic['created_at'],'updated_at':user_dic['updated_at'],'default':user_defa_dic,'setting':user_setting_dic
        }
        if user_dic is None:
            status="1"
            return JsonResponse({"status":status})
        else:
            status="0"
            return JsonResponse({"status":status,'user':all_dic})
    elif request.method == 'PATCH':#第7
        d=GetRequestBody(request.body)
        print(d)
        dkey=list(d)
        if 'token' in dkey:
            People.objects.update(token=d['token'])
        if 'name' in dkey:
            People.objects.update(name=d['name'])
        if 'birthday' in dkey:
            People.objects.update(birthday=d['birthday'])
        if 'height' in dkey:
            People.objects.update(height=d['height'])
        if 'gender' in dkey:
            People.objects.update(gender=d['gender'])
        if 'fcm_id' in dkey:
            People.objects.update(fcm_id=d['fcm_id'])
        if 'address' in dkey:
            People.objects.update(address=d['address'])
        if 'weight' in dkey:
            People.objects.update(weight=d['weight'])
        if 'phone' in dkey:
            People.objects.update(phone=d['phone'])
        if 'email' in dkey:
            People.objects.update(email=d['email'])
        status="0"
        return JsonResponse({"status":status})
    else:
        status="1"
        return JsonResponse({"status":status})
    
@csrf_exempt #第八個ＡＰＩ 上傳血壓測量結果
def Bloodpressure(request):
    if request.method == 'POST':
        uid=request.user.id
        systolic = request.POST['systolic']
        diastolic = request.POST['diastolic']
        pulse = request.POST['pulse']
        recorded_at = request.POST['recorded_at']
        status = "11"
        bloodduck.objects.create(user_id=uid,systolic=systolic,diastolic=diastolic,pulse=pulse,recorded_at=recorded_at)
        if bloodduck.objects.filter(systolic=systolic).exists():
            status = "0"
            return JsonResponse({"status":status})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt #第九個ＡＰＩ 上傳體重測量結果
def Weight(request):
    if request.method == 'POST':
        uid=request.user.id
        Waight = request.POST['weight']
        body_fat = request.POST['body_fat']
        bmi = request.POST['bmi']
        recorded_at = request.POST['recorded_at']
        status = "1"
        weight.objects.create(user_id=uid,waight=Waight,body_fat=body_fat,bmi=bmi,recorded_at=recorded_at)
        if weight.objects.exists():
            status = "0"
            return JsonResponse({"status":status})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt #第十個ＡＰＩ 上傳血糖測量結果
def Bloodsugar(request):
    if request.method == 'POST':
        uid=request.user.id
        sugar = request.POST['sugar']
        time_period = request.POST['time_period']
        recorded_at = request.POST['recorded_at']
        status = "1"
        bloodsugar.objects.create(user_id=uid,sugar=sugar,time_period=time_period,recorded_at=recorded_at)
        if bloodsugar.objects.exists():
            status = "0"
            return JsonResponse({"status":status})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt #第十一個ＡＰＩ 修改個人預設值
def Defult(request):
    if request.method == 'PATCH':
        d=GetRequestBody(request.body)
        uid=request.user.id
        dkey=list(d)
        if 'sugar_delta_max' in dkey:default.objects.filter(user_id=uid).update(sugar_delta_max=d['sugar_delta_max'])
        if 'sugar_delta_min' in dkey:default.objects.filter(user_id=uid).update(sugar_delta_min=d['sugar_delta_min'])
        if 'sugar_morning_max' in dkey:default.objects.filter(user_id=uid).update(sugar_morning_max=d['sugar_morning_max'])
        if 'sugar_morning_min' in dkey:default.objects.filter(user_id=uid).update(sugar_morning_min=d['sugar_morning_min'])
        if 'sugar_evening_max' in dkey:default.objects.filter(user_id=uid).update(sugar_evening_max=d['sugar_evening_max'])
        if 'sugar_evening_min' in dkey:default.objects.filter(user_id=uid).update(sugar_evening_min=d['sugar_evening_min'])
        if 'sugar_before_max' in dkey:default.objects.filter(user_id=uid).update(sugar_before_max=d['sugar_before_max'])
        if 'sugar_before_min' in dkey:default.objects.filter(user_id=uid).update(sugar_before_min=d['sugar_before_min'])
        if 'sugar_after_max' in dkey:default.objects.filter(user_id=uid).update(sugar_after_max=d['sugar_after_max'])
        if 'sugar_after_min' in dkey:default.objects.filter(user_id=uid).update(sugar_after_min=d['sugar_after_min'])
        if 'systolic_max' in dkey:default.objects.filter(user_id=uid).update(systolic_max=d['systolic_max'])
        if 'systolic_min' in dkey:default.objects.filter(user_id=uid).update(systolic_min=d['systolic_min'])
        if 'diastolic_max' in dkey:default.objects.filter(user_id=uid).update(diastolic_max=d['diastolic_max'])
        if 'diastolic_min' in dkey:default.objects.filter(user_id=uid).update(diastolic_min=d['diastolic_min'])
        if 'pulse_max' in dkey:default.objects.filter(user_id=uid).update(pulse_max=d['pulse_max'])
        if 'pulse_min' in dkey:default.objects.filter(user_id=uid).update(pulse_min=d['pulse_min'])
        if 'weight_max' in dkey:default.objects.filter(user_id=uid).update(weight_max=d['weight_max'])
        if 'weight_min' in dkey:default.objects.filter(user_id=uid).update(weight_min=d['weight_min'])
        if 'bmi_max' in dkey:default.objects.filter(user_id=uid).update(bmi_max=d['bmi_max'])
        if 'bmi_min' in dkey:default.objects.filter(user_id=uid).update(bmi_min=d['bmi_min'])
        if 'body_fat_max' in dkey:default.objects.filter(user_id=uid).update(body_fat_max=d['body_fat_max'])
        if 'body_fat_min' in dkey:default.objects.filter(user_id=uid).update(body_fat_min=d['body_fat_min'])
        status = "0"
        return JsonResponse({"status":status})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt#第十三個ＡＰＩ FB_LOGIN
def Privacy_policy(request):
    if request.method == 'POST':
        fb_id = request.POST['fb_id']
        People.objects.update(fb_id=fb_id)
        status="0"
        return JsonResponse({"status":status})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt#第十四個ＡＰＩ 獲取日記
def Diary(request):
    if request.method == 'GET':
        getdia = diet.objects.values()
        lga=list(getdia)
        status="0"
        return JsonResponse({"status":status,"diary":lga})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt#第十五個ＡＰＩ 上傳日記資料 有問題 但是我忘了
def Diet(request):
    if request.method == 'POST':
        uid=request.user.id
        d=same_key(request.body)
        tag=list(d['tag'])
        description = request.POST['description']
        meal = request.POST['meal']
        image = request.POST['image']
        lat = request.POST['lat']
        lng = request.POST['lng']
        location={"lat":lat.replace('"',''),"lng":lng.replace('"','')}
        recorded_at = request.POST['recorded_at']
        diet.objects.create(user_id=uid,description=description,meal=meal,tag=tag,image=image,location=location,
        recorded_at=recorded_at
        )
        status="0"
        return JsonResponse({"status":status})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt#第十六個ＡＰＩ 獲取控糖團邀請碼 有問題 有關預設驗證碼和uid
def Friendcode(request):
    print('11')
    if request.method == 'GET':
        uid=request.user.id
        status="0"
        # a=People.objects.values('username')
        # b=list(a)[0]['username']
        b='abcd12345'
        code='abcdefg'
        invite_code.objects.create(user_id=uid,user_name=b,code=code)
        return JsonResponse({"status":status,'invite_code':code})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt#第十七個ＡＰＩ 獲取控糖團成員 目前還沒有問題
def Friendlist(request):
    if request.method == 'GET':
        uid=request.user.id
        friend_list_data=[]
        friendlist_id=list(uid_id_friend.objects.filter(my_id=uid).values('friend_id'))
        for i in range(len(friendlist_id)):
            friendlist_id[i]=friendlist_id[i]['friend_id']
            fl_dic=list(friendlist.objects.filter(id=friendlist_id[i]).values())[0]
            friend_list_data.append(fl_dic)
        status="0"
        return JsonResponse({"status":status,"friends":friend_list_data})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt#第十八個ＡＰＩ 獲取控糖團邀請
def Friendrequest(request):
    if request.method == 'GET':
        uid=request.user.id
        if requestlist.objects.filter(whoami=uid).exist():
            re=requestlist.objects.filter(whoami=uid).values()
            re_dic=list(re)[0]
            requester=list(People.objects.filter(username=re_dic["user_id"]).values())[0]
            all_dic={
                "id":re_dic["id"],"user_id":re_dic["user_id"],"type":re_dic["type"],"status":re_dic["status"],
            "created_at":re_dic["created_at"],"updated_at":re_dic["updated_at"],
            "user":
                {
                "id":re_dic["user_id"],"name":requester["name"],"account":requester["username"],"email":requester["email"],
                "phone":requester["phone"],"fb_id":requester["fb_id"],"status":requester["status"],"group":requester["group"],
                "birthday":requester["birthday"],"height":requester["height"],"gender":requester["gender"],"verified":requester["verified"]
                ,"privacy_policy":requester["privacy_policy"],"must_change_password":requester["must_change_password"],
                "badge":requester["badge"],"created_at":requester["created_at"],"updated_at":requester["updated_at"]
                }
            }
            status="0"
            return JsonResponse({"status":status,"request":all_dic},)
        else:
            status = "1"
            return JsonResponse({"status":status})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt#第十九個ＡＰＩ 送出控糖團邀請
def Friendsend(request):
    if request.method == 'POST':
        type = request.POST['type']
        invite_codes = request.POST['invite_code']
        if invite_code.objects.filter(code=invite_codes).exists() is not True:
            status="1"
            return JsonResponse({"status":status})
        invite_name=invite_code.objects.filter(code=invite_codes).values('user_name')
        realname=list(invite_name)[0]['user_name']
        if friendlist.objects.filter(account=realname).exists():
            status="2"
            return JsonResponse({"status":status})
        else:
            uid=request.user.id
            whobesend=invite_code.objects.filter(code=invite_codes).values('user_id')
            requestlist.objects.create(whoami=whobesend,user_id=uid,type=type)#who am i 是對18ａｐｉ而言
            status="0"
            return JsonResponse({"status":status})
    else:
        status = "11"
        return JsonResponse({"status":status})

@csrf_exempt#第二十個ＡＰＩ 接受邀請
def Friendaccpet(request,inv_id):
    if request.method == 'GET':
        uid=request.user.id
        if requestlist.objects.filter(user_id=inv_id,whoami=uid).exists():
            b=list(invite_code.objects.filter(user_id=inv_id).values('user_name'))[0]['user_name']
            print(b)
            relation_type=list(requestlist.objects.filter(user_id=inv_id,whoami=uid).values('type'))[0]['type']
            name=list(People.objects.filter(username=b).values('name'))[0]['name']
            email =list(People.objects.filter(username=b).values('email'))[0]['email']
            phone=list(People.objects.filter(username=b).values('phone'))[0]['phone']
            fb_id=list(People.objects.filter(username=b).values('fb_id'))[0]['fb_id']
            statu=list(People.objects.filter(username=b).values('status'))[0]['status']
            group=list(People.objects.filter(username=b).values('group'))[0]['group']
            birthday=list(People.objects.filter(username=b).values('birthday'))[0]['birthday']
            height=list(People.objects.filter(username=b).values('height'))[0]['height']
            gender=list(People.objects.filter(username=b).values('gender'))[0]['gender']
            verified=list(People.objects.filter(username=b).values('verified'))[0]['verified']
            privacy_policy=list(People.objects.filter(username=b).values('privacy_policy'))[0]['privacy_policy']
            must_change_password=list(People.objects.filter(username=b).values('must_change_password'))[0]['must_change_password']
            badge=list(People.objects.filter(username=b).values('badge'))[0]['badge']
            #僅有account 和 relationtype是源自非people
            friendlist.objects.create(name=name,account=b,email=email,phone=phone,fb_id=fb_id,status=statu,
            group=group,birthday=birthday,height=height,gender=gender,verified=verified,privacy_policy=privacy_policy,
            must_change_password=must_change_password,badge=badge,relation_type=relation_type)
            list_id=list(friendlist.objects.filter(account=b).values('id'))[0]['id']
            uid_id_friend.objects.create(my_id=uid,friend_id=inv_id,relation_type=relation_type)
            requestlist.objects.filter(user_id=inv_id,whoami=uid).update(status=1,relation_id=list_id,read="true")
            status="0"
        else:
            status="1"
        return JsonResponse({"status":status})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt#第二十一個ＡＰＩ 拒絕邀請
def Friendrefuse(request,inv_id):
    if request.method == 'GET':
        uid=request.user.id
        status = "1"
        if requestlist.objects.filter(user_id=inv_id,whoami=uid).exists():
            requestlist.objects.filter(user_id=inv_id,whoami=uid).update(status=2,read="true")
            status = "0"
        return JsonResponse({"status":status})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt#二十二個ＡＰＩ 刪除邀請 有問題 有關刪除範圍
def Invite_remove(request,uid):
    if request.method == 'GET':
        user_id=request.user.id
        if uid == user_id and requestlist.objects.filter(user_id=uid).exists():
            requestlist.objects.filter(user_id=uid).delete()
            status="0"
        return JsonResponse({"status":status})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt#第二十三個ＡＰＩ 分享成果
def Share(request):
    if request.method == 'POST':
        uid=request.user.id
        type = request.POST['type']
        id = request.POST['id']
        relation_type = request.POST['relation_type']
        if int(type) in range(4):
            record.objects.create(user_id=uid,report_id=id,type=type,relation_type=relation_type)
            status="0"
            return JsonResponse({"status":status})
        else:
            status = "31"
        return JsonResponse({"status":status})
    else:
        status = "11"
        return JsonResponse({"status":status})


@csrf_exempt#第二十四ＡＰＩ 查看分享成果
def Share0(request,kind):
    if request.method == 'GET' :
        all_list=api24(request,kind)
        status = "0"
        return JsonResponse({"status":status,"records":all_list})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt#第二十五個ＡＰＩ 最後上傳時間
def Last_load(request):
    if request.method == 'GET':
        epmty=[]
        if bloodduck.objects.exists():
            bd_upt=list(bloodduck.objects.values("recorded_at"))
            for i in range(len(bd_upt)):
                epmty.append(str(bd_upt[i]['recorded_at']))
                epmty=sorted(epmty)
            bd_upt=epmty[-1]
            epmty=[]
        else:
            bd_upt="null"
        if weight.objects.exists():
            we_upt=list(weight.objects.values("recorded_at"))
            for i in range(len(we_upt)):
                epmty.append(str(we_upt[i]['recorded_at']))
                epmty=sorted(epmty)
            we_upt=epmty[-1]
            epmty=[]
        else:
            we_upt="null"
        if bloodsugar.objects.exists():
            bs_upt=list(bloodsugar.objects.values("recorded_at"))
            for i in range(len(bs_upt)):
                epmty.append(str(bs_upt[i]['recorded_at']))
                epmty=sorted(epmty)
            bs_upt=epmty[-1]
            epmty=[]
        else:
            bs_upt="null"
        if diet.objects.exists():
            di_upt=list(diet.objects.values("recorded_at"))
            for i in range(len(di_upt)):
                epmty.append(str(di_upt[i]['recorded_at']))
                epmty=sorted(epmty)
            di_upt=epmty[-1]
            epmty=[]
        else:
            di_upt="null"
        status="0"
        return JsonResponse({"status":status,"last_upload": {"blood_pressure":bd_upt,"weight": we_upt,
        "blood_sugar": bs_upt,"diet": di_upt}})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt#第二十六個ＡＰＩ 控糖團成果結算
def Results(request):
    if request.method == 'GET':
        alldic=list(requestlist.objects.values())
        al=list(requestlist.objects.values('id'))
        b=[]
        dic_i=0
        for i in range(len(alldic)):
            b.append(al[i]['id'])
            b=sorted(b)
        id_m=b[-1]+1    
        for i in range(id_m):
            if requestlist.objects.filter(id=i).exists():
                print(i)
                del alldic[dic_i]['whoami']
                friend_id=list(requestlist.objects.filter(id=i).values("relation_id"))[0]['relation_id']
                friend_dic=list(friendlist.objects.filter(id=friend_id).values())[0]
                alldic[dic_i]["relation"]=friend_dic
                dic_i+=1
        status="0"
        return JsonResponse({"status":status,"relation":alldic})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt#第27 28個ＡＰＩ 關懷
def Care(request):
    if request.method == 'POST':
        uid=request.user.id
        message = request.POST['message']
        if message is not None:
            caremessage.objects.create(user_id=uid,message=message)
            status="0"
            return JsonResponse({"status":status})
        else:
            status = "1"
            return JsonResponse({"status":status})
    elif request.method == 'GET':
        cares=caremessage.objects.values()
        readcare=list(cares)
        status = "0"
        return JsonResponse({"status":status,'cares':readcare})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt#第29個ＡＰＩ 獲取新聞 有問題 是否預設
def NEWS(request):
    if request.method == 'GET':
        uid=request.user.id
        getnews=news.objects.filter(member_id=uid).values()
        readnews=list(getnews)
        status="0"
        return JsonResponse({"status":status,'NEWS':readnews})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt#第30 31個ＡＰＩ 獲取就醫資訊
def Medical(request):
    if request.method == 'PATCH':
        d=GetRequestBody(request.body)
        dkey=list(d)
        if 'diabetes_type' in dkey:medical.objects.update(diabetes_type=d['diabetes_type'])
        if 'oad' in dkey:medical.objects.update(oad=d['oad'])
        if 'insulin' in dkey:medical.objects.update(insulin=d['insulin'])
        if 'anti_hypertensives' in dkey:medical.objects.update(anti_hypertensives=d['anti_hypertensives'])
        status="0"
        return JsonResponse({"status":status})
    elif request.method == 'GET':
        a=medical.objects.values()
        medinfo=list(a)
        status="0"
        return JsonResponse({"status":status,'medical_info':medinfo})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt#第32 33 34個ＡＰＩ 糖化血色素
def A1c(request):
    if request.method == 'POST':
        uid=request.user.id
        a1c = request.POST['a1c']
        recorded_at = request.POST['recorded_at']
        alc.objects.create(user_id=uid,a1c=a1c,recorded_at=recorded_at)
        status="0"
        return JsonResponse({"status":status})
    elif request.method == 'GET':
        alcd=alc.objects.values()
        readalc=list(alcd)
        status = "0"
        return JsonResponse({"status":status,'alcs':readalc})
    elif request.method == 'DELETE':
        d=same_key(request.body)
        c=list(d['ids'])
        for i in range(199):
            if str(i) in c:
                alc.objects.filter(id=str(i)).delete()
        status="0"
        return JsonResponse({"status":status})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt#第35個ＡＰＩ 個人設定
def Setting(request):
    if request.method == 'PATCH':
        uid=request.user.id
        d=GetRequestBody(request.body)
        dkey=list(d)
        if 'after_recording' in dkey:setting.objects.filter(user_id=uid).update(after_recording=d['after_recording'])
        if 'no_recording_for_a_day' in dkey:setting.objects.filter(user_id=uid).update(no_recording_for_a_day=d['no_recording_for_a_day'])
        if 'over_max_or_under_min' in dkey:setting.objects.filter(user_id=uid).update(over_max_or_under_min=d['over_max_or_under_min'])
        if 'after_meal' in dkey:setting.objects.filter(user_id=uid).update(after_meal=d['after_meal'])
        if 'unit_of_sugar' in dkey:setting.objects.filter(user_id=uid).update(unit_of_sugar=d['unit_of_sugar'])
        if 'unit_of_weight' in dkey:setting.objects.filter(user_id=uid).update(unit_of_weight=d['unit_of_weight'])
        if 'unit_of_height' in dkey:setting.objects.filter(user_id=uid).update(unit_of_height=d['unit_of_height'])
        status="0"
        return JsonResponse({"status":status})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt#第36個ＡＰＩ 發送給親友團
def Notification(request):
    if request.method == 'POST':
        news_twi=request.POST['message']
        uid=request.user.id
        friendid_list=list(uid_id_friend.objects.filter(my_id=uid,relation_type=1).values('friend_id'))
        for i in range(len(friendid_list)):
            friendid_list[i]=friendid_list[i]['friend_id']
            news.objects.create(member_id=friendid_list[i],message=news_twi)
        status="0"
        return JsonResponse({"status":status})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt#第37個ＡＰＩ 刪除更多好友 
def Remove(request):
    if request.method == 'DELETE':
        d=same_key(request)
        ids=list(d["ids"])
        for i in range(199):
            if str(i) in ids:
                friendlist.objects.filter(id=str(i)).delete()
        status="0"
        return JsonResponse({"status":status})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt#第38個ＡＰＩ
def Regcheck(request):
    if request.method == 'GET':
        d=GetRequestBody(request.body)
        account=d['account']
        if People.objects.filter(username=account).exists():
            status = "0"
            return JsonResponse({"status":status})
        else:
            status = "1"
            return JsonResponse({"status":status})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt#第39個ＡＰＩ
def Badge(request):
    if request.method == 'PUT':
        d=GetRequestBody(request.body)
        badge=d['badge']
        People.objects.update(badge=badge)
        status = "0"
        return JsonResponse({"status":status})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt#第40 44個ＡＰＩ  未完
def Dietrecord(request):
    if request.method == 'DELETE':
        d=GetRequestBody(request.body)
        bs_id=d['blood_sugars']
        bp_id=d['blood_pressures']
        w_id=d['weights']
        for i in range(200):
            if str(i) in bs_id:
                bloodsugar.objects.filter(id=bs_id).delete()
            if str(i) in bp_id:
                bloodduck.objects.filter(id=bp_id).delete()
            if str(i) in w_id:
                weight.objects.filter(id=w_id).delete()
        status = "0"
        return JsonResponse({"status":status})
    elif request.method == 'POST':
        # uid=2
        uid=request.user.id
        listbs=list(bloodsugar.objects.filter(user_id=uid).values())[0]
        listbd=list(bloodduck.objects.filter(user_id=uid).values())[0]
        listw=list(weight.objects.filter(user_id=uid).values())[0]
        print(listbd)
        status = "0"
        return JsonResponse({"status":status,"blood_sugars":listbs,"blood_pressures":listbd,"weights":listw})
    else:
        status = "1"
        return JsonResponse({"status":status})

@csrf_exempt#第41 42 43個ＡＰＩ
def Drug(request):
    if request.method == 'POST':
        uid=request.user.id
        type = request.POST['type']
        name = request.POST['name']
        recorded_at = request.POST['recorded_at']
        drug_useds.objects.create(user_id=uid,type=type,name=name,recorded_at=recorded_at)
        status="0"
        return JsonResponse({"status":status})
    elif request.method == 'GET':
        drug=drug_useds.objects.values()
        readdrug=list(drug)
        status = "0"
        return JsonResponse({"status":status,'drug_useds':readdrug})
    elif request.method == 'DELETE':
        d=same_key(request.body)
        c=list(d['ids'])
        for i in range(199):
            if str(i) in c:
                drug_useds.objects.filter(id=str(i)).delete()
        status="0"
        return JsonResponse({"status":status})
    else:
        status = "1"
        return JsonResponse({"status":status})

