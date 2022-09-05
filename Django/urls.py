"""Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Mining import views, operator_views, worker_views, admin_views
from django.conf import settings
from django.conf.urls. static import static

urlpatterns = [
    path('Mining/', include(('Mining.urls', 'Mining'), namespace='Mining')),
    path('admin/', admin.site.urls),
    path('logout/', views.user_logout, name="logout"),  # 用户退出登录按钮
    path('', views.login, name="login"),     # 用户登录
    path('user_login_check/', views.user_login_check, name="user_login_check"),     # 用户登录认证界面
    path('worker_index/', worker_views.worker_login_index, name="worker_index"),     # 登录工人操作界面

    path('worker_project_list/', worker_views.worker_project_list, name="worker_project_list"),     # 工人登录到工程列表界面
    path('get_project_list/', worker_views.get_project_list, name="get_project_list"),      # 获取工程数据列表

    path('project_eval_list/', worker_views.project_eval_list, name="project_eval_list"),   # 工人登录到工程评价列表界面
    path('get_evaluate_list/', worker_views.get_evaluate_list, name="get_evaluate_list"),   # 获取钻空评价列表

    path('project_data_input/', worker_views.project_data_input, name="project_data_input"),    # 跳转到钻孔数据填报页面
    path('get_dataInput_list/', worker_views.get_dataInput_list, name="get_dataInput_list"),    # 数据填报页面
    path('worker_load_data/', worker_views.worker_load_data, name="worker_load_data"),     # 工人数据表单提交

    path('operator_index/', operator_views.operator_login_index, name="operator_index"),    # 登录操作人员界面
    # path('admin_index/', admin_views.admin_login_index, name="admin_index"),  # 登录到超级管理员界面

    path('user_person/', views.user_person, name="user_person"),        # 个人信息中心

    # 跳转到工人操作页面
    path('project_report_page/', worker_views.project_report_page, name='project_report_page'),

    # 钻孔设计路由
    path('drilling_design_params/', worker_views.drilling_design_params, name="drilling_design_params"),   # 钻孔设计参数
    path('warning_reminder/', worker_views.warning_reminder, name="warning_reminder"),   # 预警提醒
    path('sealing_grouting_design_params/', worker_views.sealing_grouting_design_params, name="sealing_grouting_design_params"),   # 封孔注浆设计参数


    # 钻孔施工路由
    path('site_drill_page/', worker_views.site_drill_page, name="site_drill_page"),              # 现场打钻
    path('site_confirm_page/', worker_views.site_confirm_page, name="site_confirm_page"),        # 现场验收
    path('seal_grout_page/', worker_views.seal_grout_page, name="seal_grout_page"),              # 封孔注浆
    path('ground_confirm_page/', worker_views.ground_confirm_page, name="ground_confirm_page"),  # 地面确认

    # 工程评价
    path('drill_quality_assess/', admin_views.drill_quality_assess, name="drill_quality_assess"),  # 打钻质量评价
    path('empty_area_assess/', admin_views.empty_area_assess, name="empty_area_assess"),           # 空白区域评价
    path('seal_grouting_assess/', admin_views.seal_grouting_assess, name="seal_grouting_assess"),  # 封孔注浆评价

    path('getDrillQualityAssessData/', admin_views.getDrillQualityAssessData, name = "getDrillQualityAssessData"), #获取打孔质量评价数据
    path('getEmptyAreaAssessData/', admin_views.getEmptyAreaAssessData, name = "getEmptyAreaAssessData"), #获取空白区域评价数据
    path('exception_handle_page/', worker_views.exception_handle_page, name="exception_handle_page"),  # 异常处置


    # 超级管理员路由
    # path('admin_index/', admin_views.admin_login_index, name='admin_index'),
    # path('admin_worker_manage/', admin_views.worker_manage, name="admin_worker_manage"),    # 跳转到管理员工页面
    # path('admin_workerList_interface/', admin_views.worker_list_interface, name="admin_workerList_interface"),    # 员工数据列表接口
    # path('admin_operator_manage/', admin_views.operator_manage, name='admin_operator_manage'),  # 跳转到操作员管理页面
    # path('admin_operatorList_interface/', admin_views.operator_list_interface, name='admin_operatorList_interface'),    # 操作员数据列表接口

    #刘利利写的新接口
    # 根据工作面id获取巷道信息
    path('getTunnelByWorkface/', worker_views.getTunnelByWorkface, name='getTunnelByWorkface'),    # 数据中心路由
    #根据巷道id获取排号信息
    path('getRowByTunnel/', worker_views.getRowByTunnel, name='getRowByTunnel'),    # 数据中心路由
    # 根据排号获取当前设计孔信息
    path('getHoleDesignData/', worker_views.getHoleDesignData, name='getHoleDesignData'),    # 数据中心路由
    path('getHoleConstructionData/', worker_views.getHoleConstructionData, name='getHoleConstructionData'),    # 数据中心路由
    path('getZuanKongQualityData/', worker_views.getZuanKongQualityData, name='getZuanKongQualityData'),    # 数据中心路由
    path('submitHoleConstruction/', worker_views.submitHoleConstruction, name='submitHoleConstruction'),    # 数据中心路由
    path('submitWashCoalConstruction/', worker_views.submitWashCoalConstruction, name='submitWashCoalConstruction'),    # 数据中心路由
    path('submitFengCoalConstruction/', worker_views.submitFengCoalConstruction, name='submitFengCoalConstruction'),    # 数据中心路由
    #
    path('drill_apply_record_page/', worker_views.drill_apply_record_page, name='drill_apply_record_page'),
    # path('drilling_design_params_fill/', worker_views.drilling_design_params_fill, name="drilling_design_params_fill"),
    path('reloadDrillingDesignParams/', worker_views.reloadDrillingDesignParams, name='reloadDrillingDesignParams'),
    path('getFlushHoleByRow/', worker_views.getFlushHoleByRow, name='getFlushHoleByRow'),
    path('getFengHoleByRow/', worker_views.getFengHoleByRow, name='getFengHoleByRow'),
    path('getMeiDuanLength/', worker_views.getMeiDuanLength, name='getMeiDuanLength'),

    path('resubmitHoleDesign/', worker_views.resubmitHoleDesign, name = 'resubmitHoleDesign'),
    #操作员路由
    #打孔申请界面
    path('operator_drilling_design/', operator_views.operator_drilling_design, name="operator_drilling_design"),
    #打孔审批界面表格数据渲染
    path('operator_reload_DrillingDesignParams/', operator_views.operator_reload_DrillingDesignParams, name="operator_reload_DrillingDesignParams"),
    #审批通过/驳回
    path('passOrrejectHoleDesign/', operator_views.passOrrejectHoleDesign, name="passOrrejectHoleDesign"),
    #打孔申请历史记录
    path('operator_drilling_design_his/', operator_views.operator_drilling_design_his,name="operator_drilling_design_his"),
    path('operator_reload_DrillingDesignParamsHis/', operator_views.operator_reload_DrillingDesignParamsHis,name="operator_reload_DrillingDesignParamsHis"),

    #施工审批界面
    path('operator_drill_construct_list_page/',operator_views.operator_drill_construct_list_page, name="operator_drill_construct_list_page"),
    # 施工审批界面列表刷新数据
    path('construct_list_data/', operator_views.construct_list_data, name='construct_list_data'),
    # 施工审批记录
    path('operator_drill_construct_list_his/', operator_views.operator_drill_construct_list_his, name="operator_drill_construct_list_his"),
    # 给钻孔施工审批数据列表刷新数据
    path('construct_list_data_his/', operator_views.construct_list_data_his, name='construct_list_data_his'),

    #冲孔审批界面
    path('operator_flush_apply_page/', operator_views.operator_flush_apply_page,name="operator_flush_apply_page"),
    path('operator_flush_drill_list_page/', operator_views.operator_flush_drill_list_page,name="operator_flush_drill_list_page"),
    path('operator_flush_drill_list_his/', operator_views.operator_flush_drill_list_his,name="operator_flush_drill_list_his"),
    path('flush_drill_list_data/', operator_views.flush_drill_list_data,name="flush_drill_list_data"),
    path('flush_apply_data/', operator_views.flush_apply_data,name="flush_apply_data"),
    path('flush_drill_list_his/', operator_views.flush_drill_list_his,name="flush_drill_list_his"),
    #封孔审批界面
    path('operator_feng_apply_page/', operator_views.operator_feng_apply_page,name="operator_feng_apply_page"),
    path('operator_feng_drill_list_page/', operator_views.operator_feng_drill_list_page,name="operator_feng_drill_list_page"),
    path('operator_feng_drill_list_his/', operator_views.operator_feng_drill_list_his,name="operator_feng_drill_list_his"),
    path('feng_drill_list_data/', operator_views.feng_drill_list_data,name="feng_drill_list_data"),
    path('feng_drill_list_his/', operator_views.feng_drill_list_his,name="feng_drill_list_his"),
    path('feng_apply_data/', operator_views.feng_apply_data, name="feng_apply_data"),
    # 审批通过/驳回
    path('passOrrejectHoleConstruction/', operator_views.passOrrejectHoleConstruction, name="passOrrejectHoleConstruction"),
    path('passOrrejectFlushHole/', operator_views.passOrrejectFlushHole, name="passOrrejectFlushHole"),
    path('passOrrejectFengHole/', operator_views.passOrrejectFengHole, name="passOrrejectFengHole"),

    #钻孔冲煤申请
    path('submitFlushData/', worker_views.submitFlushData, name='submitFlushData'),
    path('submitFengData/', worker_views.submitFengData, name='submitFengData'),
    #根据排号查找封孔完成的孔
    path('getHoleFengData/', operator_views.getHoleFengData, name='getHoleFengData'),  # 数据中心路由
    path('getVidioCheckDataByHoleNum/', operator_views.getVidioCheckDataByHoleNum, name='getVidioCheckDataByHoleNum'),  # 数据中心路由
    path('videos_check_submit_process/', operator_views.videos_check_submit_process, name='videos_check_submit_process'),  # 数据中心路由

] + static (settings.STATIC_URL, document_root = settings.STATIC_ROOT)
