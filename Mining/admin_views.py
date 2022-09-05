from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from Mining.tool_views import message_data
# from util.tests import *
from util.DrawPictureUtils import *
from .models import *
import numpy as np
import pandas as pd


@xframe_options_exempt
@csrf_exempt
# 超级管理员登录的操作视图
def admin_login_index(request):
    userName = request.session.get("username")
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
    # draw_picture('16071中部底抽巷', 4)
    result = {}
    user = user_group.objects.filter(username=request.session.get("username")).first()
    if user is not None:
        belongMine = user.belongMine
        work_face = Work_face.objects.filter(mine=belongMine)
        if work_face is not None:
            work_face_obj = work_face.values_list("id", "w_name")
            result['work_face'] = work_face_obj
    return render(request, 'Super/admin_DrawGraph.html', result)


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



@xframe_options_exempt
@csrf_exempt
# 跳转到打钻质量评价页面
def drill_quality_assess(request):
    result = {}
    user = user_group.objects.filter(username=request.session.get("username")).first()
    if user is not None:
        belongMine = user.belongMine
        work_face = Work_face.objects.filter(mine=belongMine)
        if work_face is not None:
            work_face_obj = work_face.values_list("id", "w_name")
            result['work_face'] = work_face_obj
    return render(request, 'Super/Drill_Quality_Assess.html', result)


@xframe_options_exempt
@csrf_exempt
# 跳转到空白区域评价页面
def empty_area_assess(request):
    result = {}
    user = user_group.objects.filter(username=request.session.get("username")).first()
    if user is not None:
        belongMine = user.belongMine
        work_face = Work_face.objects.filter(mine=belongMine)
        if work_face is not None:
            work_face_obj = work_face.values_list("id", "w_name")
            result['work_face'] = work_face_obj
    return render(request, 'Super/Empty_Area_Assess.html', result)


@xframe_options_exempt
@csrf_exempt
# 跳转到封孔注浆评价页面
def seal_grouting_assess(request):
    result = {}
    user = user_group.objects.filter(username=request.session.get("username")).first()
    if user is not None:
        belongMine = user.belongMine
        work_face = Work_face.objects.filter(mine=belongMine)
        if work_face is not None:
            work_face_obj = work_face.values_list("id", "w_name")
            result['work_face'] = work_face_obj
    return render(request, 'Super/Seal_Grouting_Assess.html', result)



#打孔质量评价
@xframe_options_exempt
@csrf_exempt
def getDrillQualityAssessData(request):
    res = {}
    rowId = request.POST["rowId"]
    dataFrame1 = None
    dataFrame2 = None
    dataFrame3 = None
    desc = ""
    #当前排
    completionPlanCoordinates = Completion_plan_coordinate.objects.filter(completion_row_id = rowId).order_by('completion_hole_num')
    #获取钻孔评价和钻煤评价
    if completionPlanCoordinates:
        errData = []
        Data2 = []
        # holeNumList = []
        rockSectionList = []
        # seeCeilList = []
        controlMax = None
        controlMin = None
        for completionPlanCoordinate in completionPlanCoordinates:
            hole_num = completionPlanCoordinate.completion_hole_num
            controlMax =completionPlanCoordinate.see_coal_y if (controlMax is None or controlMax < completionPlanCoordinate.see_coal_y) else controlMax
            controlMin =completionPlanCoordinate.see_coal_y if (controlMin is None or controlMin > completionPlanCoordinate.see_coal_y) else controlMin
            holeDesignList = Hole_Design.objects.filter(hole_number = hole_num)
            holeConstructionList =  Hole_Construction.objects.filter(h_c_number = hole_num)
            if holeDesignList and holeConstructionList:
                holeDesign = holeDesignList.first()
                holeConstruction = holeConstructionList.first()
                errData.append([len(errData), holeDesign.rock_section - holeConstruction.con_see_coal,holeDesign.see_ceil - holeConstruction.con_see_ceil])
                rockSectionList.append({"hole_num":hole_num, "rockSectionDif":holeDesign.rock_section - holeConstruction.con_see_coal,"seeCeilDif": holeDesign.see_ceil - holeConstruction.con_see_ceil, "errorDesc": holeConstruction.drill_eval})
            temp = []
            temp.append(completionPlanCoordinate.completion_hole_num)
            temp.append(completionPlanCoordinate.kai_kong_x)
            temp.append(completionPlanCoordinate.kai_kong_y)
            temp.append(completionPlanCoordinate.see_coal_x)
            temp.append(completionPlanCoordinate.see_coal_y)
            temp.append(completionPlanCoordinate.see_cile_x)
            temp.append(completionPlanCoordinate.see_cile_y)
            temp.append(completionPlanCoordinate.hole_depth_x)
            temp.append(completionPlanCoordinate.hole_depth_y)
            Data2.append(temp)
        controlDesc = "该排控制范围上侧" + str(controlMax) + "m,控制范围下侧" + str(controlMin) + "m。"
        pingjia = ""
        desc = controlDesc + pingjia
        dataFrame2 = pd.DataFrame(Data2)
        dataFrame2.columns = ['孔号','开孔x', '开孔y','见煤x', '见煤y', '见顶x','见顶y','终孔x',  '终孔y']
        fan_yan_hole = draw_picture2(dataFrame2)
        errDataFrame = pd.DataFrame(errData)
        draw_picture3(errDataFrame)
        # dataFrame2 = dataFrame2[['孔号', '见顶x', '见顶y']]
    res["data"] = rockSectionList
    # res["fanYan"] = fan_yan_hole
    message = message_data(0, "", 5, res)
    return JsonResponse(message)

#空白质量评价
@xframe_options_exempt
@csrf_exempt
def getEmptyAreaAssessData(request):
    res = {}
    res = {}
    rowId = request.POST["rowId"]
    dataFrame1 = None
    dataFrame2 = None
    dataFrame3 = None
    desc = ""
    #当前排的上一个排
    completionPlanCoordinates1 = Completion_plan_coordinate.objects.filter(completion_row_id = str(int(rowId) - 1))
    #当前排
    completionPlanCoordinates2 = Completion_plan_coordinate.objects.filter(completion_row_id = rowId)
    # 当前排的下一个排
    completionPlanCoordinates3 = Completion_plan_coordinate.objects.filter(completion_row_id = str(int(rowId) + 1))
    #获取钻孔评价和钻煤评价
    holeEval = Hole_Eval.objects.filter(row_id = rowId)
    if not completionPlanCoordinates1 and not completionPlanCoordinates2 and not completionPlanCoordinates3:
        return
    if completionPlanCoordinates1:
        Data1 = []
        for completionPlanCoordinate in completionPlanCoordinates1:
            temp = []
            temp.append(completionPlanCoordinate.completion_hole_num)
            temp.append(completionPlanCoordinate.kai_kong_x)
            temp.append(completionPlanCoordinate.kai_kong_y)
            temp.append(completionPlanCoordinate.see_coal_x)
            temp.append(completionPlanCoordinate.see_coal_y)
            temp.append(completionPlanCoordinate.see_cile_x)
            temp.append(completionPlanCoordinate.see_cile_y)
            temp.append(completionPlanCoordinate.hole_depth_x)
            temp.append(completionPlanCoordinate.hole_depth_y)
            Data1.append(temp)
        dataFrame1 = pd.DataFrame(Data1)
        dataFrame1.columns = ['孔号','开孔x', '开孔y','见煤x', '见煤y', '见顶x','见顶y','终孔x',  '终孔y']
        dataFrame1 = dataFrame1[['孔号', '见顶x', '见顶y']]
    if completionPlanCoordinates2:
        Data2 = []
        controlMax = None
        controlMin = None
        for completionPlanCoordinate in completionPlanCoordinates2:
            controlMax =completionPlanCoordinate.see_coal_y if (controlMax is None or controlMax < completionPlanCoordinate.see_coal_y) else controlMax
            controlMin =completionPlanCoordinate.see_coal_y if (controlMin is None or controlMin > completionPlanCoordinate.see_coal_y) else controlMin
            temp = []
            temp.append(completionPlanCoordinate.completion_hole_num)
            temp.append(completionPlanCoordinate.kai_kong_x)
            temp.append(completionPlanCoordinate.kai_kong_y)
            temp.append(completionPlanCoordinate.see_coal_x)
            temp.append(completionPlanCoordinate.see_coal_y)
            temp.append(completionPlanCoordinate.see_cile_x)
            temp.append(completionPlanCoordinate.see_cile_y)
            temp.append(completionPlanCoordinate.hole_depth_x)
            temp.append(completionPlanCoordinate.hole_depth_y)
            Data2.append(temp)
        controlDesc = "该排控制范围上侧" + str(controlMax) + "m,控制范围下侧" + str(controlMin) + "m。"
        pingjia = ""
        if holeEval:
            for item in holeEval:
                if item.see_coal_eval != "见煤合格" or item.see_ceil_eval != "见顶合格":
                    pingjia = pingjia + "第" + item.h_name + "见煤不合格,原因是" + item.see_coal_eval + ",见顶不合格, 原因是" + item.see_ceil_eval + ",经补孔后合格。"
        desc = controlDesc + pingjia
        dataFrame2 = pd.DataFrame(Data2)
        dataFrame2.columns = ['孔号','开孔x', '开孔y','见煤x', '见煤y', '见顶x','见顶y','终孔x',  '终孔y']
        draw_picture1(dataFrame2)
        dataFrame2 = dataFrame2[['孔号', '见顶x', '见顶y']]
    if completionPlanCoordinates3:
        Data3 = []
        for completionPlanCoordinate in completionPlanCoordinates3:
            temp = []
            temp.append(completionPlanCoordinate.completion_hole_num)
            temp.append(completionPlanCoordinate.kai_kong_x)
            temp.append(completionPlanCoordinate.kai_kong_y)
            temp.append(completionPlanCoordinate.see_coal_x)
            temp.append(completionPlanCoordinate.see_coal_y)
            temp.append(completionPlanCoordinate.see_cile_x)
            temp.append(completionPlanCoordinate.see_cile_y)
            temp.append(completionPlanCoordinate.hole_depth_x)
            temp.append(completionPlanCoordinate.hole_depth_y)
            Data3.append(temp)
        dataFrame3 = pd.DataFrame(Data1)
        dataFrame3.columns = ['孔号','开孔x', '开孔y','见煤x', '见煤y', '见顶x','见顶y','终孔x',  '终孔y']
        dataFrame3 = dataFrame3[['孔号', '见顶x', '见顶y']]
    draw_picture4(dataFrame1 ,dataFrame2, dataFrame3)
    res["code"] = "0"
    res["desc"] = desc
    return JsonResponse(res)
