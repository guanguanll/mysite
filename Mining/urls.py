from django.contrib import admin
from django.urls import path

from Mining import worker_views, admin_views, operator_views

# 管理后台标题修改
admin.site.site_header = '智能采矿管理中心'  # 设置header
admin.site.site_title = '智能采矿管理中心'   # 设置title
admin.site.index_title = '智能采矿管理中心'


urlpatterns = [

    path('admin/', admin_views.admin_login_index),  # 登录到超级管理员界面
    path('admin_loginout_index/', admin_views.admin_loginout_index, name='admin_loginout_index'),   # 退出登录

    # -------------------------------------------矿工路由--------------------------------------------------------------
    path('worker/', worker_views.worker_login_index, name='worker_login_index'),
    path('drilling_construction_params/', worker_views.drilling_construction_params, name='drilling_construction_params'),
    path('drilling_design_params_fill/', worker_views.drilling_design_params_fill, name="drilling_design_params_fill"),
    path('drill_working_data_fillin/', worker_views.drill_working_data_fillin, name='drill_working_data_fillin'),
    path('drill_wash_data_fillin/', worker_views.drill_wash_data_fillin, name='drill_wash_data_fillin'),
    path('drill_sealing_data_fillin/', worker_views.drill_sealing_data_fillin, name='drill_sealing_data_fillin'),
    path('drill_roadway_choosed/', worker_views.drill_roadway_choosed, name='drill_roadway_choosed'),
    # 巷道选择提交处理
    path('drill_roadway_choosed_res/', worker_views.drill_roadway_choosed_res, name='drill_roadway_choosed_res'),
    # 申请打孔提交信息
    path('drill_apply_record_page/', worker_views.drill_apply_record_page, name='drill_apply_record_page'),
    path('drill_feedback_massage_fillin/', worker_views.drill_feedback_massage_fillin, name='drill_feedback_massage_fillin'),
    path('drill_feedback_data_fillin/', worker_views.drill_feedback_data_fillin, name='drill_feedback_data_fillin'),

    # 跳转到钻孔施工数据列表
    path('goto_drill_construct_list_page/', worker_views.goto_drill_construct_list_page, name='goto_drill_construct_list_page'),
    # 给钻孔施工数据列表刷新数据
    path('flush_drill_construct_list_data/', worker_views.flush_drill_construct_list_data, name='flush_drill_construct_list_data'),
    # 跳转到施工数据填报表单
    path('goto_drill_construct_layer_page/', worker_views.goto_drill_construct_layer_page, name='goto_drill_construct_layer_page'),

    # 跳转到冲孔数据list页面
    path('goto_flush_drill_list_page/', worker_views.goto_flush_drill_list_page, name='goto_flush_drill_list_page'),
    # 给冲孔数据list刷新数据
    path('goto_flush_drill_list_data/', worker_views.goto_flush_drill_list_data, name='goto_flush_drill_list_data'),
    # 冲孔数据填报表单
    path('goto_flush_drill_layer_page/', worker_views.goto_flush_drill_layer_page, name='goto_flush_drill_layer_page'),


    # 跳转到封孔数据list页面
    path('goto_feng_drill_list_page/', worker_views.goto_feng_drill_list_page, name='goto_feng_drill_list_page'),
    # 给封孔数据list刷新数据
    path('goto_feng_drill_list_data/', worker_views.goto_feng_drill_list_data, name='goto_feng_drill_list_data'),
    # 封孔数据填报表单
    path('goto_feng_drill_layer_page/', worker_views.goto_feng_drill_layer_page, name='goto_feng_drill_layer_page'),


    # -------------------------------------------操作员路由--------------------------------------------------------------
    path('operator/', operator_views.operator_login_index, name='operator_login_index'),
    # 操作员查看钻孔施工监控视list
    path('operator/check_videos_record_list/', operator_views.check_videos_record_list, name='check_videos_record_list'),
    # 操作员查看钻孔施工监控视list的渲染
    path('operator/check_videos_record_rendering/', operator_views.check_videos_record_rendering, name='check_videos_record_rendering'),
    # 操作员查看钻孔施工监控视list的填充
    path('operator/check_videos_record_fillin/', operator_views.check_videos_record_fillin, name='check_videos_record_fillin'),
    # 视屏监控数据提交
    path('videos_data_submit_process/', operator_views.videos_data_submit_process, name="videos_data_submit_process"),


    # 操作员查看视频举牌记录的list视图
    path('operator/check_videos_holding_record_list/', operator_views.check_videos_holding_record_list, name='check_videos_holding_record_list'),
    # 操作员查看视频举牌记录list的数据渲染视图
    path('operator/check_videos_holding_record_rendering/', operator_views.check_videos_holding_record_rendering, name='check_videos_holding_record_rendering'),
    # 操作员查看视频举牌记录的数据填充视图
    path('operator/check_videos_holding_record_fillin/', operator_views.check_videos_holding_record_fillin, name='check_videos_holding_record_fillin'),
    # 举牌记录填报
    path('videos_juipai_submit_process/', operator_views.videos_juipai_submit_process, name="videos_juipai_submit_process"),


    # 操作员查看施工资料记录的list
    path('operator/check_material_record_list/', operator_views.check_material_record_list, name='check_material_record_list'),
    # 操作员查看施工资料记录list的渲染
    path('operator/check_material_record_rendering/', operator_views.check_material_record_rendering, name='check_material_record_rendering'),
    # 操作员查看施工资料记录list的填充
    path('operator/check_material_record_fillin/', operator_views.check_material_record_fillin, name='check_material_record_fillin'),
    # 施工资料验收界面
    path('file_check_submit_process/', operator_views.file_check_submit_process, name='file_check_submit_process'),

    
    # 跳转到巷道选择页面
    path('operator/goto_roadway_choose_viewpage/', operator_views.goto_roadway_choose_viewpage, name='goto_roadway_choose_viewpage'),

    # 跳转到申请信息页面
    path('operator/goto_apply_record_viewpage/', operator_views.goto_apply_record_viewpage, name='goto_apply_record_viewpage'),
    # 申请信息页面数据渲染
    path('operator/goto_apply_record_rendering/', operator_views.goto_apply_record_rendering, name='goto_apply_record_rendering'),
    # 跳转到审批记录信息页面
    path('operator/goto_approve_record_viewpage', operator_views.goto_approve_record_viewpage, name='goto_approve_record_viewpage'),
    # 审批记录页面数据渲染
    path('operator/goto_approve_record_rendering/', operator_views.goto_approve_record_rendering, name='goto_approve_record_rendering'),




    # 管理员路由
    path('admin_draw_graph_one/', admin_views.admin_draw_graph_one, name='admin_draw_graph_one'),    # 智能绘图路由
    path('admin_search_data/', admin_views.admin_search_data, name='admin_search_data'),    # 数据中心路由
    path('admin_data_operator/', admin_views.admin_data_operator, name='admin_data_operator'),    # 数据中心路由
    path('admin_database_update/', admin_views.admin_database_update, name='admin_database_update'),    # 数据中心路由

]
