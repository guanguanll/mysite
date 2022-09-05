import datetime
import json
import random

from django.core import serializers
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from Mining.tool_views import message_data
from django.forms.models import model_to_dict

from util.enum import statusChoice
from .models import *


def operator_login_index(request):
    userName = request.session.get("username")
    return render(request, 'Operator/operator_index.html', locals())


@xframe_options_exempt
@csrf_exempt
# 操作员核查钻孔视频验收监控记录列表
def check_videos_record_list(request):
    result = {}
    user = user_group.objects.filter(username=request.session.get("username")).first()
    if user is not None:
        belongMine = user.belongMine
        work_face = Work_face.objects.filter(mine=belongMine)
        if work_face is not None:
            work_face_obj = work_face.values_list("id", "w_name")
            result['work_face'] = work_face_obj
    return render(request, 'Operator/videos_check_list_page.html', result)


@xframe_options_exempt
@csrf_exempt
# 操作员核查钻孔视频验收监控记录list渲染
def check_videos_record_rendering(request):
    data = request.GET
    dataLists = []
    if data:
        rowId = data["rowId"]
        h_c_number = data["kong_num"]
        holeConstructions = None
        washCoalConstructions = None
        zhuJiangConstructions = None
        dataLists = []
        if rowId and h_c_number:
            holeConstructions = Hole_Construction.objects.filter(row_id=rowId, h_c_number=h_c_number)
            washCoalConstructions = Wash_Coal_Construction.objects.filter(row_id=rowId, h_c_number=h_c_number)
            zhuJiangConstructions = zhu_jiang_Construction.objects.filter(row_id=rowId, h_c_number=h_c_number)
            if holeConstructions and washCoalConstructions and zhuJiangConstructions:
                holeConstruction = holeConstructions.first()
                washCoalConstruction = washCoalConstructions.first()
                zhuJiangConstruction = zhuJiangConstructions.first()
                end_hole_depth = 0 if not zhuJiangConstruction.end_hole_depth else float(
                    zhuJiangConstruction.end_hole_depth)
                start_hole_depth = 0 if not zhuJiangConstruction.start_hole_depth else float(
                    zhuJiangConstruction.start_hole_depth)
                dataDict = {'kong_num': h_c_number,
                            'pian_angle': holeConstruction.r_deflection_angle,
                            'hole_height': holeConstruction.hole_height,
                            'qing_angle': holeConstruction.r_elevation_angle,
                            'start_zuan_time': holeConstruction.time,
                            'flush_start_t': washCoalConstruction.water_start_time,
                            'flush_end_t': washCoalConstruction.water_end_time,
                            'mei_count': washCoalConstruction.actual_flush_mei,
                            'return_start_t': holeConstruction.remove_drill_start,
                            'return_end_t': holeConstruction.remove_drill_end,
                            'kong_depth': holeConstruction.con_hole_depth,
                            'worker_name': holeConstruction.construction_person_name,
                            'feng_start_t': zhuJiangConstruction.feng_time,
                            'feng_end_t': "",  # 没值
                            'feng_kong_len': abs(round(end_hole_depth - start_hole_depth, 2)),
                            'shai_guan_len': zhuJiangConstruction.screening_length,
                            'video_num': zhuJiangConstruction.video_number,
                            'error_msg': zhuJiangConstruction.grouting_abnormal_situation,
                            'video_people': '',  # 没值
                            'submit_time': zhuJiangConstruction.feng_time,
                            'class_times': ''}
                dataLists.append(dataDict)
        elif rowId:
            holeConstructions = Hole_Construction.objects.filter(row_id=rowId)
            washCoalConstructions = Wash_Coal_Construction.objects.filter(row_id=rowId)
            zhuJiangConstructions = zhu_jiang_Construction.objects.filter(row_id=rowId)
            if zhuJiangConstructions:
                for zhuJiangConstruction in zhuJiangConstructions:
                    h_c_number = zhuJiangConstruction.h_c_number
                    holeConstruction = holeConstructions.filter(h_c_number=h_c_number).first()
                    washCoalConstruction = washCoalConstructions.filter(h_c_number=h_c_number).first()
                    end_hole_depth = 0 if not zhuJiangConstruction.end_hole_depth else float(
                        zhuJiangConstruction.end_hole_depth)
                    start_hole_depth = 0 if not zhuJiangConstruction.start_hole_depth else float(
                        zhuJiangConstruction.start_hole_depth)
                    dataDict = {'kong_num': h_c_number,
                                'pian_angle': holeConstruction.r_deflection_angle,
                                'hole_height': holeConstruction.hole_height,
                                'qing_angle': holeConstruction.r_elevation_angle,
                                'start_zuan_time': holeConstruction.time,
                                'flush_start_t': washCoalConstruction.water_start_time,
                                'flush_end_t': washCoalConstruction.water_end_time,
                                'mei_count': washCoalConstruction.actual_flush_mei,
                                'return_start_t': holeConstruction.remove_drill_start,
                                'return_end_t': holeConstruction.remove_drill_end,
                                'kong_depth': holeConstruction.con_hole_depth,
                                'worker_name': holeConstruction.construction_person_name,
                                'feng_start_t': zhuJiangConstruction.feng_time,
                                'feng_end_t': "",  # 没值
                                'feng_kong_len': abs(round(end_hole_depth - start_hole_depth, 2)),
                                'shai_guan_len': zhuJiangConstruction.screening_length,
                                'video_num': zhuJiangConstruction.video_number,
                                'error_msg': zhuJiangConstruction.grouting_abnormal_situation,
                                'video_people': '',  # 没值
                                'submit_time': zhuJiangConstruction.feng_time,
                                'class_times': ''}
                    dataLists.append(dataDict)

    msg = {"code": 0, "data": dataLists}
    return JsonResponse(msg)


@xframe_options_exempt
@csrf_exempt
# 操作员核查钻孔视频监控记录填写
def check_videos_record_fillin(request):
    result = {}
    user = user_group.objects.filter(username=request.session.get("username")).first()
    if user is not None:
        belongMine = user.belongMine
        work_face = Work_face.objects.filter(mine=belongMine)
        if work_face is not None:
            work_face_obj = work_face.values_list("id", "w_name")
            result['work_face'] = work_face_obj
    return render(request, 'Operator/videos_check_submit.html', result)


@xframe_options_exempt
@csrf_exempt
# 操作员核查钻孔视频举牌记录list
def check_videos_holding_record(request):
    return render(request, 'Operator/jupai_required_list.html')


@xframe_options_exempt
@csrf_exempt
# 操作员核查钻孔视频举牌记录list
def check_videos_holding_record_list(request):
    result = {}
    user = user_group.objects.filter(username=request.session.get("username")).first()
    if user is not None:
        belongMine = user.belongMine
        work_face = Work_face.objects.filter(mine=belongMine)
        if work_face is not None:
            work_face_obj = work_face.values_list("id", "w_name")
            result['work_face'] = work_face_obj
    return render(request, 'Operator/jupai_required_list.html', result)


@xframe_options_exempt
@csrf_exempt
# 操作员核查钻孔视频举牌监控记录列表的渲染
def check_videos_holding_record_rendering(request):
    data = request.GET
    try:
        if data:
            rowId = data['rowId']
            h_c_number = data['kong_num']
            shiGongChecks = None
            dataList = []
            if rowId and h_c_number:
                vedioChecks = vedioCheck.objects.filter(row_id=rowId, h_c_number=h_c_number)
            elif rowId:
                vedioChecks = vedioCheck.objects.filter(row_id=rowId)
            if vedioChecks:
                for vedioCheckObj in vedioChecks:
                    dateTimestr = vedioCheckObj.date_time.strftime("%Y-%m-%d %H:%M:%S")
                    isKaiKongShenQingStr = "是" if vedioCheckObj.isKaiKongShenQing == "1" else "否"
                    isKaiKongJuPaiStr = "是" if vedioCheckObj.isKaiKongJuPai == "1" else "否"
                    isJianMeiJuPaiStr = "是" if vedioCheckObj.isJianMeiJuPai == "1" else "否"
                    isJianDingJuPaiStr = "是" if vedioCheckObj.isJianDingJuPai == "1" else "否"
                    isZhongKongJuPaiStr = "是" if vedioCheckObj.isZhongKongJuPai == "1" else "否"
                    isTuiZuanYanShouJuPaiStr = "是" if vedioCheckObj.isTuiZuanYanShouJuPai == "1" else "否"
                    isChongMeiYanShouJuPaiStr = "是" if vedioCheckObj.isChongMeiYanShouJuPai == "1" else "否"
                    isFengKongKaiShiJuPaiStr = "是" if vedioCheckObj.isFengKongKaiShiJuPai == "1" else "否"
                    isFengKongYanShouJuPaiStr = "是" if vedioCheckObj.isFengKongYanShouJuPai == "1" else "否"
                    dataDict = model_to_dict(vedioCheckObj)
                    dataDict["dateTimestr"] = dateTimestr
                    dataDict["isKaiKongShenQingStr"] = isKaiKongShenQingStr
                    dataDict["isKaiKongJuPaiStr"] = isKaiKongJuPaiStr
                    dataDict["isJianMeiJuPaiStr"] = isJianMeiJuPaiStr
                    dataDict["isJianDingJuPaiStr"] = isJianDingJuPaiStr
                    dataDict["isZhongKongJuPaiStr"] = isZhongKongJuPaiStr
                    dataDict["isTuiZuanYanShouJuPaiStr"] = isTuiZuanYanShouJuPaiStr
                    dataDict["isChongMeiYanShouJuPaiStr"] = isChongMeiYanShouJuPaiStr
                    dataDict["isFengKongKaiShiJuPaiStr"] = isFengKongKaiShiJuPaiStr
                    dataDict["isFengKongYanShouJuPaiStr"] = isFengKongYanShouJuPaiStr
                    dataList.append(dataDict)
            msg = {"code": 0, "data": dataList}
        else:
            msg = {"code": 0, "data": []}
    except Exception as e:
        msg = {"code": 0, "data": []}
    finally:
        return JsonResponse(msg)


@xframe_options_exempt
@csrf_exempt
# 核查视频举牌记录的数据填充
def check_videos_holding_record_fillin(request):
    result = {}
    user = user_group.objects.filter(username=request.session.get("username")).first()
    if user is not None:
        belongMine = user.belongMine
        work_face = Work_face.objects.filter(mine=belongMine)
        if work_face is not None:
            work_face_obj = work_face.values_list("id", "w_name")
            result['work_face'] = work_face_obj
    return render(request, "Operator/jupai_required.html", result)


@xframe_options_exempt
@csrf_exempt
# 操作员核查钻孔施工资料记录list
def check_material_record_list(request):
    result = {}
    user = user_group.objects.filter(username=request.session.get("username")).first()
    if user is not None:
        belongMine = user.belongMine
        work_face = Work_face.objects.filter(mine=belongMine)
        if work_face is not None:
            work_face_obj = work_face.values_list("id", "w_name")
            result['work_face'] = work_face_obj
    return render(request, 'Operator/file_check_list_page.html', result)


@xframe_options_exempt
@csrf_exempt
# 操作员核查钻孔施工资料记录list的数据渲染
def check_material_record_rendering(request):
    data = request.GET
    try:
        if data:
            rowId = data['rowId']
            h_c_number = data['kong_num']
            shiGongChecks = None
            dataList = []
            if rowId and h_c_number:
                shiGongChecks = ShiGongCheck.objects.filter(row_id=rowId, h_c_number=h_c_number)
            elif rowId:
                shiGongChecks = ShiGongCheck.objects.filter(row_id=rowId)
            if shiGongChecks:
                for shiGongCheck in shiGongChecks:
                    dateTimestr = shiGongCheck.date_time.strftime("%Y-%m-%d %H:%M:%S")
                    isQiQuanStr = "是" if shiGongCheck.isQiQuan == "1" else "否"
                    isCeXieStr = "是" if shiGongCheck.isCeXie == "1" else "否"
                    dataDict = model_to_dict(shiGongCheck)
                    dataDict["dateTimestr"] = dateTimestr
                    dataDict["isQiQuanStr"] = isQiQuanStr
                    dataDict["isCeXieStr"] = isCeXieStr
                    dataList.append(dataDict)
            msg = {"code": 0, "data": dataList}
        else:
            msg = {"code": 0, "data": []}
    except Exception as e:
        msg = {"code": 0, "data": []}
    finally:
        return JsonResponse(msg)


@xframe_options_exempt
@csrf_exempt
# 操作员核查施工资料记录的数据填充
def check_material_record_fillin(request):
    result = {}
    user = user_group.objects.filter(username=request.session.get("username")).first()
    if user is not None:
        belongMine = user.belongMine
        work_face = Work_face.objects.filter(mine=belongMine)
        if work_face is not None:
            work_face_obj = work_face.values_list("id", "w_name")
            result['work_face'] = work_face_obj
    return render(request, 'Operator/file_check_page.html', result)


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


# @xframe_options_exempt
# @csrf_exempt
# # 跳转到审批记录数据渲染
# def goto_approve_record_rendering(request):
#     apply_record_obj = Apply_Record.objects.order_by("-apply_time").all()
#     apply_record = []
#     for item in apply_record_obj:
#         apply_status_desc = Enums.statusChoice.get(item.apply_status)
#         item.apply_time = item.apply_time.strftime("%Y年%m月%d日")
#         itemDict = model_to_dict(item)
#         itemDict["apply_status_desc"] = apply_status_desc
#         apply_record.append(itemDict)
#     message = message_data(0, "", len(apply_record), apply_record)
#     return JsonResponse(message)


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


# -------------------------------------视频举牌验收-------------------------------
@xframe_options_exempt
@csrf_exempt
# 视屏举牌数据填报验收
def videos_juipai_submit_process(request):
    if request.method == "POST":
        data = request.POST["data"]
        dataDict = json.loads(data)
        row_Id = dataDict["row"]
        h_c_number = dataDict["kong_num"]
        desc = dataDict["desc"]
        person = dataDict["person"]
        isKaiKongShenQing = dataDict["isKaiKongShenQing"]
        isKaiKongJuPai = dataDict["isKaiKongJuPai"]
        isJianMeiJuPai = dataDict["isJianMeiJuPai"]
        isJianDingJuPai = dataDict["isJianDingJuPai"]
        isZhongKongJuPai = dataDict["isZhongKongJuPai"]
        isTuiZuanYanShouJuPai = dataDict["isTuiZuanYanShouJuPai"]
        isChongMeiYanShouJuPai = dataDict["isChongMeiYanShouJuPai"]
        isFengKongKaiShiJuPai = dataDict["isFengKongKaiShiJuPai"]
        isFengKongYanShouJuPai = dataDict["isFengKongYanShouJuPai"]
        date = datetime.datetime.now()
        vedioChecks = vedioCheck.objects.filter(row_id=row_Id, h_c_number=h_c_number)
        if vedioChecks:
            message = {"code": 1, "msg": '当前孔已有验收记录!'}
        else:
            vedioCheckobj = vedioCheck(
                row_id=row_Id,
                h_c_number=h_c_number,
                isKaiKongShenQing=isKaiKongShenQing,
                isKaiKongJuPai=isKaiKongJuPai,
                isJianMeiJuPai=isJianMeiJuPai,
                isJianDingJuPai=isJianDingJuPai,
                isZhongKongJuPai=isZhongKongJuPai,
                isTuiZuanYanShouJuPai=isTuiZuanYanShouJuPai,
                isChongMeiYanShouJuPai=isChongMeiYanShouJuPai,
                isFengKongKaiShiJuPai=isFengKongKaiShiJuPai,
                isFengKongYanShouJuPai=isFengKongYanShouJuPai,
                date_time=date,
                person=person,
                desc=desc
            )
            vedioCheckobj.save()
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
        dataDict = json.loads(data)
        row_Id = dataDict["row"]
        h_c_number = dataDict["kong_num"]
        desc = dataDict["desc"]
        person = dataDict["person"]
        isQiQuan = dataDict["isQiQuan"]
        isCeXie = dataDict["isCeXie"]
        date = datetime.datetime.now()
        shiGongChecks = ShiGongCheck.objects.filter(row_id=row_Id, h_c_number=h_c_number)
        if shiGongChecks:
            message = {"code": 1, "msg": '当前孔已有验收记录!'}
        else:
            shiGongCheck = ShiGongCheck(
                row_id=row_Id,
                h_c_number=h_c_number,
                isQiQuan=isQiQuan,
                isCeXie=isCeXie,
                date_time=date,
                person=person,
                desc=desc
            )
            shiGongCheck.save()
            message = {"code": 0, "msg": '提交成功!'}
    else:
        message = {"code": 1, "msg": '提交失败!'}
    return JsonResponse(message)


@xframe_options_exempt
@csrf_exempt
# 跳转到管理员——打孔申请审批界面
def operator_drilling_design(request):
    result = {}
    user = user_group.objects.filter(username=request.session.get("username")).first()
    if user is not None:
        belongMine = user.belongMine
        work_face = Work_face.objects.filter(mine=belongMine)
        if work_face is not None:
            work_face_obj = work_face.values_list("id", "w_name")
            result['work_face'] = work_face_obj
    return render(request, 'Operator/Drilling_Design_Params.html', result)


# 钻孔设计参数查询
@xframe_options_exempt
@csrf_exempt
def operator_reload_DrillingDesignParams(request):
    page = request.GET.get('page')
    page_limit = request.GET.get('limit')
    hole_data = []
    message = None
    try:
        kong_num = request.GET.get('kong_num')
        rowId = request.GET.get('rowId')
        row = Row.objects.filter(id=rowId).first()
        if kong_num:
            hole_design_datas = Hole_Design.objects.filter(row=row, hole_number=kong_num, status="0")
        else:
            hole_design_datas = Hole_Design.objects.filter(row=row, status="0")
        hole_list = []
        for item in hole_design_datas:
            hole_list.append(model_to_dict(item))
        paginator = Paginator(hole_list, page_limit)
        # 前端传来页数的数据
        data = paginator.page(page)
        for i in range(len(data)):
            status = hole_list[i]['status']
            desc = statusChoice[status]
            status = int(status)
            hole_data.append({"id": hole_list[i]['id'], "pai_num": row.row_id, "kong_num": hole_list[i]['hole_number'],
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
                              "desc": desc})
        message = message_data(0, "", len(hole_list), hole_data)
    except Exception as e:
        logging.log("查询结果异常" + e)
        message = message_data(1, "", 0)
    finally:
        return JsonResponse(message)


def getRound2(value):
    if value is None:
        return ""
    else:
        return round(value, 2)


@csrf_exempt
def passOrrejectHoleDesign(request):
    data = request.POST
    res = {}
    res["code"] = "1"
    try:
        id = data["id"]
        hole_number = data["hole_number"]
        status = data["status"]
        holeDesigns = Hole_Design.objects.filter(id=id, hole_number=hole_number, status="0")
        if holeDesigns:
            holeDesign = holeDesigns.first()
            holeDesign.status = status
            holeDesign.currentHoleFlag = "0"
            holeDesign.desc = statusChoice[holeDesign.status]
            holeDesign.save()
            res["code"] = "0"
            res["msg"] = "提交成功"
        else:
            res["msg"] = "查询记录为空"

    except Exception as e:
        res["msg"] = "接口异常" + e
    finally:
        return JsonResponse(res)


@xframe_options_exempt
@csrf_exempt
# 跳转到管理员——打孔申请审批历史记录
def operator_drilling_design_his(request):
    result = {}
    user = user_group.objects.filter(username=request.session.get("username")).first()
    if user is not None:
        belongMine = user.belongMine
        work_face = Work_face.objects.filter(mine=belongMine)
        if work_face is not None:
            work_face_obj = work_face.values_list("id", "w_name")
            result['work_face'] = work_face_obj
    return render(request, 'Operator/Drilling_Design_Params_His.html', result)


# 钻孔设计审批记录查询
@xframe_options_exempt
@csrf_exempt
def operator_reload_DrillingDesignParamsHis(request):
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
            hole_design_datas = Hole_Design.objects.filter(row_id=rowId, hole_number=kong_num, status__in=["1", "2"])
        elif rowId:
            hole_design_datas = Hole_Design.objects.filter(row_id=rowId, status__in=["1", "2"])
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
                                  "desc": desc})
            message = message_data(0, "", len(hole_list), hole_data)
        else:
            message = message_data(0, "", 0, [])
    except Exception as e:
        logging.log("查询结果异常" + e)
        message = message_data(1, "", 0, [])
    finally:
        return JsonResponse(message)


# 跳转到钻孔施工数据列表
@xframe_options_exempt
@csrf_exempt
def operator_drill_construct_list_page(request):
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
    return render(request, "Operator/construct_list_page.html", result)


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
            holeConstructionDatas = Hole_Construction.objects.filter(row=row, h_c_number=kong_num, status="0")
        else:
            holeConstructionDatas = Hole_Construction.objects.filter(row=row, status="0")
        hole_list = []
        for item in holeConstructionDatas:
            holeDesign = Hole_Design.objects.get(hole_number=item.h_c_number)
            time = item.time
            remove_drill_start = item.remove_drill_start
            remove_drill_end = item.remove_drill_end
            deflection_angle = holeDesign.deflection_angle  # 钻孔设计偏角
            design_elevation_angel = holeDesign.design_elevation_angel  # 钻孔设计仰角
            rock_section = holeDesign.rock_section  # 钻孔见煤位置
            hole_depth = holeDesign.hole_depth  # 设计孔深
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
def operator_drill_construct_list_his(request):
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
    return render(request, "Operator/construct_list_his.html", result)


# 给钻孔施工数据列表刷新数据
@xframe_options_exempt
@csrf_exempt
def construct_list_data_his(request):
    try:
        page = request.GET.get('page')
        page_limit = request.GET.get('limit')
        kong_num = request.GET.get('kong_num')
        rowId = request.GET.get('rowId')
        row = Row.objects.filter(id=rowId).first()
        if kong_num:
            holeConstructionDatas = Hole_Construction.objects.filter(row=row, h_c_number=kong_num,
                                                                     status__in=["1", "2"])
        else:
            holeConstructionDatas = Hole_Construction.objects.filter(row=row, status__in=["1", "2"])
        hole_list = []
        for item in holeConstructionDatas:
            holeDesign = Hole_Design.objects.get(hole_number=item.h_c_number)
            time = item.time
            remove_drill_start = item.remove_drill_start
            remove_drill_end = item.remove_drill_end
            deflection_angle = holeDesign.deflection_angle  # 钻孔设计偏角
            design_elevation_angel = holeDesign.design_elevation_angel  # 钻孔设计仰角
            rock_section = holeDesign.rock_section  # 钻孔见煤位置
            hole_depth = holeDesign.hole_depth  # 设计孔深
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


# 跳转到冲孔申请审批界面
@xframe_options_exempt
@csrf_exempt
def operator_flush_apply_page(request):
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
    return render(request, "Operator/flush_apply_page.html", result)


# 跳转到冲孔确认审批界面
@xframe_options_exempt
@csrf_exempt
def operator_flush_drill_list_page(request):
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
    return render(request, "Operator/flush_drill_list_page.html", result)


# 跳转到冲孔列表
@xframe_options_exempt
@csrf_exempt
def operator_flush_drill_list_his(request):
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
    return render(request, "Operator/flush_drill_list_his.html", result)


# 冲孔数据列表刷新
@xframe_options_exempt
@csrf_exempt
def flush_drill_list_data(request):
    page = request.GET.get('page')
    page_limit = request.GET.get('limit')
    kong_num = request.GET.get('kong_num')
    rowId = request.GET.get('rowId')
    row = Row.objects.filter(id=rowId).first()
    if kong_num:
        washCoalConstructions = Wash_Coal_Construction.objects.filter(row=row, h_c_number=kong_num, status="0")
    else:
        washCoalConstructions = Wash_Coal_Construction.objects.filter(row=row, status="0")
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
        hole_list.append(holeJson)
    paginator = Paginator(hole_list, page_limit)
    # 前端传来页数的数据
    data = paginator.page(page)
    message = message_data(0, "", len(hole_list), hole_list)
    return JsonResponse(message)


# 冲孔数据列表刷新
@xframe_options_exempt
@csrf_exempt
def flush_apply_data(request):
    page = request.GET.get('page')
    page_limit = request.GET.get('limit')
    kong_num = request.GET.get('kong_num')
    rowId = request.GET.get('rowId')
    row = Row.objects.filter(id=rowId).first()
    if kong_num:
        washCoalConstructions = Wash_Coal_Construction.objects.filter(row=row, h_c_number=kong_num, status="3")
    else:
        washCoalConstructions = Wash_Coal_Construction.objects.filter(row=row, status="3")
    hole_list = []
    for item in washCoalConstructions:
        holeJson = model_to_dict(item)
        holeJson["row"] = row.row_id
        hole_list.append(holeJson)
    paginator = Paginator(hole_list, page_limit)
    # 前端传来页数的数据
    data = paginator.page(page)
    message = message_data(0, "", len(hole_list), hole_list)
    return JsonResponse(message)


# 冲孔数据列表刷新
@xframe_options_exempt
@csrf_exempt
def flush_drill_list_his(request):
    page = request.GET.get('page')
    page_limit = request.GET.get('limit')
    kong_num = request.GET.get('kong_num')
    rowId = request.GET.get('rowId')
    row = Row.objects.filter(id=rowId).first()
    if kong_num:
        washCoalConstructions = Wash_Coal_Construction.objects.filter(row=row, h_c_number=kong_num,
                                                                      status__in=["1", "2"])
    else:
        washCoalConstructions = Wash_Coal_Construction.objects.filter(row=row, status__in=["1", "2"])
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
        hole_list.append(holeJson)
    paginator = Paginator(hole_list, page_limit)
    # 前端传来页数的数据
    data = paginator.page(page)
    message = message_data(0, "", len(hole_list), hole_list)
    return JsonResponse(message)


# ----------------------------------封孔填报-----------------------------------------

# 跳转到封孔申请审批界面
@xframe_options_exempt
@csrf_exempt
def operator_feng_apply_page(request):
    result = {}
    # work_face_obj = Work_face.objects.values_list("w_name")
    user = user_group.objects.filter(username=request.session.get("username")).first()
    if user is not None:
        belongMine = user.belongMine
        work_face = Work_face.objects.filter(mine=belongMine)
        if work_face is not None:
            work_face_obj = work_face.values_list("id", "w_name")
            result['work_face'] = work_face_obj
    return render(request, "Operator/feng_apply_page.html", result)


# 跳转到封孔确认审批列表
@xframe_options_exempt
@csrf_exempt
def operator_feng_drill_list_page(request):
    result = {}
    # work_face_obj = Work_face.objects.values_list("w_name")
    user = user_group.objects.filter(username=request.session.get("username")).first()
    if user is not None:
        belongMine = user.belongMine
        work_face = Work_face.objects.filter(mine=belongMine)
        if work_face is not None:
            work_face_obj = work_face.values_list("id", "w_name")
            result['work_face'] = work_face_obj
    return render(request, "Operator/feng_drill_list_page.html", result)


# 跳转到封孔审批记录列表
@xframe_options_exempt
@csrf_exempt
def operator_feng_drill_list_his(request):
    result = {}
    # work_face_obj = Work_face.objects.values_list("w_name")
    user = user_group.objects.filter(username=request.session.get("username")).first()
    if user is not None:
        belongMine = user.belongMine
        work_face = Work_face.objects.filter(mine=belongMine)
        if work_face is not None:
            work_face_obj = work_face.values_list("id", "w_name")
            result['work_face'] = work_face_obj
    return render(request, "Operator/feng_drill_list_his.html", result)


# 封孔数据列表刷新
@xframe_options_exempt
@csrf_exempt
def feng_drill_list_data(request):
    page = request.GET.get('page')
    page_limit = request.GET.get('limit')
    kong_num = request.GET.get('kong_num')
    rowId = request.GET.get('rowId')
    row = Row.objects.filter(id=rowId).first()
    if kong_num:
        zhuJiangConstructions = zhu_jiang_Construction.objects.filter(row=row, h_c_number=kong_num, status="0")
    else:
        zhuJiangConstructions = zhu_jiang_Construction.objects.filter(row=row, status="0")
    hole_list = []
    for item in zhuJiangConstructions:
        feng_time = item.feng_time.strftime("%Y-%m-%d %H:%M:%S")
        holeJson = model_to_dict(item)
        holeJson["row"] = row.row_id
        holeJson["feng_time"] = feng_time
        hole_list.append(holeJson)
    paginator = Paginator(hole_list, page_limit)
    # 前端传来页数的数据
    data = paginator.page(page)
    message = message_data(0, "", len(hole_list), hole_list)
    return JsonResponse(message)


# 封孔数据列表刷新
@xframe_options_exempt
@csrf_exempt
def feng_drill_list_his(request):
    page = request.GET.get('page')
    page_limit = request.GET.get('limit')
    kong_num = request.GET.get('kong_num')
    rowId = request.GET.get('rowId')
    row = Row.objects.filter(id=rowId).first()
    if kong_num:
        zhuJiangConstructions = zhu_jiang_Construction.objects.filter(row=row, h_c_number=kong_num,
                                                                      status__in=["1", "2"])
    else:
        zhuJiangConstructions = zhu_jiang_Construction.objects.filter(row=row, status__in=["1", "2"])
    hole_list = []
    for item in zhuJiangConstructions:
        feng_time = item.feng_time.strftime("%Y-%m-%d %H:%M:%S")
        holeJson = model_to_dict(item)
        holeJson["row"] = row.row_id
        holeJson["feng_time"] = feng_time
        hole_list.append(holeJson)
    paginator = Paginator(hole_list, page_limit)
    # 前端传来页数的数据
    data = paginator.page(page)
    message = message_data(0, "", len(hole_list), hole_list)
    return JsonResponse(message)


# 封孔申请列表刷新
@xframe_options_exempt
@csrf_exempt
def feng_apply_data(request):
    page = request.GET.get('page')
    page_limit = request.GET.get('limit')
    kong_num = request.GET.get('kong_num')
    rowId = request.GET.get('rowId')
    row = Row.objects.filter(id=rowId).first()
    if kong_num:
        zhuJiangConstructions = zhu_jiang_Construction.objects.filter(row=row, h_c_number=kong_num, status="3")
    else:
        zhuJiangConstructions = zhu_jiang_Construction.objects.filter(row=row, status="3")
    hole_list = []
    for item in zhuJiangConstructions:
        holeJson = model_to_dict(item)
        holeJson["row"] = row.row_id
        hole_list.append(holeJson)
    paginator = Paginator(hole_list, page_limit)
    # 前端传来页数的数据
    data = paginator.page(page)
    message = message_data(0, "", len(hole_list), hole_list)
    return JsonResponse(message)


@csrf_exempt
def passOrrejectHoleConstruction(request):
    data = request.POST
    res = {}
    res["code"] = "1"
    try:
        id = data["id"]
        hole_number = data["hole_number"]
        status = data["status"]
        beforeStatus = data["beforeStatus"]
        reason = data["reason"]
        holeConstructions = Hole_Construction.objects.filter(id=id, h_c_number=hole_number, status=beforeStatus)
        if holeConstructions:
            holeConstruction = holeConstructions.first()
            holeConstruction.status = status
            holeConstruction.desc = statusChoice[holeConstruction.status]
            holeConstruction.reason = reason
            holeConstruction.save()
            res["code"] = "0"
            res["msg"] = "提交成功"
        else:
            res["msg"] = "钻孔申请记录为空"

    except Exception as e:
        res["msg"] = "接口异常" + e
    finally:
        return JsonResponse(res)


# 提交冲孔申请
@csrf_exempt
def passOrrejectFlushHole(request):
    data = request.POST
    res = {}
    res["code"] = "1"
    try:
        hole_number = data["hole_number"]
        id = data["id"]
        beforeStatus = data["beforeStatus"]
        status = data["status"]
        reason = data["reason"]
        washCoalConstructions = Wash_Coal_Construction.objects.filter(h_c_number=hole_number, id=id,
                                                                      status=beforeStatus)
        if washCoalConstructions:
            washCoalConstruction = washCoalConstructions.first()
            washCoalConstruction.status = status
            washCoalConstruction.desc = statusChoice[status]
            washCoalConstruction.reason = reason
            washCoalConstruction.save()
            res["code"] = "0"
            res["msg"] = "提交成功"
        else:
            res["msg"] = "冲孔确认申请记录为空"

    except Exception as e:
        res["msg"] = "接口异常" + e
    finally:
        return JsonResponse(res)


# 提交注浆申请
@csrf_exempt
def passOrrejectFengHole(request):
    data = request.POST
    res = {}
    res["code"] = "1"
    try:
        hole_number = data["hole_number"]
        id = data["id"]
        beforeStatus = data["beforeStatus"]
        status = data["status"]
        reason = data["reason"]
        zhujiangConstructions = zhu_jiang_Construction.objects.filter(h_c_number=hole_number, id=id,
                                                                      status=beforeStatus)
        if zhujiangConstructions:
            zhujiangConstruction = zhujiangConstructions.first()
            zhujiangConstruction.status = status
            zhujiangConstruction.desc = statusChoice[status]
            zhujiangConstruction.reason = reason
            zhujiangConstruction.save()
            res["code"] = "0"
            res["msg"] = "提交成功"
        else:
            res["msg"] = "封孔确认申请记录为空"

    except Exception as e:
        res["msg"] = "接口异常" + e
    finally:
        return JsonResponse(res)

#视频监控验收根据排号查询封孔后的孔号信息
@csrf_exempt
def getHoleFengData(request):
    data = {}
    try:
        rowId = request.POST["row"]
        if rowId:
            logging.INFO = "rowId" + rowId + "得到排号信息"
            rows = Row.objects.filter(id=rowId)
            if rows:
                row = rows.first()
                zhuJiangConstructions = zhu_jiang_Construction.objects.filter(row=row, status="1")
                if zhuJiangConstructions:
                    data = serializers.serialize('json', zhuJiangConstructions)
    except Exception as e:
        logging.INFO = "获取设计孔信息异常" + e
    finally:
        res = {"data": data}
        return JsonResponse(res)


#视频监控验收根据孔号渲染界面
@csrf_exempt
def getVidioCheckDataByHoleNum(request):
    data = request.POST
    dataDict = {}
    if data:
        rowId = data["rowId"]
        h_c_number = data["kong_num"]
        if rowId and h_c_number:
            holeConstructions = Hole_Construction.objects.filter(row_id=rowId, h_c_number=h_c_number)
            washCoalConstructions = Wash_Coal_Construction.objects.filter(row_id=rowId, h_c_number=h_c_number)
            zhuJiangConstructions = zhu_jiang_Construction.objects.filter(row_id=rowId, h_c_number=h_c_number)
            if holeConstructions and washCoalConstructions and zhuJiangConstructions:
                holeConstruction = holeConstructions.first()
                washCoalConstruction = washCoalConstructions.first()
                zhuJiangConstruction = zhuJiangConstructions.first()
                end_hole_depth = 0 if not zhuJiangConstruction.end_hole_depth else float(
                    zhuJiangConstruction.end_hole_depth)
                start_hole_depth = 0 if not zhuJiangConstruction.start_hole_depth else float(
                    zhuJiangConstruction.start_hole_depth)
                dataDict = {'kong_num': h_c_number,
                            'pian_angle': holeConstruction.r_deflection_angle,
                            'hole_height': holeConstruction.hole_height,
                            'qing_angle': holeConstruction.r_elevation_angle,
                            'start_zuan_time': holeConstruction.time,
                            'flush_start_t': washCoalConstruction.water_start_time,
                            'flush_end_t': washCoalConstruction.water_end_time,
                            'mei_count': washCoalConstruction.actual_flush_mei,
                            'return_start_t': holeConstruction.remove_drill_start,
                            'return_end_t': holeConstruction.remove_drill_end,
                            'kong_depth': holeConstruction.con_hole_depth,
                            'worker_name': holeConstruction.construction_person_name,
                            'feng_start_t': zhuJiangConstruction.feng_time,
                            'feng_end_t': "",  # 没值
                            'feng_kong_len': abs(round(end_hole_depth - start_hole_depth, 2)),
                            'shai_guan_len': zhuJiangConstruction.screening_length,
                            'video_num': zhuJiangConstruction.video_number,
                            'error_msg': zhuJiangConstruction.grouting_abnormal_situation,
                            'video_people': '',  # 没值
                            'submit_time': zhuJiangConstruction.feng_time,
                            'class_times': ''}
    return JsonResponse(dataDict)

@csrf_exempt
def videos_check_submit_process(request):
    data = eval(request.POST["data"])
    res = {}
    res["code"] = "1"
    try:
        if data:
            rowId = data["row"]
            h_c_number = data["kong_num"]
            holeConstructions = Hole_Construction.objects.filter(row_id=rowId, h_c_number=h_c_number)
            washCoalConstructions = Wash_Coal_Construction.objects.filter(row_id=rowId, h_c_number=h_c_number)
            zhuJiangConstructions = zhu_jiang_Construction.objects.filter(row_id=rowId, h_c_number=h_c_number)
            if holeConstructions and washCoalConstructions and zhuJiangConstructions:
                holeConstruction = holeConstructions.first()
                washCoalConstruction = washCoalConstructions.first()
                zhuJiangConstruction = zhuJiangConstructions.first()
                time = data["drill_start_time"]
                water_start_time = data["flush_start_time"]
                water_end_time = data["flush_end_time"]
                drill_start_time = data["drill_start_time"]
                remove_drill_start = data["reback_start_time"]
                remove_drill_end = data["reback_end_time"]
                feng_time = data["feng_start_time"]
                video_number = data["video_num"]
                holeConstruction.time = time
                washCoalConstruction.water_start_time = water_start_time
                washCoalConstruction.water_end_time = water_end_time
                holeConstruction.remove_drill_start = remove_drill_start
                holeConstruction.remove_drill_end = remove_drill_end
                zhuJiangConstruction.feng_time = feng_time
                zhuJiangConstruction.video_number = video_number
                holeConstruction.save()
                washCoalConstruction.save()
                zhuJiangConstruction.save()
                res["code"] = "0"
    except Exception as e:
       logging.INFO = "提交异常" + e
    finally:
       return JsonResponse(res)


