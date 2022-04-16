from .models import *
from import_export import resources


# 工作面
class WorkFaceProxyResource(resources.ModelResource):
    exclude = ['id']

    class Meta:
        model = Work_face


# 巷道管理
class TunnelProxyResource(resources.ModelResource):
    exclude = ['id']

    class Meta:
        model = Tunnel


# 底板巷层位标高坐标IJ列
class DBHXZDBProxyResource(resources.ModelResource):
    exclude = ['id']

    class Meta:
        model = di_ban_hang_xiuzheng_ding_ban


# 底板巷层位标高坐标xy列
class XZHMCDBProxyResource(resources.ModelResource):
    exclude = ['id']

    class Meta:
        model = xiu_zheng_hou_meiceng_di_ban


# 底板巷层位标高坐标AJ AK列
class XZMCDBProxyResource(resources.ModelResource):
    exclude = ['id']

    class Meta:
        model = xiu_zheng_mei_ceng_ding_ban


# 处理后的坐标轴（上部分）
class PMZBKZProxyResource(resources.ModelResource):
    exclude = ['id']

    class Meta:
        model = ping_mian_zuo_biao_kong_zhi


# 处理后的坐标轴（下部分）
class PMZBKZXProxyResource(resources.ModelResource):
    exclude = ['id']

    class Meta:
        model = ping_mian_zuo_biao_kong_zhi_xia


# 泄压范围坐标
class ProxyResource(resources.ModelResource):
    exclude = ['id']

    class Meta:
        model = xie_ya_fan_wei
