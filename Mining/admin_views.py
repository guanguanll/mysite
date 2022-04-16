from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from Mining.tool_views import message_data


@xframe_options_exempt
@csrf_exempt
# 超级管理员登录的操作视图
def admin_login_index(request):
    return render(request, 'Super/admin_index.html', locals())


@xframe_options_exempt
@csrf_exempt
# 超级管理员登录的操作视图
def admin_loginout_index(request):
    return render(request, 'login/login.html', locals())


@xframe_options_exempt
@csrf_exempt
# 超级管理员登录智能绘图页面
def admin_draw_graph_one(request):
    return render(request, 'Super/admin_DrawGraph.html')


@xframe_options_exempt
@csrf_exempt
# 超级管理员登录数据管理中心页面
def admin_search_data(request):
    return render(request, 'Super/admin_SearchData.html')

@xframe_options_exempt
@csrf_exempt
# 超级管理员登录数据操作中心页面
def admin_data_operator(request):
    return render(request, 'Super/admin_DataOperator.html')


@xframe_options_exempt
@csrf_exempt
# 超级管理员登录数据库更新页面
def admin_database_update(request):
    return render(request, 'Super/admin_DataBaseUpdate.html')


@xframe_options_exempt
@csrf_exempt
# 管理员工的页面
def worker_manage(request):
    return render(request, 'Super/workerlist.html')


@xframe_options_exempt
@csrf_exempt
# 管理操作员的页面
def operator_manage(request):
    return render(request, 'Super/operatorlist.html')


@xframe_options_exempt
@csrf_exempt
# 员工列表数据接口
def worker_list_interface(request):
    data = [
        {'id': '001', 'username': 'zhangsan ', 'passwd': '123456789', 'usertype': 'worker'},
        {'id': '002', 'username': 'zhangsan ', 'passwd': '123456789', 'usertype': 'worker'},
        {'id': '003', 'username': 'zhangsan ', 'passwd': '123456789', 'usertype': 'worker'},
        {'id': '004', 'username': 'zhangsan ', 'passwd': '123456789', 'usertype': 'worker'},
        {'id': '005', 'username': 'zhangsan ', 'passwd': '123456789', 'usertype': 'worker'},
        {'id': '006', 'username': 'zhangsan ', 'passwd': '123456789', 'usertype': 'worker'},
        {'id': '007', 'username': 'zhangsan ', 'passwd': '123456789', 'usertype': 'worker'},
        {'id': '008', 'username': 'zhangsan ', 'passwd': '123456789', 'usertype': 'worker'},
        {'id': '009', 'username': 'zhangsan ', 'passwd': '123456789', 'usertype': 'worker'},
        {'id': '010', 'username': 'zhangsan ', 'passwd': '123456789', 'usertype': 'worker'},
    ]
    message = message_data(0, "", 5, data)
    return JsonResponse(message)


@xframe_options_exempt
@csrf_exempt
# 员工列表数据接口
def operator_list_interface(request):
    data = [
        {'id': '001', 'username': 'zhangsan ', 'passwd': '123456789', 'usertype': 'operator'},
        {'id': '002', 'username': 'zhangsan ', 'passwd': '123456789', 'usertype': 'operator'},
        {'id': '003', 'username': 'zhangsan ', 'passwd': '123456789', 'usertype': 'operator'},
        {'id': '004', 'username': 'zhangsan ', 'passwd': '123456789', 'usertype': 'operator'},
        {'id': '005', 'username': 'zhangsan ', 'passwd': '123456789', 'usertype': 'operator'},
        {'id': '006', 'username': 'zhangsan ', 'passwd': '123456789', 'usertype': 'operator'},
        {'id': '007', 'username': 'zhangsan ', 'passwd': '123456789', 'usertype': 'operator'},
        {'id': '008', 'username': 'zhangsan ', 'passwd': '123456789', 'usertype': 'operator'},
        {'id': '009', 'username': 'zhangsan ', 'passwd': '123456789', 'usertype': 'operator'},
        {'id': '010', 'username': 'zhangsan ', 'passwd': '123456789', 'usertype': 'operator'},
    ]
    message = message_data(0, "", 5, data)
    return JsonResponse(message)
