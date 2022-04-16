from django.http import JsonResponse
from django.shortcuts import render
from Mining.models import user_group
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

# 用户登录视图
def login(request):
    return render(request, 'Login/login.html')


# 用户登录认证视图
def user_login_check(request):
    status = ''  # 状态标识位
    if request.method == 'GET':
        return render(request, 'Login/login.html')
    else:
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            vercode = request.POST.get('vercode')
            role = request.POST.get('role')
            print('用户名:', username, '密码:', password, '验证码:', vercode, '角色', role)
            obj = user_group.objects.filter(username=username)
            if obj.count() != 0:
                if password == obj[0].userpwd:
                    if role == obj[0].usertype:
                        request.session['username'] = username
                        request.session['password'] = password
                        request.session['role'] = role
                        status = "success"
                    else:
                        print("role type is error!\n")
                        status = "fail"
                else:
                    print("password is error!\n")
                    status = "fail"
            else:
                print("user count is not exist! please check your count!\n")
                status = "fail"

            context = {'status': status, 'username': username, 'password': password, 'vercode': vercode, 'role': role}
        except:
            context['status'] = 'fail'
        finally:
            return JsonResponse(context)


# 用户退出登录视图
def user_logout(request):
    return render(request, 'Login/login.html')


@xframe_options_exempt
@csrf_exempt
# 用户密码找回视图
def user_pwd_recover(request):
    return render(request, '')


@xframe_options_exempt
@csrf_exempt
# 用户个人中心
def user_person(request):
    return render(request, "Person/Inform.html")
