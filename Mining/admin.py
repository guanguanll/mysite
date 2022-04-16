from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin

# 用户组模型管理类
from .resources import *


@admin.register(user_group)
class UserGroupManage(admin.ModelAdmin):
    # 列表显示哪些字段的列
    list_display = ['username', 'userpwd', 'usertype']
    # 控制list_display中的字段， 哪些可以链接到修改页
    list_display_links = ['username']
    # 添加过滤器
    list_filter = ['username']


@admin.register(Mine)
class MineManager(admin.ModelAdmin):
    list_display = ['m_name', 'company', 'workface_count']
    list_filter = ['company']

    def workface_count(self, obj):
        return Work_face.objects.filter(mine=obj).count()

    workface_count.short_description = '工作面数量'


# 排管理类
@admin.register(Row)
class PaiManager(admin.ModelAdmin):
    list_display = ['tunnel', 'row_id', 'mei_qing_jiao', 'current_tunnel_depth', 'row_x', 'row_y', 'row_z',
                    'pillar_thickness',
                    'coal_seam_thickness', 'left_number', 'right_number']


# 公司组模型管理类
@admin.register(Company)
class CompanyManager(admin.ModelAdmin):
    list_display = ['c_name', 'mine_count']
    list_filter = ['c_name']

    # inlines = [MineInline]

    def mine_count(self, obj):
        return Mine.objects.filter(company=obj).count()

    mine_count.short_description = '煤矿数量'


# 工作面模型管理类
@admin.register(Work_face)
class WorkFaceManager(ImportExportActionModelAdmin):
    list_display = ['w_name', 'mine', 'odd_even_column_distance', 'w_name', 'distance_of_coal_rock_tunnel',
                    'change_of_coal_rock', 'with_of_coal_roadway', 'control_range_of_final_hole_to_meet',
                    'drivage_distance', 'recovery_distance', 'up_tunnel_up', 'down_tunnel_tunnel',
                    'qie_yan_qie', 'drainage_radius', 'thickness_of_pinch_coal', 'over_flush_coefficient',
                    'volume_weight_of_coal', 'coal_ultra_thick_divided', 'borehole_segmentation_standard1',
                    'borehole_segmentation_standard2']
    list_filter = ['w_name', 'mine']
    resource_class = WorkFaceProxyResource


# 巷道模型管理类
@admin.register(Tunnel)
class TunnelManager(ImportExportActionModelAdmin):
    list_display = ['work_face', 'tunnel_name', 'mine_width', 'mine_hight', 'di_ban_hang', 'mei_ceng_qing_jiao',
                    'tunnel_first_hole_number', 'arch_radius', 'zuan_kong_chui_ju', 'hole_height', 'di_ban_hang_hight',
                    'tunnel_actual_row_gap', 'up_control_x', 'up_control_y', 'up_control_z', 'down_control_x',
                    'down_control_y', 'down_control_z', 'left_control_x', 'left_control_y', 'left_control_z',
                    'right_control_x', 'right_control_y', 'right_control_z', 'release_press_x', 'release_press_y',
                    'release_press_z', 'di_ban_tunnel_qi_dian_x', 'di_ban_tunnel_qi_dian_y', 'di_ban_tunnel_qi_dian_z',
                    'di_ban_tunnel_zhong_dian_x', 'di_ban_tunnel_zhong_dian_y', 'di_ban_tunnel_zhong_dian_z',
                    'is_mine_ceil_tunnel_midline_x', 'is_mine_ceil_tunnel_midline_y', 'is_mine_ceil_tunnel_midline_z',
                    'di_ban_tunnel_midline_mine_ceil_x', 'di_ban_tunnel_midline_mine_ceil_y',
                    'di_ban_tunnel_midline_mine_ceil_z',
                    'di_ban_tunnel_midline_mine_floor_x', 'di_ban_tunnel_midline_mine_floor_y',
                    'di_ban_tunnel_midline_mine_floor_z',
                    'tunnel_length', 'tunnel_row_numebers', 'tunnel_row_dig_hole_id']
    # list_filter = ['tunnel_name', 'work_face', 'mine_width', 'tunnel_row_numebers']
    resource_class = TunnelProxyResource


# 底板巷层位标高坐标IJ列
@admin.register(di_ban_hang_xiuzheng_ding_ban)
class DiBanHangXZDB_Manager(ImportExportActionModelAdmin):
    list_display = ['di_ban_hang_tunnel', 'di_I_x', 'di_J_Z']
    resource_class = DBHXZDBProxyResource


# 底板巷层位标高坐标xy列
@admin.register(xiu_zheng_hou_meiceng_di_ban)
class XiuZhengHMCDB_Manager(ImportExportActionModelAdmin):
    list_display = ['xiu_zheng_hou_tunnel', 'xiu_zheng_x', 'xiu_zheng_z']
    resource_class = XZHMCDBProxyResource


# 底板巷层位标高坐标AJ AK列
@admin.register(xiu_zheng_mei_ceng_ding_ban)
class XiuZhengMCDB_Manager(ImportExportActionModelAdmin):
    list_display = ['xiu_tunnel', 'Xiu_x', 'xiu_z']
    resource_class = XZMCDBProxyResource


# 处理后的坐标轴（上部分）
@admin.register(ping_mian_zuo_biao_kong_zhi)
class Ping_Mian_Zuo_BKZ(ImportExportActionModelAdmin):
    list_display = ['Chu_li_shang_X', 'Chu_li_shang_Y']
    resource_class = PMZBKZProxyResource


# 处理后的坐标轴（下部分）
@admin.register(ping_mian_zuo_biao_kong_zhi_xia)
class Ping_Mian_Zuo_BKZX(ImportExportActionModelAdmin):
    list_display = ['Chu_li_xia_X', 'Chu_li_xia_Y']
    resource_class = PMZBKZXProxyResource


# 泄压范围坐标
@admin.register(xie_ya_fan_wei)
class Xie_Ya_Fan_Wei(ImportExportActionModelAdmin):
    list_display = ['Xie_ya_x', 'Xie_ya_y']
    resource_class = ProxyResource




