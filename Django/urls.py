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
from Mining import views, tool_views, operator_views, worker_views, admin_views
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
    path('drill_quality_assess/', worker_views.drill_quality_assess, name="drill_quality_assess"),  # 打钻质量评价
    path('empty_area_assess/', worker_views.empty_area_assess, name="empty_area_assess"),           # 空白区域评价
    path('seal_grouting_assess/', worker_views.seal_grouting_assess, name="seal_grouting_assess"),  # 封孔注浆评价
    path('exception_handle_page/', worker_views.exception_handle_page, name="exception_handle_page"),  # 异常处置


    # 超级管理员路由
    # path('admin_index/', admin_views.admin_login_index, name='admin_index'),
    # path('admin_worker_manage/', admin_views.worker_manage, name="admin_worker_manage"),    # 跳转到管理员工页面
    # path('admin_workerList_interface/', admin_views.worker_list_interface, name="admin_workerList_interface"),    # 员工数据列表接口
    # path('admin_operator_manage/', admin_views.operator_manage, name='admin_operator_manage'),  # 跳转到操作员管理页面
    # path('admin_operatorList_interface/', admin_views.operator_list_interface, name='admin_operatorList_interface'),    # 操作员数据列表接口

] + static (settings.STATIC_URL, document_root = settings.STATIC_ROOT)
