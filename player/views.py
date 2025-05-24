from django.shortcuts import render, redirect
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from .models import Profile
from datetime import datetime, timezone
import uuid

User = get_user_model()

#註冊帳號
def signup_view(request):
    errorMessage = None

    if request.method == 'POST':
        print("收到POST請求")

        #讀取輸入資料
        account = request.POST.get('account', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirmPassword', '')
        print(f'account {account}')

        #密碼一致性確認
        if confirm_password != password:
            errorMessage = "密鑰配對錯誤：請輸入密鑰確保同步性"
            return render(request, 'player/signup.html', {'errorMessage': errorMessage})
        print("完成密碼確認")
        
        #密碼強度檢查
        try:
            validate_password(password)
        #將錯誤內容指派給變數e
        except ValidationError as e:
            errorMessage = "密鑰驗證失敗：輸入密鑰不符通訊規範"
            return render(request, 'player/signup.html', {'errorMessage': errorMessage})
        print("通過密碼認證")
        
        #帳號唯一性確認
        if User.objects.filter(username = account).exists():
            errorMessage = "識別衝突：該識別碼已在通訊系統內登記"
            return render(request, 'player/signup.html', {'errorMessage': errorMessage})
        #帳號唯一性確認
        if User.objects.filter(email = email).exists():
            errorMessage = "端口衝突：該通訊端口已綁定其他識別碼"
            return render(request, 'player/signup.html', {'errorMessage': errorMessage})
        print("通過唯一性認證")
        
        #建立新帳號
        user = User.objects.create_user(username = account, email = email, password = password)
        user.is_active = False
        user.save()
        print("成功建立帳號")

        #暫時記住用戶
        request.session['tempUserId'] = str(user.id)
        request.session['postConsentRedirect'] = '/player/login'
        return redirect('player:welcome')
    
    return render(request, 'player/signup.html')

#帳號驗證
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk = uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        print("成功啟用帳號")
        return redirect('player:login')
    
    else:
        #要換html
        return render(request, 'signup.html')

#同意書並簽名
def consent_form_view(request):
    #獲取用戶
    userId = request.session.get('tempUserId')

    #攔截非註冊進入
    #if not userId:
    #    return redirect('signup')
    
    user = User.objects.get(pk = userId)

    if not request.session.get('signupEmail'):
        print("首次開啟同意書")
        #寄送驗證信
        currentSite = get_current_site(request)
        mailSubject = '📡 Welcome to No.3 BASE – The Last Safe Zone'
        message = render_to_string('player/signupEmail.html', {
            'user': user,
            'domain': currentSite,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user)
        })
        send_mail(mailSubject, message, 'BASE 03 控管中心 <no3base.notify@gmail.com>', [user.email], html_message=message)
        print("成功寄送驗證")

    if request.method == 'POST':
        print("收到POST請求")
        
        #讀取輸入資料
        name = request.POST.get('name')
        user.first_name = name
        user.save()
        print(name)

        nextUrl = request.session.pop('postConsentRedirect', '/player/login')
        return redirect(nextUrl)
        #return redirect('player:login')
    
    #設定協調時間
    zuluTime = user.date_joined.strftime("ZULU TIME %Y.%m.%d | %H:%M")

    return render(request, 'player/consent_form.html', {
        'account': user.username,
        'zuluTime': zuluTime
    })

#登入帳號
def login_view(request):
    errorMessage = None

    if request.method == 'POST':
        print("收到POST請求")

        #讀取輸入資料
        account = request.POST.get('account')
        password = request.POST.get('password')
        rember = request.POST.get('remberMe')
        print(f'account {account}')

        #確認帳號狀況
        try:
            userObj = User.objects.get(username = account)
            print("確認帳號存在")
        except User.DoesNotExist:
            errorMessage = "識別失敗：查無此通訊帳號"
            print("查無帳號")
            return render(request, 'player/login.html', {'errorMessage': errorMessage})
        
        #帳號存在進行登入
        user = authenticate(request, username = account, password = password)
        print(user)

        if user is not None:
            #登入成功進行記住綁定
            login(request, user)
            
            #每日登入經驗
            try:
                profile = user.profile
                now = datetime.now(timezone.utc).date()

                if profile.loginExpGainDate != now:
                    profile.exp += 5
                    profile.loginExpGainDate = now

                profile.recalculate_level()
                profile.save()
            except User.DoesNotExist:
                pass

            #記住帳號設定
            if not rember:
                request.session.set_expiry(0)
                print("不記住帳號")
            else:
                request.session.set_expiry(60*60*24*180)
                print("記住帳號")
            
            #如果沒有完成暱稱設定（視為未同意規則）
            if not user.first_name:
                #暫時記住用戶
                request.session['tempUserId'] = str(user.id)
                request.session['postConsentRedirect'] = request.GET.get('next') or '/'
                return redirect('player:welcome')

            nextUrl = request.GET.get('next') or '/'
            return redirect(nextUrl)
        
        else:
            #密碼錯誤登入失敗
            errorMessage = "驗證失敗：請確認您的通訊密鑰"

    return render(request, 'player/login.html', {'errorMessage': errorMessage})

#登出帳號
def logout_view(request):
    logout(request)
    nextUrl = request.GET.get('next') or '/'
    return redirect(nextUrl)