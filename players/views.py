from django.shortcuts import render, redirect
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator


def signup_view(request):
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
            return render(request, 'players/signup.html', {'error': '確認密碼錯誤'})
        print("完成密碼確認")
        
        #密碼強度檢查
        try:
            validate_password(password)
        #將錯誤內容指派給變數e
        except ValidationError as e:
            return render(request, 'players/signup.html', {'error': e.messages[0]})
        print("通過密碼認證")
        
        #帳號唯一性確認
        if User.objects.filter(username = account).exists():
            return render(request, 'players/signup.html', {'error': '帳號已被註冊'})
        #帳號唯一性確認
        if User.objects.filter(email = email).exists():
            return render(request, 'players/signup.html', {'error': '帳號已被註冊'})
        print("通過唯一性認證")
        
        #建立新帳號
        user = User.objects.create_user(username = account, email = email, password = password)
        user.is_active = False
        user.save()
        print("成功建立帳號")

        #寄送驗證信
        current_site = get_current_site(request)
        mail_subject = '📡 Welcome to No.3 BASE – The Last Safe Zone'
        message = render_to_string('players/signupEmail.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user)
        })
        send_mail(mail_subject, message, 'BASE 03 控管中心 <no3base.notify@gmail.com>', [email], html_message=message)
        print("成功寄送驗證")

        return render(request, 'players/signup.html', {'message': '請到您的信箱點擊驗證連結完成註冊'})
    
    return render(request, 'players/signup.html')

def login_view(request):
    if request.method == 'POST':
        print("收到POST請求")

        #讀取輸入資料
        account = request.POST.get('account')
        password = request.POST.get('password')
        rember = request.POST.get('remberMe')
        print(f'account {account}')

        user = authenticate(request, username = account, password = password)
        print(user)

        if user is not None:
            login(request, user)

            if not rember:
                request.session.set_expiry(0)
                print("不記住帳號")
            else:
                request.session.set_expiry(60*60*24*180)
                print("記住帳號")


    return render(request, 'players/login.html')

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
        return redirect('login')
    
    else:
        #要換html
        return render(request, 'signup.html')
