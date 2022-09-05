import json
import math

from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from Mining.tool_views import message_data
from django.forms.models import model_to_dict
from .models import *
from django.core import serializers
from django.core.paginator import Paginator  # Django内置分页功能模块
# from util.tests import *
from util.enum import statusChoice


# 工人登录的操作视图
def worker_login_index(request):
    userName = request.session.get("username")
    return render(request, 'Worker/worker_index.html', locals())

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
    result = {}
    user = user_group.objects.filter(username=request.session.get("username")).first()
    if user is not None:
        belongMine = user.belongMine
        work_face = Work_face.objects.filter(mine=belongMine)
        if work_face is not None:
            work_face_obj = work_face.values_list("id", "w_name")
            result['work_face'] = work_face_obj
    return render(request, 'Worker/Drilling_Design_Params.html', result)


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
# 跳转到异常处置页面
def exception_handle_page(request):
    return render(request, 'Worker/Exception_Handle.html')


@xframe_options_exempt
@csrf_exempt
# 跳转到钻孔施工参数页面
def drilling_construction_params(request):
    # 先定义一个result
    result = {}
    # work_face_obj = Work_face.objects.values_list("w_name")
    user = user_group.objects.filter(username=request.session.get("username")).first()
    if user is not None:
        belongMine = user.belongMine
        work_face = Work_face.objects.filter(mine=belongMine)
        if work_face is not None:
            work_face_obj = work_face.values_list("id", "w_name")
            result['work_face'] = work_face_obj
    return render(request, 'Worker/drillingApplication.html', result)
    # return render(request, 'Worker/Drilling_Design_Params.html')


@csrf_exempt
# 钻孔申请路由
def drill_apply_record_page(request):
    if request.method == "POST":
        data = request.POST["data"]
        json_data = json.loads(data)
        user_name = request.session['username']
        rowId = json_data['row']
        holeNum = json_data['hole_number']
        if rowId:
            rows = Row.objects.filter(id = rowId)
            if rows:
                row = rows.first()
                # apply_inform = "申请开" + row.row_id + "排" + holeNum + "号孔"
                holeDesign = Hole_Design.objects.get(hole_number=holeNum, row= row)
                isFirstHole = holeDesign.isFirstHole
                status = holeDesign.status
                if "0" == isFirstHole and "-1" == status:
                    # 如果是首孔,且状态非驳回
                    design_hole_height = holeDesign.design_hole_height
                    rock_section = holeDesign.rock_section
                    arch_radius = holeDesign.row.tunnel.arch_radius
                    design_elevation_angel = holeDesign.design_elevation_angel
                    chuan_ding_length = holeDesign.row.tunnel.work_face.chuan_ding_length
                    see_ceil = holeDesign.see_ceil
                    kai_kong_pou_x = 0
                    kai_kong_pou_y = design_hole_height
                    design_jian_mei_x = format(
                        (holeDesign.rock_section + arch_radius) * math.cos((design_elevation_angel / 180) * math.pi),
                        '.2f')
                    design_jian_mei_y = format(design_hole_height + (rock_section + arch_radius) *
                                               math.sin((design_elevation_angel / 180) * math.pi), '.2f')
                    design_jian_ding_x = format(
                        (see_ceil + arch_radius) * math.cos((design_elevation_angel / 180) * math.pi), '.2f')
                    design_jian_ding_y = format(design_hole_height + (see_ceil + arch_radius) *
                                                math.sin((design_elevation_angel / 180) * math.pi), '.2f')
                    zhong_kong_length = float(chuan_ding_length) + see_ceil  # 终孔长度
                    design_zhong_kong_x = format(
                        (zhong_kong_length + arch_radius) * math.cos((design_elevation_angel / 180) * math.pi),
                        '.2f')
                    design_zhong_kong_y = format(design_hole_height + (zhong_kong_length + arch_radius) *
                                                 math.sin((design_elevation_angel / 180) * math.pi), '.2f')

                    my_record1 = Hole_Design_Pou_Mian(design_jian_mei_x=design_jian_mei_x,
                                                      design_jian_mei_y=design_jian_mei_y,
                                                      design_jian_ding_x=design_jian_ding_x,
                                                      design_jian_ding_y=design_jian_ding_y,
                                                      design_zhong_kong_x=design_zhong_kong_x,
                                                      design_zhong_kong_y=design_zhong_kong_y,
                                                      kai_kong_pou_x=kai_kong_pou_x, kai_kong_pou_y=kai_kong_pou_y,
                                                      hole_number_id=holeDesign.id)
                    my_record1.save()
                tunnel_name = row.tunnel.tunnel_name
                row_id = row.id
                #设计孔评价，如果孔不合理，当前孔不允许施工
                isRight = hole_design_estimate(tunnel_name, row_id, holeNum)
                if isRight:
                    holeNum = get_numbers(holeNum)[1]
                    newHoleNumber = None
                    if holeNum %2 == 0:
                        #如果当前孔是偶数孔，向右设计偶数孔
                        newHoleNumber = design_even_hole(tunnel_name, row_id, holeNum)
                    else:
                        #如果当前孔是奇数孔，向右设计奇数孔
                        newHoleNumber = design_odd_hole(tunnel_name, row_id, holeNum)
                    if newHoleNumber is not None:
                        holeDesign.currentHoleFlag = "1"
                        holeDesign.save()
                        message = {"code": 1, "msg": '孔号'+ str(holeNum) + "为不合格孔" + ",请重新提交新孔"+ str(newHoleNumber) +"打孔信息！" }
                elif holeDesign:
                    holeDesign.status = "0"
                    holeDesign.save()
                    message = {"code": 0, "msg": '申请成功!'}
    return JsonResponse(message)


# 钻孔设计参数界面表格根据查询条件重载
@xframe_options_exempt
@csrf_exempt
def reloadDrillingDesignParams(request):
    page = request.GET.get('page')
    page_limit = request.GET.get('limit')
    hole_data = []
    message = None
    try:
        kong_num = request.GET.get('kong_num')
        rowId = request.GET.get('rowId')
        # row = Row.objects.filter(id=rowId).first()
        hole_design_datas = None
        if kong_num and rowId:
            hole_design_datas = Hole_Design.objects.filter(row_id = rowId, hole_number=kong_num)
        elif rowId:
            hole_design_datas = Hole_Design.objects.filter(row_id = rowId)
        hole_list = []
        if hole_design_datas:
            for item in hole_design_datas:
                hole_list.append(model_to_dict(item))
            paginator = Paginator(hole_list, page_limit)
            # 前端传来页数的数据
            data = paginator.page(page)
            for i in range(len(data)):
                status = hole_list[i]['status']
                desc = statusChoice[status]
                status = int(status)
                hole_data.append({"id": hole_list[i]['id'], "pai_num": rowId, "kong_num": hole_list[i]['hole_number'],
                              "pian_angle": getRound2(hole_list[i]['deflection_angle']),
                              "yang_angle": getRound2(hole_list[i]['design_elevation_angel']),
                              "kong_length": getRound2(hole_list[i]['hole_depth']),
                              "yan_kong_length": getRound2(hole_list[i]['rock_section']),
                              "mei_duan_length": getRound2(hole_list[i]['coal_section']),
                              "wash_coal": hole_list[i]['weight_of_flush_coal'],
                              "see_ding_tip": "预计%d米见岩，请缓慢钻进并注意见顶辨识" % (hole_list[i]['see_ceil'] - 1),
                              "see_mei_tip": "预计%d米见煤，请缓慢钻进并注意见煤辨识" % (
                                  0 if hole_list[i]['rock_section'] is None else hole_list[i]['rock_section'] - 1),
                              "status": status,
                              "desc": desc + "" if hole_list[i]["reason"] is None else "," + hole_list[i]["reason"]})
            message = message_data(0, "", len(hole_list), hole_data)
        else:
            message = message_data(0, "", 0, [])
    except Exception as e:
        logging.log("查询结果异常" + e)
        message = message_data(1, "", 0, [])
    finally:
        return JsonResponse(message)
# ----------------------------------钻孔施工填报-----------------------------------------
# 跳转到钻孔施工数据列表
@xframe_options_exempt
@csrf_exempt
def goto_drill_construct_list_page(request):
    # 先定义一个result
    result = {}
    # work_face_obj = Work_face.objects.values_list("w_name")
    user = user_group.objects.filter(username=request.session.get("username")).first()
    if user is not None:
        belongMine = user.belongMine
        work_face = Work_face.objects.filter(mine=belongMine)
        if work_face is not None:
            work_face_obj = work_face.values_list("id", "w_name")
            result['work_face'] = work_face_obj
    return render(request, "Worker/construct_list_page.html", result)


# 给钻孔施工数据列表刷新数据
@xframe_options_exempt
@csrf_exempt
def construct_list_data(request):
    try:
        page = request.GET.get('page')
        page_limit = request.GET.get('limit')
        kong_num = request.GET.get('kong_num')
        rowId = request.GET.get('rowId')
        row = Row.objects.filter(id=rowId).first()
        if kong_num:
            holeConstructionDatas = Hole_Construction.objects.filter(row=row, h_c_number=kong_num)
        else:
            holeConstructionDatas = Hole_Construction.objects.filter(row=row)
        hole_list = []
        for item in holeConstructionDatas:
            holeDesign = Hole_Design.objects.get(hole_number = item.h_c_number)
            time = item.time
            remove_drill_start = item.remove_drill_start
            remove_drill_end = item.remove_drill_end
            deflection_angle = holeDesign.deflection_angle #钻孔设计偏角
            design_elevation_angel = holeDesign.design_elevation_angel #钻孔设计仰角
            rock_section = holeDesign.rock_section #钻孔见煤位置
            hole_depth = holeDesign.hole_depth #设计孔深
            timeStr = time.strftime("%Y-%m-%d %H:%M:%S")
            remove_drill_startStr = remove_drill_start.strftime("%Y-%m-%d %H:%M:%S")
            remove_drill_endStr = remove_drill_end.strftime("%Y-%m-%d %H:%M:%S")
            holeJson = model_to_dict(item)
            holeJson["time"] = timeStr
            holeJson["remove_drill_start"] = remove_drill_startStr
            holeJson["remove_drill_end"] = remove_drill_endStr
            holeJson["deflection_angle"] = deflection_angle
            holeJson["design_elevation_angel"] = design_elevation_angel
            holeJson["rock_section"] = rock_section
            holeJson["hole_depth"] = hole_depth
            holeJson["pass_coal_seam"] = str(float(item.hole_height) - float(item.con_see_coal))
            holeJson["row"] = row.row_id
            holeJson["desc"] = holeJson["desc"] + ("" if holeJson["reason"] is None else ("," + holeJson["reason"]))
            hole_list.append(holeJson)
        paginator = Paginator(hole_list, page_limit)
        # 前端传来页数的数据
        data = paginator.page(page)
        message = message_data(0, "", len(hole_list), hole_list)
    except Exception as e:
        logging.log("查询结果异常" + e)
        message = message_data(1, "", 0)
    finally:
        return JsonResponse(message)



# 跳转到钻孔施工数据列表
@xframe_options_exempt
@csrf_exempt
def goto_drill_construct_layer_page(request):
    result = {}
    # work_face_obj = Work_face.objects.values_list("w_name")
    user = user_group.objects.filter(username=request.session.get("username")).first()
    if user is not None:
        belongMine = user.belongMine
        work_face = Work_face.objects.filter(mine=belongMine)
        if work_face is not None:
            work_face_obj = work_face.values_list("id", "w_name")
            result['work_face'] = work_face_obj
            # result['user'] = user.val
    return render(request, "Worker/construct_submit_layer.html", result)
# ----------------------------------冲孔填报-----------------------------------------
# 跳转到冲孔列表
@xframe_options_exempt
@csrf_exempt
def goto_flush_drill_list_page(request):
    # 先定义一个result
    result = {}
    # work_face_obj = Work_face.objects.values_list("w_name")
    user = user_group.objects.filter(username=request.session.get("username")).first()
    if user is not None:
        belongMine = user.belongMine
        work_face = Work_face.objects.filter(mine=belongMine)
        if work_face is not None:
            work_face_obj = work_face.values_list("id", "w_name")
            result['work_face'] = work_face_obj
    return render(request, "Worker/flush_drill_list_page.html", result)


# 冲孔数据列表刷新
@xframe_options_exempt
@csrf_exempt
def goto_flush_drill_list_data(request):
    page = request.GET.get('page')
    page_limit = request.GET.get('limit')
    kong_num = request.GET.get('kong_num')
    rowId = request.GET.get('rowId')
    row = Row.objects.filter(id=rowId).first()
    if kong_num:
        washCoalConstructions = Wash_Coal_Construction.objects.filter(row=row, h_c_number=kong_num, status = "1")
    else:
        washCoalConstructions = Wash_Coal_Construction.objects.filter(row=row)
    hole_list = []
    for item in washCoalConstructions:
        time = item.time.strftime("%Y-%m-%d %H:%M:%S")
        water_start_time = item.water_start_time.strftime("%Y-%m-%d %H:%M:%S")
        water_end_time = item.water_end_time.strftime("%Y-%m-%d %H:%M:%S")
        coal_rush_quantity_length = item.coal_rush_quantity_length
        coal_rush_quantity_wide = item.coal_rush_quantity_wide
        coal_rush_quantity_height = item.coal_rush_quantity_height
        holeJson = model_to_dict(item)
        holeJson["flush_volume"] = str(coal_rush_quantity_length * coal_rush_quantity_wide * coal_rush_quantity_height)
        holeJson["row"] = row.row_id
        holeJson["time"] = time
        holeJson["water_start_time"] = water_start_time
        holeJson["water_end_time"] = water_end_time
        holeJson["desc"] = holeJson["desc"] + ("" if holeJson["reason"] is None else ("," + holeJson["reason"]))
        hole_list.append(holeJson)
    paginator = Paginator(hole_list, page_limit)
    # 前端传来页数的数据
    data = paginator.page(page)
    message = message_data(0, "", len(hole_list), hole_list)
    return JsonResponse(message)


# 冲孔数据填报表单
@xframe_options_exempt
@csrf_exempt
def goto_flush_drill_layer_page(request):
    result = {}
    # work_face_obj = Work_face.objects.values_list("w_name")
    user = user_group.objects.filter(username=request.session.get("username")).first()
    if user is not None:
        belongMine = user.belongMine
        work_face = Work_face.objects.filter(mine=belongMine)
        if work_face is not None:
            work_face_obj = work_face.values_list("id", "w_name")
            result['work_face'] = work_face_obj
    return render(request, "Worker/flush_drill_submit_layer.html", result)


# ----------------------------------封孔填报-----------------------------------------
# 跳转到封孔列表
@xframe_options_exempt
@csrf_exempt
def goto_feng_drill_list_page(request):
    result = {}
    # work_face_obj = Work_face.objects.values_list("w_name")
    user = user_group.objects.filter(username=request.session.get("username")).first()
    if user is not None:
        belongMine = user.belongMine
        work_face = Work_face.objects.filter(mine=belongMine)
        if work_face is not None:
            work_face_obj = work_face.values_list("id", "w_name")
            result['work_face'] = work_face_obj
    return render(request, "Worker/feng_drill_list_page.html", result)


# 封孔数据列表刷新
@xframe_options_exempt
@csrf_exempt
def goto_feng_drill_list_data(request):
    page = request.GET.get('page')
    page_limit = request.GET.get('limit')
    kong_num = request.GET.get('kong_num')
    rowId = request.GET.get('rowId')
    row = Row.objects.filter(id=rowId).first()
    if kong_num:
        zhuJiangConstructions = zhu_jiang_Construction.objects.filter(row=row, h_c_number=kong_num)
    else:
        zhuJiangConstructions = zhu_jiang_Construction.objects.filter(row=row)
    hole_list = []
    for item in zhuJiangConstructions:
        feng_time = item.feng_time.strftime("%Y-%m-%d %H:%M:%S")
        holeJson = model_to_dict(item)
        holeJson["row"] = row.row_id
        holeJson["feng_time"] = feng_time
        holeJson["desc"] = holeJson["desc"] + ("" if holeJson["reason"] is None else ("," + holeJson["reason"]))
        hole_list.append(holeJson)
    paginator = Paginator(hole_list, page_limit)
    # 前端传来页数的数据
    data = paginator.page(page)
    message = message_data(0, "", len(hole_list), hole_list)
    return JsonResponse(message)


# 封孔数据填报表单
@xframe_options_exempt
@csrf_exempt
def goto_feng_drill_layer_page(request):
    result = {}
    # work_face_obj = Work_face.objects.values_list("w_name")
    user = user_group.objects.filter(username=request.session.get("username")).first()
    if user is not None:
        belongMine = user.belongMine
        work_face = Work_face.objects.filter(mine=belongMine)
        if work_face is not None:
            work_face_obj = work_face.values_list("id", "w_name")
            result['work_face'] = work_face_obj
    return render(request, "Worker/feng_drill_submit_layer.html", result)


def getRound2(value):
    if value is None:
        return ""
    else:
        return round(value, 2)


# 根据工作面id获取巷道信息，用于下拉框动态显示
@csrf_exempt
def getTunnelByWorkface(request):
    data = {}
    try:
        workfaceId = request.POST["work_face"]
        if not workfaceId:
            return data
        else:
            logging.INFO = "根据workfaceId" + workfaceId + "得到巷道信息"
            workfaces = Work_face.objects.filter(id=workfaceId)
            if workfaces is not None:
                workface = workfaces.first()
                tunnels = Tunnel.objects.filter(work_face=workface)
                if tunnels is not None:
                    data = serializers.serialize('json', tunnels)
    except Exception as e:
        logging.INFO = "获取巷道信息异常" + e
    finally:
        print(type(data))
        res = {"data": data}
        return JsonResponse(res)


# 根据巷道id获取排号信息，用于下拉框动态显示
@csrf_exempt
def getRowByTunnel(request):
    data = {}
    try:
        tunnelId = request.POST["tunnel"]
        if not tunnelId:
            return data
        else:
            logging.INFO = "tunnelId" + str(tunnelId) + "得到排号信息"
            rows = Row.objects.filter(tunnel_id=tunnelId)
            if rows is not None:
                data = serializers.serialize('json', rows)
    except Exception as e:
        logging.INFO = "获取排号信息异常" + e
    finally:
        print(type(data))
        res = {"data": data}
        return JsonResponse(res)

# 根据排号获取冲孔界面的孔号信息，用于下拉框动态显示
@csrf_exempt
def getFlushHoleByRow(request):
    data = {}
    try:
        rowId = request.POST["row"]
        if not rowId:
            return data
        else:
            logging.INFO = "rowId" + rowId + "得到孔号信息"
            rows = Row.objects.filter(id = rowId)
            if rows is None:
                return data
            row = rows.first()
            holeConstructions = Hole_Construction.objects.filter(row_id = row.id, status = "1")
            if holeConstructions is not None:
                data = serializers.serialize('json', holeConstructions)
    except Exception as e:
        logging.INFO = "获取孔号信息异常" + e
    finally:
        print(type(data))
        res = {"data": data}
        return JsonResponse(res)

# 根据排号获取封界面的孔号信息，用于下拉框动态显示
@csrf_exempt
def getFengHoleByRow(request):
    data = {}
    try:
        rowId = request.POST["row"]
        if not rowId:
            return data
        else:
            logging.INFO = "rowId" + rowId + "得到孔号信息"
            rows = Row.objects.filter(id = rowId)
            if rows is None:
                return data
            row = rows.first()
            washCoalConstructions = Wash_Coal_Construction.objects.filter(row_id = row.id, status = "1")
            if washCoalConstructions is not None:
                data = serializers.serialize('json', washCoalConstructions)
    except Exception as e:
        logging.INFO = "获取孔号信息异常" + e
    finally:
        print(type(data))
        res = {"data": data}
        return JsonResponse(res)
# 根据排号获取当前设计孔信息，用与钻孔设计参数界面渲染显示
@csrf_exempt
def getHoleDesignData(request):
    data = {}
    data["code"] = 1
    try:
        rowId = request.POST["row"]
        if rowId:
            logging.INFO = "rowId" + rowId + "得到排号信息"
            rows = Row.objects.filter(id=rowId)
            if rows:
                row = rows.first()
                holeDesigns = Hole_Design.objects.filter(row=row, currentHoleFlag="0", status = "0")
                if holeDesigns:
                    holeDesign = holeDesigns.first()
                    data["hole_number"] = holeDesign.hole_number
                    data["deflection_angle"] = holeDesign.deflection_angle
                    data["design_elevation_angel"] = holeDesign.design_elevation_angel
                    data["hole_depth"] = holeDesign.hole_depth
                    data["rock_section"] = holeDesign.rock_section
                    data["coal_section"] = holeDesign.coal_section
                    data["weight_of_flush_coal"] = holeDesign.weight_of_flush_coal
                    data["see_ceil"] = holeDesign.see_ceil
                    data["code"] = 0
    except:
        logging.INFO = "获取设计孔信息异常"
    finally:
        return JsonResponse(data)


# 根据排号获取当前施工孔信息，用与施工参数界面渲染显示
@csrf_exempt
def getHoleConstructionData(request):
    data = {}
    data["code"] = 1
    try:
        rowId = request.POST["row"]
        if rowId:
            logging.INFO = "rowId" + rowId + "得到排号信息"
            rows = Row.objects.filter(id=rowId)
            if rows:
                row = rows.first()
                holeDesigns = Hole_Design.objects.filter(row=row, currentHoleFlag="0", status = "1")
                if holeDesigns:
                    holeDesign = holeDesigns.first()
                    data["hole_number"] = holeDesign.hole_number   #孔号
                    data["deflection_angle"] = holeDesign.deflection_angle  # 设计偏角
                    data["design_elevation_angel"] = holeDesign.design_elevation_angel #设计仰角
                    data["hole_depth"] = holeDesign.hole_depth #设计孔深
                    data["rock_section"] = holeDesign.rock_section #设计岩段 = 设计见煤
                    data["coal_section"] = holeDesign.coal_section #设计煤段
                    data["weight_of_flush_coal"] = holeDesign.weight_of_flush_coal #设计冲煤量
                    data["see_ceil"] = holeDesign.see_ceil #设计见顶
                    data["code"] = 0
    except:
        logging.INFO = "获取施工孔信息异常"
    finally:
        return JsonResponse(data)


#钻孔施工界面评价
@csrf_exempt
def getZuanKongQualityData(request):  # 钻孔施工质量评价 见止煤误差(单孔评价)
    res = {}
    res["code"] = 1
    try:
        data = request.POST['data']
        json_data = json.loads(data)
        tunnel_name, row_id, hole_number, actual_location, actual_kong_length,pass_mei,r_elevation_angle= json_data['tunnel_name'],json_data['row_id'], json_data['hole_number'],json_data["actual_location"],json_data["actual_kong_length"],json_data["pass_mei"],json_data["check_angle"]
        number = get_numbers(hole_number)[1]  # 当前钻孔数字
        tunnel_Data = get_tunnel_datas(tunnel_name)
        mei_ceng_qing_jiao =float(tunnel_Data['mei_ceng_qing_jiao'])
        tunnel_first_hole_number = tunnel_Data['tunnel_first_hole_number']  # 这一排的首孔号
        first_number = get_numbers(tunnel_first_hole_number)[1]
        first_hole_design_Data = get_hole_design_datas(tunnel_name, row_id, first_number)
        first_coal_section = float(first_hole_design_Data['coal_section'])  # 首孔设计煤段
        first_hole_Construction_con_see_coal = float(actual_location)  # 首孔施工见煤
        first_hole_Construction_con_see_ceil = float(actual_kong_length) - float(pass_mei) # 首孔施工见顶
        Row_Data = get_row_data(tunnel_name, row_id)
        id = Row_Data.id
        hole_design_Data = get_hole_design_datas(tunnel_name, row_id, hole_number)
        mei_duan_length = float(actual_kong_length) - float(pass_mei) - float(actual_location)  # 煤段长度
        # 判断当前孔在首孔哪一侧
        if number > first_number:
            s = 1
        else:
            s = -1

        if abs(float(actual_location) - hole_design_Data['rock_section']) <= 5 and \
                abs(first_hole_Construction_con_see_ceil - hole_design_Data['see_ceil']) <= 5:
            res["msg"] = "见煤合格" + ";见顶合格"
        elif abs(float(actual_location) - hole_design_Data['rock_section']) > 5 and \
                abs(first_hole_Construction_con_see_ceil - hole_design_Data['see_ceil']) > 5:
            # 煤段倾角
            judgment = abs(math.asin((first_hole_Construction_con_see_coal - first_hole_Construction_con_see_ceil +
                                      first_coal_section) * math.cos(math.radians(mei_ceng_qing_jiao)) / 2 / (
                                         mei_duan_length)) * 180 / math.pi) - mei_ceng_qing_jiao * s
            # 岩段倾角
            judgment1 = first_hole_Construction_con_see_ceil * math.cos((judgment) / 180 * math.pi) + \
                        first_hole_Construction_con_see_ceil * math.sin((judgment) / 180 * math.pi) * \
                        math.sin((90 - judgment + s * mei_ceng_qing_jiao) / 180 * math.pi)

            if abs(judgment - float(r_elevation_angle)) > 1:
                if abs(judgment1 - first_hole_Construction_con_see_ceil) >= 3:
                    res["msg"] = "钻孔偏斜" + ";钻孔偏斜"
                else:
                    res["msg"] = "施工倾角误差大，为：" + str(judgment) + "°" + ";施工倾角误差大, 为:" + str(judgment) +'°'
            else:
                res["msg"] = "有断层" + ";有断层"
        else:
            res["msg"] = "有断层" + ";有断层"
        res["code"] = 0
    except Exception as e:
        res["msg"] = "评价内部接口异常"
    finally:
        return JsonResponse(res)

#施工参数填报，立即提交，保存评价结果和施工信息
@csrf_exempt
def submitHoleConstruction(request):
    res = {}
    res["code"] = 1
    try:
        jsonData = request.POST
        if jsonData:
            kong_num = jsonData['kong_num']    #孔号
            drill_eval = jsonData['assess_kong']    #评价结果
            row = jsonData['row']               #排id
            tunnel_num = jsonData['tunnel']     #巷道
            tunnel_name = Tunnel.objects.filter(id = tunnel_num).first().tunnel_name
            assess_kongList = drill_eval.split(";")
            see_coal_eval = assess_kongList[0]
            see_ceil_eval = assess_kongList[1]
            hole_height = None
            hole_Design = Hole_Design.objects.filter(hole_number = kong_num, row_id = row).first()
            #保存评价结果
            holeEval = Hole_Eval(see_coal_eval=see_coal_eval, see_ceil_eval=see_ceil_eval, h_name=kong_num, row_id=row)
            if "见煤合格" == see_coal_eval and "见顶合格" == see_ceil_eval:
                #设计下一个孔  控制范围评价
                if hole_Design:
                    hole_number = hole_Design.hole_number
                    tunnel_name = hole_Design.row.tunnel.tunnel_name
                    row_id = hole_Design.row.row_id
                    hole_height = hole_Design.design_hole_height
                    newHoleNum = None
                    if get_numbers(hole_number)[1]%2 == 0 :
                        #设计偶数孔
                        newHoleNum = design_even_hole(tunnel_name,row_id,hole_number)
                    else:
                        #设计奇数孔
                        newHoleNum =design_odd_hole(tunnel_name,row_id,hole_number)
                    logging.INFO("设计新孔孔号为" + newHoleNum)
            else:
                # 保存施工信息
                time = jsonData['time']  # 施工日期
                r_deflection_angle = jsonData['check_direction']  # 钻孔复核偏角
                r_elevation_angle = jsonData['check_angle']  # 钻孔复核倾角
                con_see_coal = jsonData['actual_location']  # 实际见煤位置
                con_hole_depth = jsonData['actual_kong_length']  # 实际孔深
                pass_mei = jsonData['pass_mei']  # 过煤钻岩
                con_see_ceil = str(float(con_hole_depth) - float(pass_mei))
                drill_depth = jsonData['pass_length']  # 当班钻进深度
                construction_person_name = jsonData['work_person']
                text_person = jsonData['check_person']
                ab_situation = jsonData['kong_error_msg']  # 孔内瓦斯异常情况
                ab_hole_depth_position = None
                if "无" != ab_situation:
                    ab_hole_depth_position = ab_situation[-8:-5]
                holeConstruction = Hole_Construction(h_c_number=kong_num, row_id=row, hole_height=hole_height,
                                                     time=time, r_deflection_angle=r_deflection_angle,
                                                     r_elevation_angle=r_elevation_angle, con_see_coal=con_see_coal,
                                                     con_see_ceil=con_see_ceil, drill_depth=drill_depth,
                                                     drill_eval=drill_eval, ab_situation=ab_situation,
                                                     ab_hole_depth_position=ab_hole_depth_position,
                                                     construction_person_name=construction_person_name,
                                                     text_person=text_person)

                holeConstruction.save()
                #评价结果不合格则补孔
                design_repair_hole(tunnel_name, row, kong_num)
            hole_Design.currentHoleFlag = "1"
            hole_Design.save()
            holeEval.save()
            res["code"] = 1
            res["msg"] = "保存成功"
    except Exception as e:
        logging.INFO  = "保存施工参数异常" + e
        res["msg"] ="保存施工参数异常" + e
    finally:
        return JsonResponse(res)

#冲孔参数填报，立即提交，冲孔参数信息
@csrf_exempt
def submitWashCoalConstruction(request):
    res = {}
    res["code"] = 1
    msg = ""
    try:
        jsonData = request.POST
        if jsonData:
            kong_num = jsonData["kong_num"]
            row_id = jsonData["kong_num"]
            holeConstructions = Wash_Coal_Construction.objects.filter(h_c_number = kong_num, status = "1")
            washCoalConstructions = Wash_Coal_Construction.objects.filter(row_id = row_id,h_c_number = kong_num, status = "4")
            con_see_coal = None
            con_see_ceil = None
            if holeConstructions:
                holeConstruction = holeConstructions.first()
                con_see_coal = holeConstruction.con_see_coal
                con_see_ceil = holeConstruction.con_see_ceil
            h_c_number = kong_num
            row_id = jsonData["row"]
            chong_drill_eval = jsonData["assess_flush_kong"]
            coal_rush_quantity_length = jsonData["flush_mei_count_lenth"]
            coal_rush_quantity_wide = jsonData["flush_mei_count_wide"]
            coal_rush_quantity_height = jsonData["flush_mei_count_heigth"]
            construction_person_name = jsonData["work_person"]
            text_person = jsonData["check_person"]
            water_start_time = jsonData["flush_start_time"]
            water_end_time = jsonData["flush_end_time"]
            if washCoalConstructions:
                washCoalConstruction = washCoalConstructions.first()
                washCoalConstruction.con_see_coal = con_see_coal
                washCoalConstruction.con_see_ceil= con_see_ceil
                washCoalConstruction.chong_drill_eval =chong_drill_eval
                washCoalConstruction.construction_person_name = construction_person_name
                washCoalConstruction.text_person = text_person
                washCoalConstruction.water_start_time = water_start_time
                washCoalConstruction.water_end_time = water_end_time
                washCoalConstruction.coal_rush_quantity_length=coal_rush_quantity_length
                washCoalConstruction.coal_rush_quantity_wide=coal_rush_quantity_wide
                washCoalConstruction.coal_rush_quantity_height=coal_rush_quantity_height
                washCoalConstruction.save()
                res["code"] = 0
                msg = "保存成功"
            else:
                res["code"] = 1
                msg = "冲孔申请成功记录为空"
    except Exception as e:
        msg = "保存冲孔参数异常"
    finally:
        res["msg"] = msg
        return JsonResponse(res)


#封孔参数填报，立即提交，冲孔参数信息
@csrf_exempt
def submitFengCoalConstruction(request):
    res = {}
    res["code"] = 1
    msg = ""
    try:
        jsonData = request.POST
        if jsonData:
            kong_num = jsonData["kong_num"]
            row_id = jsonData["row"]
            zhuJiangConstructions = zhu_jiang_Construction.objects.filter(row_id= row_id, h_c_number = kong_num, status = "4")
            if zhuJiangConstructions:
                zhuJiangConstruction = zhuJiangConstructions.first()
                zhu_drill_eval = jsonData["assess_feng_kong"]
                screening_length = jsonData["shai_guan_length"]
                grouting_pressure = jsonData["zhu_jiang_pressure"]
                grouting_amount = jsonData["zhu_jiang_count"]
                # start_hole_depth = jsonData[""]   #开始封孔孔深
                # end_hole_depth = jsonData[""]     #结束封孔孔深
                construction_person_name = jsonData["work_person"]
                text_person = jsonData["check_person"]
                feng_time = jsonData["feng_date"]
                h_c_number = kong_num
                zhuJiangConstruction.zhu_drill_eval= zhu_drill_eval,
                zhuJiangConstruction.screening_length = screening_length,
                zhuJiangConstruction.grouting_pressure= grouting_pressure,
                zhuJiangConstruction.grouting_amount =grouting_amount,
                # zhuJiangConstruction.start_hole_depth = start_hole_depth,
                # zhuJiangConstruction.end_hole_depth = end_hole_depth,
                zhuJiangConstruction.construction_person_name = construction_person_name,
                zhuJiangConstruction.text_person =text_person,
                zhuJiangConstruction.feng_time = feng_time
                zhuJiangConstruction.save()
                res["code"] = 0
                msg = "保存成功"
            else:
                msg = "封孔申请记录为空"
    except Exception as e:
        # logging.INFO = "保存冲孔参数异常" + e
        msg = "保存封孔参数异常"
    finally:
        res["msg"] = msg
        return JsonResponse(res)
# 角度转弧度函数
def math_function_transform(value):
    transform_value = ((value / 180) * math.pi)
    return transform_value

@csrf_exempt
def getMeiDuanLength(request):
    jsonData = request.POST
    res = {}
    res["code"] = 1
    try:
        if jsonData:
            row = jsonData["row"]
            hole_num = jsonData["hole_num"]
            if row and hole_num:
                holeConstructions = Hole_Construction.objects.filter(row_id =row, h_c_number = hole_num)
                if holeConstructions:
                    holeConstruction = holeConstructions.first()
                    meiduanLength = holeConstruction.con_see_ceil - holeConstruction.con_see_coal
                    res["mes"] = meiduanLength
                    res["code"] = 0
    except:
        logging.INFO("获取煤段长度异常")
    finally:
        return JsonResponse(res)

@csrf_exempt
def resubmitHoleDesign(request):
    data = request.POST
    res = {}
    res["code"] = "1"
    try:
        id = data["id"]
        holeDesigns = Hole_Design.objects.filter(id = id)
        if holeDesigns:
            holeDesign = holeDesigns.first()
            Hole_Designs = Hole_Design.objects.filter(row_id = holeDesign.row_id, currentHoleFlag = "0")
            Hole_Designs = Hole_Designs.filter(~Q(id = id))
            if Hole_Designs.count == 0:
                holeDesign.status = "1"
                holeDesign.currentHoleFlag = "0"
                holeDesign.desc = statusChoice[holeDesign.status]
                holeDesign.save()
                res["code"] = "0"
                res["msg"] = "提交成功"
            else:
                res["msg"] = "孔号" + holeDesign.hole_number +"非当前孔,不能进行重新申请"
        else:
            res["msg"] = "查询记录为空"

    except Exception as e:
        res["msg"] = "接口异常" + e
    finally:
        return JsonResponse(res)

#冲孔申请界面
@csrf_exempt
def flush_apply_index(request):
    result = {}
    user = user_group.objects.filter(username=request.session.get("username")).first()
    if user is not None:
        belongMine = user.belongMine
        work_face = Work_face.objects.filter(mine=belongMine)
        if work_face is not None:
            work_face_obj = work_face.values_list("id", "w_name")
            result['work_face'] = work_face_obj
    return render(request, "Worker/flush_apply_index.html", result)

#封孔申请界面
@csrf_exempt
def feng_apply_index(request):
    result = {}
    user = user_group.objects.filter(username=request.session.get("username")).first()
    if user is not None:
        belongMine = user.belongMine
        work_face = Work_face.objects.filter(mine=belongMine)
        if work_face is not None:
            work_face_obj = work_face.values_list("id", "w_name")
            result['work_face'] = work_face_obj
    return render(request, "Worker/feng_apply_index.html", result)

#冲孔申请提交
@csrf_exempt
def submitFlushData(request):
    data = request.POST
    res = {}
    res["code"] = 1
    try:
        if data:
            row_id = data["row"]
            h_c_number = data["kong_num"]
            holeConstruction = Hole_Construction.objects.filter(row_id = row_id, h_c_number = h_c_number, status = '2')
            if holeConstruction:
                washCoalConstructions = Wash_Coal_Construction.objects.filter(h_c_number=h_c_number)
                if washCoalConstructions is not None:
                    res["msg"] = "已经存在冲煤申请记录"
                else:
                    washCoalConstruction = Wash_Coal_Construction(row_id=row_id, h_c_number=h_c_number)
                    washCoalConstruction.save()
                    res["code"] = 0
                    res["msg"] = "申请成功"
            else:
                res["msg"] = "当前孔施工确认未通过"
        else:
            res["msg"] = "提交数据为空"
    except Exception as e:
        res["msg"] = "接口异常" + e
    finally:
        return JsonResponse(res)
#封孔申请提交
@csrf_exempt
def submitFengData(request):
    data = request.POST
    res = {}
    res["code"] = 1
    try:
        if data:
            row_id = data["row"]
            h_c_number = data["kong_num"]
            washCoalConstruction = Wash_Coal_Construction.objects.filter(row_id = row_id, h_c_number = h_c_number, status = '2')
            if washCoalConstruction:
                zhuJiangConstructions = zhu_jiang_Construction.objects.filter(h_c_number= h_c_number)
                if zhuJiangConstructions is not None:
                    res["msg"] = "已经存在冲煤申请记录"
                else:
                    zhuJiangConstruction = zhu_jiang_Construction(row_id=row_id, h_c_number=h_c_number)
                    zhuJiangConstruction.save()
                    res["code"] = 0
                    res["msg"] = "申请成功"
            else:
                res["msg"] = "当前孔冲孔确认未通过"
        else:
            res["msg"] = "提交数据为空"
    except Exception as e:
        res["msg"] = "接口异常" + e
    finally:
        return JsonResponse(res)



