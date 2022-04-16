import json
import random

from django.shortcuts import render, redirect
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from Mining.tool_views import message_data
from django.forms.models import model_to_dict
from .models import *


# 工人登录的操作视图
def worker_login_index(request):
    return render(request, 'Worker/worker_index.html', locals())


@xframe_options_exempt
@csrf_exempt
# 巷道选择界面
def drill_roadway_choosed(request):
    work_face_obj = Work_face.objects.values_list("w_name")
    tunnel_obj = Tunnel.objects.values_list("tunnel_name")
    row_obj = Row.objects.values_list("row_id")
    return render(request, "Worker/roadway_choose.html",
                  {"work_face": work_face_obj, "tunnel": tunnel_obj, "row": row_obj})


@xframe_options_exempt
@csrf_exempt
# 巷道选择后的数据提交
def drill_roadway_choosed_res(request):
    if request.method == "POST":
        row_id = request.POST["row"]
        row_data = Row.objects.filter(row_id=row_id)
        if row_data.count() > 0:
            request.session['row_id'] = row_data[0].id
            request.session['row_num'] = row_data[0].row_id
        else:
            request.session['row_id'] = -1
            request.session['row_num'] = -1
    return render(request, "Worker/roadway_choose.html")


@xframe_options_exempt
@csrf_exempt
# 跳转工程信息填报界面
def project_report_page(request):
    return render(request, 'Login/Company_Choose.html', locals())


@xframe_options_exempt
@csrf_exempt
# 工程列表视图
def worker_project_list(request):
    return render(request, 'Worker/project_list.html')


@xframe_options_exempt
@csrf_exempt
# 工程评价列表视图
def project_eval_list(request):
    return render(request, 'Worker/evaluate_project.html')


@xframe_options_exempt
@csrf_exempt
# 钻孔数据填报列表视图
def project_data_input(request):
    return render(request, 'Worker/data_input.html')


@xframe_options_exempt
@csrf_exempt
# 获取工程列表视图
def get_project_list(request):
    data = [
        {"id": 1, "kong_num": 1001, "pian_angle": 20, "yang_angle": 10, "kong_length": 100, "yan_kong_length": 100,
         "mei_duan_length": 120, "chong_mei_count": 1200},
        {"id": 2, "kong_num": 1002, "pian_angle": 20, "yang_angle": 10, "kong_length": 100, "yan_kong_length": 100,
         "mei_duan_length": 120, "chong_mei_count": 1200},
        {"id": 3, "kong_num": 1003, "pian_angle": 20, "yang_angle": 10, "kong_length": 100, "yan_kong_length": 100,
         "mei_duan_length": 120, "chong_mei_count": 1200},
        {"id": 4, "kong_num": 1004, "pian_angle": 20, "yang_angle": 10, "kong_length": 100, "yan_kong_length": 100,
         "mei_duan_length": 120, "chong_mei_count": 1200},
        {"id": 5, "kong_num": 1005, "pian_angle": 20, "yang_angle": 10, "kong_length": 100, "yan_kong_length": 100,
         "mei_duan_length": 120, "chong_mei_count": 1200},
    ]
    message = message_data(0, "", 5, data)
    return JsonResponse(message)


@xframe_options_exempt
@csrf_exempt
# 获取工程列表视图
def get_evaluate_list(request):
    data = [
        {"id": 1, "kong_num": 1001, "see_mei_eval": "合格", "see_ding_eval": "不合格", "kong_space_eval": "合格",
         "chong_mei_eval": "合格", "add_kong_req": "无需补孔"},
        {"id": 2, "kong_num": 1002, "see_mei_eval": "合格", "see_ding_eval": "不合格", "kong_space_eval": "合格",
         "chong_mei_eval": "合格", "add_kong_req": "无需补孔"},
        {"id": 3, "kong_num": 1003, "see_mei_eval": "合格", "see_ding_eval": "不合格", "kong_space_eval": "合格",
         "chong_mei_eval": "合格", "add_kong_req": "无需补孔"},
        {"id": 4, "kong_num": 1004, "see_mei_eval": "合格", "see_ding_eval": "不合格", "kong_space_eval": "合格",
         "chong_mei_eval": "合格", "add_kong_req": "无需补孔"},
        {"id": 5, "kong_num": 1005, "see_mei_eval": "合格", "see_ding_eval": "不合格", "kong_space_eval": "合格",
         "chong_mei_eval": "合格", "add_kong_req": "无需补孔"},
    ]
    message = message_data(0, "", 5, data)
    return JsonResponse(message)


@xframe_options_exempt
@csrf_exempt
# 获取钻孔数据列表视图
def get_dataInput_list(request):
    data = [
        {"id": 1, "kong_num": 1001, "pian_angle": 32, "yang_angle": 33, "see_mei": 123, "see_ding": 233,
         "kong_length": 2232, "chong_mei": 124},
        {"id": 2, "kong_num": 1002, "pian_angle": 32, "yang_angle": 33, "see_mei": 123, "see_ding": 233,
         "kong_length": 2232, "chong_mei": 124},
        {"id": 3, "kong_num": 1003, "pian_angle": 32, "yang_angle": 33, "see_mei": 123, "see_ding": 233,
         "kong_length": 2232, "chong_mei": 124},
        {"id": 4, "kong_num": 1004, "pian_angle": 32, "yang_angle": 33, "see_mei": 123, "see_ding": 233,
         "kong_length": 2232, "chong_mei": 124},
        {"id": 5, "kong_num": 1005, "pian_angle": 32, "yang_angle": 33, "see_mei": 123, "see_ding": 233,
         "kong_length": 2232, "chong_mei": 124},
        {"id": 6, "kong_num": 1006, "pian_angle": 32, "yang_angle": 33, "see_mei": 123, "see_ding": 233,
         "kong_length": 2232, "chong_mei": 124},
    ]
    message = message_data(0, "", 5, data)
    return JsonResponse(message)


@xframe_options_exempt
@csrf_exempt
# 工人填报钻孔数据
def worker_load_data(request):
    if request.method == "POST":
        data = request.POST.get('param1')
        print(data)
        message = message_data(0, "数据上传成功!", 0, None)
        return JsonResponse(message)
    else:
        print("111111111111111")
        message = message_data(0, "数据上传方式有误!", 0, None)
        return JsonResponse(message)


@xframe_options_exempt
@csrf_exempt
# 跳转到钻孔设计参数页面
def drilling_design_params(request):
    return render(request, 'Worker/Drilling_Design_Params.html')


@xframe_options_exempt
@csrf_exempt
def drilling_design_params_fill(request):
    row_id = request.session["row_id"]
    row_num = request.session["row_num"]
    hole_design_data = Hole_Design.objects.filter(row=row_id)
    hole_list = []
    hole_data = []
    for item in hole_design_data:
        hole_list.append(model_to_dict(item))
    for i in range(len(hole_list)):
        hole_data.append({"id": i + 1, "pai_num": row_num, "kong_num": hole_list[i]['hole_number'],
                          "pian_angle": round(hole_list[i]['deflection_angle'], 3),
                          "yang_angle": round(hole_list[i]['design_elevation_angel'], 3),
                          "kong_length": round(hole_list[i]['hole_depth'], 3),
                          "yan_kong_length": round(hole_list[i]['rock_section'], 3),
                          "mei_duan_length": round(hole_list[i]['coal_section'], 3),
                          "wash_coal": hole_list[i]['weight_of_flush_coal'],
                          "see_ding_tip": "预计%d米见岩，请缓慢钻进并注意见顶辨识" % (hole_list[i]['see_ceil'] - 1),
                          "see_mei_tip": "预计%d米见煤，请缓慢钻进并注意见煤辨识" % (hole_list[i]['rock_section'] - 1)})
    message = message_data(0, "", len(hole_list), hole_data)
    return JsonResponse(message)


@xframe_options_exempt
@csrf_exempt
# 钻孔施工填报表
def drill_working_data_fillin(request):
    return render(request, "Table_Inform/worker_submit_table1.html")


@xframe_options_exempt
@csrf_exempt
# 冲孔数据填报表
def drill_wash_data_fillin(request):
    return render(request, "Table_Inform/worker_submit_table2.html")


@xframe_options_exempt
@csrf_exempt
# 封孔数据填报表
def drill_sealing_data_fillin(request):
    return render(request, "Table_Inform/worker_submit_table3.html")


@xframe_options_exempt
@csrf_exempt
# 反馈信息页面
def drill_feedback_massage_fillin(request):
    return render(request, "Worker/feedback_massage.html")


@xframe_options_exempt
@csrf_exempt
# 反馈信息页面数据填充
def drill_feedback_data_fillin(request):
    record_obj = Apply_Record.objects.filter(apply_person=request.session["username"])
    record_data = []
    if record_obj.count() > 0:
        for item in record_obj:
            item_dict = model_to_dict(item)
            apply_time = item_dict['apply_time']
            item_dict['apply_time'] = str(apply_time)
            record_data.append(item_dict)
        message = message_data(0, "", record_obj.count(), record_data)
        print(record_data)
    else:
        message = message_data(0, "", record_obj.count(), record_data)
    return JsonResponse(message)


@xframe_options_exempt
@csrf_exempt
# 跳转到预警提醒页面
def warning_reminder(request):
    return render(request, 'Worker/Warning_Reminder.html')


@xframe_options_exempt
@csrf_exempt
# 跳转到封孔注浆设计参数页面
def sealing_grouting_design_params(request):
    return render(request, 'Worker/Sealling_Grouting_Design.html')


@xframe_options_exempt
@csrf_exempt
# 跳转到现场打钻参数页面
def site_drill_page(request):
    return render(request, 'Worker/Site_Drill.html')


@xframe_options_exempt
@csrf_exempt
# 跳转到现场验收页面
def site_confirm_page(request):
    return render(request, 'Worker/Site_Accepting.html')


@xframe_options_exempt
@csrf_exempt
# 跳转到封孔注浆页面
def seal_grout_page(request):
    return render(request, 'Worker/Seal_Grouting.html')


@xframe_options_exempt
@csrf_exempt
# 跳转到地面确认页面
def ground_confirm_page(request):
    return render(request, 'Worker/Ground_Confirm.html')


@xframe_options_exempt
@csrf_exempt
# 跳转到打钻质量评价页面
def drill_quality_assess(request):
    return render(request, 'Worker/Drill_Quality_Assess.html')


@xframe_options_exempt
@csrf_exempt
# 跳转到空白区域评价页面
def empty_area_assess(request):
    return render(request, 'Worker/Empty_Area_Assess.html')


@xframe_options_exempt
@csrf_exempt
# 跳转到封孔注浆评价页面
def seal_grouting_assess(request):
    return render(request, 'Worker/Seal_Grouting_Assess.html')


@xframe_options_exempt
@csrf_exempt
# 跳转到异常处置页面
def exception_handle_page(request):
    return render(request, 'Worker/Exception_Handle.html')


@xframe_options_exempt
@csrf_exempt
# 跳转到钻孔施工参数页面
def drilling_construction_params(request):
    return render(request, 'Worker/Drilling_Design_Params.html')


@xframe_options_exempt
@csrf_exempt
# 钻孔申报路由
def drill_apply_record_page(request):
    if request.method == "POST":
        data = request.POST["data"]
        json_data = json.loads(data)
        bian_num = int(json_data['pai_num']) * 100000 + random.randint(0, 10000)
        user_name = request.session['username']
        apply_inform = "申请开" + json_data['pai_num'] + "排" + json_data["kong_num"] + "号孔"
        apply_status = "待审核"
        apply_msg = "暂无"
        apply_inform_search = Apply_Record.objects.filter(kong_num=json_data["kong_num"])
        if apply_inform_search.count() > 0:
            message = {"code": 1, "msg": '该孔号已经被申请!'}
        else:
            new_record = Apply_Record(apply_id=bian_num, apply_person=user_name, pai_num=int(json_data["pai_num"]),
                                      kong_num=json_data["kong_num"], pian_angle=float(json_data["pian_angle"]),
                                      yang_angle=float(json_data["yang_angle"]),
                                      kong_length=float(json_data["kong_length"]),
                                      yan_kong_length=float(json_data["yan_kong_length"]),
                                      mei_duan_length=float(json_data["mei_duan_length"]),
                                      flush_mei_count=float(json_data["wash_coal"]), apply_inform=apply_inform,
                                      apply_status=apply_status, reback_msg=apply_msg)
            new_record.save()
            message = {"code": 0, "msg": '申请成功!'}
    return JsonResponse(message)


# ----------------------------------钻孔施工填报-----------------------------------------
# 跳转到钻孔施工数据列表
@xframe_options_exempt
@csrf_exempt
def goto_drill_construct_list_page(request):
    return render(request, "Worker/construct_list_page.html")


# 给钻孔施工数据列表刷新数据
@xframe_options_exempt
@csrf_exempt
def flush_drill_construct_list_data(request):
    data = [{
        "id": 1, "work_place": "河南", "work_date": "2021-10-21", "pai_num": "100021", "kong_num": "B2-12",
        "design_angle": "32.221",
        "check_angle": "12.22", "design_dip_angle": "13.443", "check_dip_angle": "12.33", "design_see_mei": "23.445",
        "actual_see_mei": "12.321", "design_length": "12.445", "actual_length": "43.121", "pass_coal_seam": "22.34",
        "pass_length": "234.4", "error_msg": "暂无", "drill_assess": "暂无", "work_person": "张三", "check_person": "李四"
    },
        {
            "id": 2, "work_place": "山东", "work_date": "2021-10-21", "pai_num": "100021", "kong_num": "B2-12",
            "design_angle": "32.221",
            "check_angle": "12.22", "design_dip_angle": "13.443", "check_dip_angle": "12.33",
            "design_see_mei": "23.445",
            "actual_see_mei": "12.321", "design_length": "12.445", "actual_length": "43.121", "pass_coal_seam": "22.34",
            "pass_length": "234.4", "error_msg": "暂无", "drill_assess": "暂无", "work_person": "张三", "check_person": "李四"
        },
    ]
    message = message_data(0, "", 5, data)
    return JsonResponse(message)


# 跳转到钻孔施工数据列表
@xframe_options_exempt
@csrf_exempt
def goto_drill_construct_layer_page(request):
    return render(request, "Worker/construct_submit_layer.html")


# ----------------------------------冲孔填报-----------------------------------------
# 跳转到冲孔列表
@xframe_options_exempt
@csrf_exempt
def goto_flush_drill_list_page(request):
    return render(request, "Worker/flush_drill_list_page.html")


# 冲孔数据列表刷新
@xframe_options_exempt
@csrf_exempt
def goto_flush_drill_list_data(request):
    data = [
        {
            "id": 1, "pai_num": "10021", "kong_num": "B9-10", "flush_date": "2021-12-10", "actual_mei_count": "123.32",
            "drill_redius": "34.334", "flush_start_time": "34.334", "flush_end_time": "34.334",
            "class_flush_mei": "34.334",
            "flush_volume": "34.334", "assess_flush": "34.334", "work_person": "34.334", "check_person": "34.334",
        },
        {
            "id": 2, "pai_num": "10021", "kong_num": "B9-10", "flush_date": "2021-12-10", "actual_mei_count": "123.32",
            "drill_redius": "34.334", "flush_start_time": "34.334", "flush_end_time": "34.334",
            "class_flush_mei": "34.334",
            "flush_volume": "34.334", "assess_flush": "34.334", "work_person": "34.334", "check_person": "34.334",
        },
    ]

    message = message_data(0, "", 5, data)
    return JsonResponse(message)


# 冲孔数据填报表单
@xframe_options_exempt
@csrf_exempt
def goto_flush_drill_layer_page(request):
    return render(request, "Worker/flush_drill_submit_layer.html")


# ----------------------------------封孔填报-----------------------------------------
# 跳转到封孔列表
@xframe_options_exempt
@csrf_exempt
def goto_feng_drill_list_page(request):
    return render(request, "Worker/feng_drill_list_page.html")


# 封孔数据列表刷新
@xframe_options_exempt
@csrf_exempt
def goto_feng_drill_list_data(request):
    data = [
        {
            "id": 1, "pai_num": "10021", "kong_num": "B9-10", "feng_date": "2021-12-10", "feng_drill_length": "123.32",
            "screen_length": "34.334", "grouting_count": "34.334", "grouting_pressure": "34.334",
            "feng_assess": "34.334", "work_person": "34.334", "check_person": "34.334",
        },

        {
            "id": 2, "pai_num": "10022", "kong_num": "B9-10", "feng_date": "2021-12-10", "feng_drill_length": "123.32",
            "screen_length": "34.334", "grouting_count": "34.334", "grouting_pressure": "34.334",
            "feng_assess": "34.334", "work_person": "34.334", "check_person": "34.334",
        },

    ]

    message = message_data(0, "", 5, data)
    return JsonResponse(message)


# 封孔数据填报表单
@xframe_options_exempt
@csrf_exempt
def goto_feng_drill_layer_page(request):
    return render(request, "Worker/feng_drill_submit_layer.html")
