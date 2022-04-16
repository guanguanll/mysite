import json
import random

from django.shortcuts import render, redirect
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from Mining.tool_views import message_data
from django.forms.models import model_to_dict
from .models import *


def operator_login_index(request):
    return render(request, 'Operator/operator_index.html', locals())


@xframe_options_exempt
@csrf_exempt
# 操作员核查钻孔视频验收监控记录列表
def check_videos_record_list(request):
    return render(request, 'Operator/videos_check_list_page.html')


@xframe_options_exempt
@csrf_exempt
# 操作员核查钻孔视频验收监控记录list渲染
def check_videos_record_rendering(request):
    data = [
        {'address': '三峡', 'kong_num': 1001, 'pian_angle': 20, 'direction': '向上', 'qing_angle': 30,
         'start_zuan_time': '10-11', 'flush_start_t': '10-11', 'flush_end_t': '11.12', 'mei_count': 111,
         'return_start_t': '12.10', 'return_end_t': '12.11', 'kong_depth': 231, 'feng_start_t': '12.22',
         'feng_end_t': '12.23', 'feng_kong_len': 11, 'shai_guan_len': 23, 'video_num': 1002,
         'error_msg': '冲me量不足', 'worker_name': '张三', 'video_people': '李四', 'submit_time': '12.24',
         'class_times': 223},

        {'address': '河南洛阳', 'kong_num': 1002, 'pian_angle': 20, 'direction': '向上', 'qing_angle': 30,
         'start_zuan_time': '10-11', 'flush_start_t': '10-11', 'flush_end_t': '11.12', 'mei_count': 111,
         'return_start_t': '12.10', 'return_end_t': '12.11', 'kong_depth': 231, 'feng_start_t': '12.22',
         'feng_end_t': '12.23', 'feng_kong_len': 11, 'shai_guan_len': 23, 'video_num': 1002,
         'error_msg': '冲me量不足', 'worker_name': '张三', 'video_people': '李四', 'submit_time': '12.24',
         'class_times': 223},
    ]

    msg = {"code": 0, "data": data}
    return JsonResponse(msg)


@xframe_options_exempt
@csrf_exempt
# 操作员核查钻孔视频监控记录填写
def check_videos_record_fillin(request):
    return render(request, 'Operator/videos_check_submit.html')


@xframe_options_exempt
@csrf_exempt
# 操作员核查钻孔视频举牌记录list
def check_videos_holding_record_list(request):
    return render(request, 'Operator/jupai_required_list.html')


@xframe_options_exempt
@csrf_exempt
# 操作员核查钻孔视频举牌监控记录列表的渲染
def check_videos_holding_record_rendering(request):
    data = [
        {"id": 1, "kong_num": '10001', "kai_kong_req": "是", "kai_kong_hold": "是", "see_mei_hold": "是", "see_ding_hold": "是",
         "end_kong_hold": "是", 'return_zuan_hold': "否", "flush_kong_hold": "否", "fill_kong_start_hold": "是",
         "fill_kong_check_hold": "是"},
        {"id": 2, "kong_num": '10002', "kai_kong_req": "是", "kai_kong_hold": "是", "see_mei_hold": "是", "see_ding_hold": "是",
         "end_kong_hold": "是", 'return_zuan_hold': "否", "flush_kong_hold": "否", "fill_kong_start_hold": "是",
         "fill_kong_check_hold": "是"},
        {"id": 3, "kong_num": '10003', "kai_kong_req": "是", "kai_kong_hold": "是", "see_mei_hold": "是", "see_ding_hold": "是",
         "end_kong_hold": "是", 'return_zuan_hold': "否", "flush_kong_hold": "否", "fill_kong_start_hold": "是",
         "fill_kong_check_hold": "是"},
        {"id": 4, "kong_num": '10004', "kai_kong_req": "是", "kai_kong_hold": "是", "see_mei_hold": "是", "see_ding_hold": "是",
         "end_kong_hold": "是", 'return_zuan_hold': "否", "flush_kong_hold": "否", "fill_kong_start_hold": "是",
         "fill_kong_check_hold": "是"},
        {"id": 5, "kong_num": '10005', "kai_kong_req": "是", "kai_kong_hold": "是", "see_mei_hold": "是", "see_ding_hold": "是",
         "end_kong_hold": "是", 'return_zuan_hold': "否", "flush_kong_hold": "否", "fill_kong_start_hold": "是",
         "fill_kong_check_hold": "是"},
        ]
    msg = {"code": 0, "data": data}
    return JsonResponse(msg)


@xframe_options_exempt
@csrf_exempt
# 核查视频举牌记录的数据填充
def check_videos_holding_record_fillin(request):
    return render(request, "Operator/jupai_required.html")


@xframe_options_exempt
@csrf_exempt
# 操作员核查钻孔施工资料记录list
def check_material_record_list(request):
    return render(request, 'Operator/file_check_list_page.html')


@xframe_options_exempt
@csrf_exempt
# 操作员核查钻孔施工资料记录list的数据渲染
def check_material_record_rendering(request):
    data = [
        {'kong_num': 1001, 'open_kong_require': '是', 'open_kong_hold': '是', 'submit_status': 1,
         'submit_times': '2021-11-12', 'submit_person': '李四'},
        {'kong_num': 1002, 'open_kong_require': '是', 'open_kong_hold': '是', 'submit_status': 1,
         'submit_times': '2021-11-12', 'submit_person': '李四'},
        {'kong_num': 1003, 'open_kong_require': '是', 'open_kong_hold': '是', 'submit_status': 1,
         'submit_times': '2021-11-12', 'submit_person': '李四'},
        {'kong_num': 1004, 'open_kong_require': '是', 'open_kong_hold': '是', 'submit_status': 1,
         'submit_times': '2021-11-12', 'submit_person': '李四'},
        {'kong_num': 1005, 'open_kong_require': '是', 'open_kong_hold': '是', 'submit_status': 1,
         'submit_times': '2021-11-12', 'submit_person': '李四'},
    ]

    msg = {"code": 0, "data": data}
    return JsonResponse(msg)


@xframe_options_exempt
@csrf_exempt
# 操作员核查施工资料记录的数据填充
def check_material_record_fillin(request):
    return render(request, 'Operator/')


@xframe_options_exempt
@csrf_exempt
# 跳转到巷道选择页面
def goto_roadway_choose_viewpage(request):
    return render(request, 'Operator/Roadway_Choose.html')


@xframe_options_exempt
@csrf_exempt
# 跳转到申请记录页面
def goto_apply_record_viewpage(request):
    return render(request, 'Operator/apply_record.html')


@xframe_options_exempt
@csrf_exempt
# 申请记录的数据渲染
def goto_apply_record_rendering(request):
    data = [
        {"id": 1, "apply_num": '1000001', "apply_person": "小王", "apply_inform": "开始打钻10001号孔",
         "apply_status": "未读", "apply_msg": "审核通过"},
        {"id": 2, "apply_num": '1000002', "apply_person": "小李", "apply_inform": "开始打钻10002号孔",
         "apply_status": "未通过", "apply_msg": "申请的孔号有误，请重新申请"},
        ]
    msg = {"code": 0, "data": data}
    return JsonResponse(msg)


@xframe_options_exempt
@csrf_exempt
# 跳转到审批记录页面
def goto_approve_record_viewpage(request):
    return render(request, 'Operator/approve_record.html')


@xframe_options_exempt
@csrf_exempt
# 跳转到审批记录数据渲染
def goto_approve_record_rendering(request):
    apply_record_obj = Apply_Record.objects.all()
    apply_record = []
    for item in apply_record_obj:
        apply_record.append(model_to_dict(item))
    message = message_data(0, "", len(apply_record), apply_record)
    return JsonResponse(message)


# -------------------------------------视屏监控验收-------------------------------

@xframe_options_exempt
@csrf_exempt
# 视屏监控数据填报接收
def videos_data_submit_process(request):
    if request.method == "POST":
        data = request.POST["data"]
        submit_data = json.loads(data)
        print(submit_data)
        message = {"code": 0, "msg": '提交成功!'}
    else:
        message = {"code": 1, "msg": '提交失败!'}
    return JsonResponse(message)


# -------------------------------------视屏举牌验收-------------------------------
@xframe_options_exempt
@csrf_exempt
# 视屏举牌数据填报验收
def videos_juipai_submit_process(request):
    if request.method == "POST":
        data = request.POST["data"]
        print(json.loads(data))
        message = {"code": 0, "msg": '提交成功!'}
    else:
        message = {"code": 1, "msg": '提交失败!'}
    return JsonResponse(message)



# -------------------------------------施工资料验收-------------------------------
@xframe_options_exempt
@csrf_exempt
# 施工资料验收填报
def file_check_submit_process(request):
    if request.method == "POST":
        data = request.POST["data"]
        print(json.loads(data))
        message = {"code": 0, "msg": '提交成功!'}
    else:
        message = {"code": 1, "msg": '提交失败!'}
    return JsonResponse(message)