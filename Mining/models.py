import logging

from django.db import models

# Create your models here.
from django.utils import timezone


class Company(models.Model):
    c_name = models.CharField(max_length=30, verbose_name="公司名称")  # 公司名

    class Meta:
        db_table = "Company"
        verbose_name = "公司管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"Company：{self.c_name}"


class Mine(models.Model):
    m_name = models.CharField(max_length=30, verbose_name="煤矿名称")  # 矿的名字
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="所属公司")  # 关连Company

    class Meta:
        db_table = 'Mine'
        verbose_name = "煤矿管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"Mine:{self.m_name}"


class user_group(models.Model):
    # 用户分组的键值对
    worker = '0'
    operator = '1'
    superadmin = '2'
    usergroup = ((worker, 'worker'), (operator, 'operator'), (superadmin, 'superadmin'))
    username = models.CharField(max_length=12, verbose_name="用户名")  # 账号
    userpwd = models.CharField(max_length=20, verbose_name="用户密码")  # 账号密码
    # 新增字段，用户属于哪个矿区
    belongMine = models.ForeignKey(Mine, on_delete=models.CASCADE, verbose_name="所属矿区")
    usertype = models.CharField(max_length=20, choices=usergroup, default=worker, verbose_name="用户身份类别")  # 用户身份类别，默认为工人

    class Meta:
        db_table = "user_group"
        verbose_name = "用户管理"
        verbose_name_plural = verbose_name


class Work_face(models.Model):  # 以下数据全部需要提前录入
    mine = models.ForeignKey(Mine, on_delete=models.CASCADE, verbose_name="所属煤矿")  # 关联Mine
    odd_even_column_distance = models.FloatField(max_length=10, null=True, blank=True, default=3,
                                                 verbose_name="设计奇偶列间距")  # 设计奇偶列间距（九里山矿默认为3米）
    w_name = models.CharField(max_length=30, null=True, blank=True, verbose_name="工作面的名字")  # 工作面的名字
    chuan_ding_length = models.CharField(max_length=10, null=True, blank=True, verbose_name="穿顶长度")  # 穿顶长度
    chong_mei_standard = models.CharField(max_length=10, null=True, blank=True, verbose_name="冲煤标准")  # 冲煤标准
    distance_of_coal_rock_tunnel = models.FloatField(max_length=10, null=True, blank=True,
                                                     verbose_name="煤岩巷间距")  # 煤岩巷间距
    change_of_coal_rock = models.CharField(max_length=30, null=True, blank=True, verbose_name="煤岩变化")  # 煤岩变化
    with_of_coal_roadway = models.FloatField(max_length=10, null=True, blank=True, verbose_name="煤巷宽度")  # 煤巷宽度
    control_range_of_final_hole_to_meet = models.FloatField(max_length=30, null=True, blank=True,
                                                            verbose_name="终孔见煤控制范围")  # 终孔见煤控制范围
    drivage_distance = models.FloatField(max_length=10, null=True, blank=True, verbose_name="设计掘进间距")  # 设计掘进间距
    recovery_distance = models.FloatField(max_length=10, null=True, blank=True, verbose_name="设计回采间距")  # 设计回采间距
    up_tunnel_up = models.FloatField(max_length=10, null=True, blank=True, verbose_name="上部底板巷上巷内错距离")  # 上部底板巷上巷内错距离
    down_tunnel_tunnel = models.FloatField(max_length=10, null=True, blank=True,
                                           verbose_name="下部底板巷与下巷内错距离")  # 下部底板巷与下巷内错距离
    qie_yan_qie = models.FloatField(max_length=10, null=True, blank=True,
                                    verbose_name="切眼底板巷与切眼巷道内错距离")  # 切眼底板巷与切眼巷道内错距离
    # 下面是之前从矿级别添加过来的7个字段
    drainage_radius = models.FloatField(max_length=10, null=True, blank=True, verbose_name="抽采半径")  # 抽采半径
    thickness_of_pinch_coal = models.FloatField(max_length=10, null=True, blank=True, verbose_name="尖灭煤厚")  # 尖灭煤厚
    over_flush_coefficient = models.FloatField(max_length=10, null=True, blank=True, verbose_name="超冲系数")  # 超冲系数
    volume_weight_of_coal = models.FloatField(max_length=10, null=True, blank=True, verbose_name="煤体容量")  # 煤体容量
    coal_ultra_thick_divided = models.FloatField(max_length=10, null=True, blank=True, verbose_name="煤厚超大划分")  # 煤厚超大划分
    # 下面这两个字段数据是否合法、是否修改，还要看后期算法的具体实现过程
    borehole_segmentation_standard1 = models.CharField(max_length=30, null=True, blank=True,
                                                       verbose_name="煤孔分割标准1")  # 煤孔分割标准1
    borehole_segmentation_standard2 = models.CharField(max_length=30, null=True, blank=True,
                                                       verbose_name="煤孔分割标准2")  # 煤孔分割标准2

    class Meta:
        db_table = 'work_face'
        verbose_name = "工作面管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.w_name


class Word(models.Model):  # 将word中的数据直接读取并保存到数据库中
    work_face_name = models.CharField(max_length=30, null=True, blank=True)  # 工作面的名称
    tunnel_name = models.CharField(max_length=30, null=True, blank=True)  # 巷道名称
    position = models.FloatField(max_length=10, null=True, blank=True)  # 位置
    q = models.FloatField(max_length=10, null=True, blank=True)
    s = models.FloatField(max_length=10, null=True, blank=True)
    h2 = models.FloatField(max_length=10, null=True, blank=True)
    gas_emission = models.FloatField(max_length=10, null=True, blank=True)  # 瓦斯涌出
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # 日期
    Air_volume = models.FloatField(max_length=10, null=True, blank=True)  # 风量
    Return_air_concentration = models.FloatField(max_length=10, null=True, blank=True)  # 回风浓度
    check_person_name = models.CharField(max_length=30, null=True, blank=True)  # 验证人员姓名
    mine_depth = models.FloatField(max_length=10, null=True, blank=True)  # 煤厚

    class Meta:
        db_table = 'word'


class Tunnel(models.Model):  # 巷道表
    work_face = models.ForeignKey(Work_face, on_delete=models.CASCADE, verbose_name='所属工作面')  # 关联Work_face
    tunnel_name = models.CharField(max_length=30, verbose_name='巷道名')  # 巷道名
    mine_width = models.FloatField(max_length=10, null=True, blank=True, verbose_name='煤巷宽度')  # 煤巷宽度
    mine_hight = models.FloatField(max_length=10, null=True, blank=True, verbose_name='煤巷高度')  # 煤巷高度
    di_ban_hang = models.FloatField(max_length=10, null=True, blank=True, verbose_name='底板巷宽度')  # 底板巷宽度
    mei_ceng_qing_jiao = models.FloatField(max_length=10, null=True, blank=True, verbose_name='煤层倾角')  # 煤层倾角
    tunnel_first_hole_number = models.CharField(max_length=10, null=True, blank=True, verbose_name='首个钻孔号')  # 首个钻孔号
    arch_radius = models.FloatField(max_length=10, null=True, blank=True, verbose_name='拱形半径')  # 拱形半径
    zuan_kong_chui_ju = models.FloatField(max_length=10, null=True, blank=True, verbose_name='钻孔垂距')  # 钻孔垂距
    hole_height = models.FloatField(max_length=10, null=True, blank=True, verbose_name='开孔高度')  # 开孔高度
    # --------------------------------------------------
    di_ban_hang_hight = models.FloatField(max_length=10, null=True, blank=True, verbose_name='底板巷高度')  # 底板巷高度
    tunnel_actual_row_gap = models.FloatField(max_length=10, null=True, blank=True, verbose_name='巷道实际排间距')  # 巷道实际排间距

    up_control_x = models.FloatField(max_length=10, null=True, blank=True, verbose_name='上部控制范围x')  # 上部控制范围x
    up_control_y = models.FloatField(max_length=10, null=True, blank=True, verbose_name='上部控制范围y')  # 上部控制范围y
    up_control_z = models.FloatField(max_length=10, null=True, blank=True, verbose_name='上部控制范围z，设置为空')  # 上部控制范围z，设置为空

    down_control_x = models.FloatField(max_length=10, null=True, blank=True, verbose_name='下部控制范围x')  # 下部控制范围x
    down_control_y = models.FloatField(max_length=10, null=True, blank=True, verbose_name='下部控制范围y')  # 下部控制范围y
    down_control_z = models.FloatField(max_length=10, null=True, blank=True, verbose_name='下部控制范围Z设置为空')  # 下部控制范围Z设置为空

    left_control_x = models.FloatField(max_length=10, null=True, blank=True, verbose_name='左侧控制范围x')  # 左侧控制范围x
    left_control_y = models.FloatField(max_length=10, null=True, blank=True, verbose_name='左侧控制范围y')  # 左侧控制范围y
    left_control_z = models.FloatField(max_length=10, null=True, blank=True, verbose_name="左侧控制范围z设置为空")  # 左侧控制范围z设置为空

    right_control_x = models.FloatField(max_length=10, null=True, blank=True, verbose_name='右侧控制范围x')  # 右侧控制范围x
    right_control_y = models.FloatField(max_length=10, null=True, blank=True, verbose_name='右侧控制范围y')  # 右侧控制范围y
    right_control_z = models.FloatField(max_length=10, null=True, blank=True, verbose_name='右侧控制范围z设置为空')  # 右侧控制范围z设置为空

    release_press_x = models.FloatField(max_length=10, null=True, blank=True, verbose_name='泄压范围坐标x')  # 泄压范围坐标x
    release_press_y = models.FloatField(max_length=10, null=True, blank=True, verbose_name='泄压范围坐标y')  # 泄压范围坐标y
    release_press_z = models.FloatField(max_length=10, null=True, blank=True, verbose_name='泄压范围坐标z设置为空')  # 泄压范围坐标z设置为空

    # ### _______________________________________________________________
    di_ban_tunnel_qi_dian_x = models.FloatField(max_length=10, null=True, blank=True,
                                                verbose_name='底板巷底板中心线起点坐标x')  # 底板巷底板中心线起点坐标x
    di_ban_tunnel_qi_dian_y = models.FloatField(max_length=10, null=True, blank=True,
                                                verbose_name='底板巷底板中心线起坐标y')  # 底板巷底板中心线起坐标y
    di_ban_tunnel_qi_dian_z = models.FloatField(max_length=10, null=True, blank=True,
                                                verbose_name='底板巷底板中心线起点坐标z设置为空')  # 底板巷底板中心线起点坐标z设置为空

    di_ban_tunnel_zhong_dian_x = models.FloatField(max_length=10, null=True, blank=True,
                                                   verbose_name='底板巷底板中心线终点坐标x')  # 底板巷底板中心线终点坐标x
    di_ban_tunnel_zhong_dian_y = models.FloatField(max_length=10, null=True, blank=True,
                                                   verbose_name='底板巷底板中心线终点坐标y')  # 底板巷底板中心线终点坐标y
    di_ban_tunnel_zhong_dian_z = models.FloatField(max_length=10, null=True, blank=True,
                                                   verbose_name='底板巷底板中心线终点坐标z  设置为空')  # 底板巷底板中心线终点坐标z  设置为空

    is_mine_ceil_tunnel_midline_x = models.FloatField(max_length=10, null=True, blank=True,
                                                      verbose_name='被掩护煤巷顶板中心线起止及折线点坐标x')  # 被掩护煤巷顶板中心线起止及折线点坐标x
    is_mine_ceil_tunnel_midline_y = models.FloatField(max_length=10, null=True, blank=True,
                                                      verbose_name='被掩护煤巷顶板中心线起止及折线点坐标y')  # 被掩护煤巷顶板中心线起止及折线点坐标y
    is_mine_ceil_tunnel_midline_z = models.FloatField(max_length=10, null=True, blank=True,
                                                      verbose_name='被掩护煤巷顶板中心线起止及折线点坐标z')  # 被掩护煤巷顶板中心线起止及折线点坐标z 设置为空

    di_ban_tunnel_midline_mine_ceil_x = models.FloatField(max_length=10, null=True, blank=True,
                                                          verbose_name='底板巷中心线煤层顶板起止及折线点坐标x')  # 底板巷中心线煤层顶板起止及折线点坐标x
    di_ban_tunnel_midline_mine_ceil_y = models.FloatField(max_length=10, null=True, blank=True,
                                                          verbose_name='底板巷中心线煤层顶板起止及折线点坐标y')  # 底板巷中心线煤层顶板起止及折线点坐标y
    di_ban_tunnel_midline_mine_ceil_z = models.FloatField(max_length=10, null=True, blank=True,
                                                          verbose_name='底板巷中心线煤层顶板起止及折线点坐标z')  # 底板巷中心线煤层顶板起止及折线点坐标z

    di_ban_tunnel_midline_mine_floor_x = models.FloatField(max_length=10, null=True, blank=True,
                                                           verbose_name='底板巷中心线煤层底板起止及折线点坐标x')  # 底板巷中心线煤层底板起止及折线点坐标x
    di_ban_tunnel_midline_mine_floor_y = models.FloatField(max_length=10, null=True, blank=True,
                                                           verbose_name='底板巷中心线煤层底板起止及折线点坐标y')  # 底板巷中心线煤层底板起止及折线点坐标y
    di_ban_tunnel_midline_mine_floor_z = models.FloatField(max_length=10, null=True, blank=True,
                                                           verbose_name='底板巷中心线煤层底板起止及折线点坐标z')  # 底板巷中心线煤层底板起止及折线点坐标z

    tunnel_length = models.FloatField(max_length=10, null=True, blank=True, verbose_name='巷道长')  # 巷道长
    tunnel_row_numebers = models.FloatField(max_length=10, null=True, blank=True, verbose_name='巷道总排数')  # 巷道总排数
    tunnel_row_dig_hole_id = models.FloatField(max_length=10, null=True, blank=True, verbose_name='巷道排钻孔编号')  # 巷道排钻孔编号

    class Meta:
        db_table = 'tunnel'
        verbose_name = "巷道管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tunnel_name


class xiu_zheng_mei_ceng_ding_ban(models.Model):  # 修正后煤层顶板坐标表
    xiu_tunnel = models.ForeignKey(Tunnel, on_delete=models.CASCADE, verbose_name="巷道号")
    Xiu_x = models.FloatField(max_length=30, null=True, blank=True, verbose_name="修正X坐标")
    xiu_z = models.FloatField(max_length=30, null=True, blank=True, verbose_name="修正Y坐标")

    class Meta:
        db_table = 'xiu_zheng_mei_ceng_ding_ban'
        verbose_name = "修正后煤层顶板坐标表"
        verbose_name_plural = verbose_name


# 底板巷道顶板坐标表
class di_ban_hang_xiuzheng_ding_ban(models.Model):
    di_ban_hang_tunnel = models.ForeignKey(Tunnel, on_delete=models.CASCADE, verbose_name="巷道号")
    di_I_x = models.FloatField(max_length=30, null=True, blank=True, verbose_name="底板巷道顶板坐标X")
    di_J_Z = models.FloatField(max_length=30, null=True, blank=True, verbose_name="底板巷道顶板坐标Y")

    class Meta:
        db_table = 'di_ban_hang_xiuzheng_ding_ban'
        verbose_name = "底板巷道顶板坐标表"
        verbose_name_plural = verbose_name


class xiu_zheng_hou_meiceng_di_ban(models.Model):  # 修正后煤层底板坐标表
    xiu_zheng_hou_tunnel = models.ForeignKey(Tunnel, on_delete=models.CASCADE, verbose_name="巷道号")
    xiu_zheng_x = models.FloatField(max_length=30, null=True, blank=True, verbose_name="修正后煤层底板坐标X")
    xiu_zheng_z = models.FloatField(max_length=30, null=True, blank=True, verbose_name="修正后煤层底板坐标Z")

    class Meta:
        db_table = 'xiu_zheng_hou_meiceng_di_ban'
        verbose_name = "修正后煤层底板坐标表"
        verbose_name_plural = verbose_name


class Rock_pillar_thickness(models.Model):  # 岩柱厚度表
    tunnel_rock = models.ForeignKey(Tunnel, on_delete=models.CASCADE, verbose_name="巷道号")  # 关联巷道的外键
    thickness_x = models.FloatField(max_length=10, null=True, blank=True, verbose_name="岩柱厚度所对应的x坐标点")  # 岩柱厚度所对应的x坐标点
    thickness = models.FloatField(max_length=10, null=True, blank=True, verbose_name="岩柱厚度")  # 岩柱厚度

    class Meta:
        db_table = "rock_pillar_thickness"
        verbose_name = "岩柱厚度表"
        verbose_name_plural = verbose_name


class Tunnel_Coal_Dip_Angle(models.Model):  # 巷道煤层倾角表
    tunnel_coal_dip_angle_tunnel = models.ForeignKey(Tunnel, on_delete=models.CASCADE)  # 关联巷道表
    group_type = models.CharField(max_length=30, null=True, blank=True)  # 组别J1-15,16-93,通过组名选择煤层倾角
    dip_angle = models.FloatField(max_length=10, null=True, blank=True)  # 煤层倾角，先通过组名选择，然后将选择的倾角保存到数据库中
    duan_ceng_length = models.FloatField(max_length=10, null=True, blank=True)  # 断层平距

    class Meta:
        db_table = 'tunnel_coal_dig_angle'
        verbose_name = "巷道煤层倾角表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.group_type


class Di_Ban_Tunnel_Tun_Kuo(models.Model):  # 底板巷轮廓坐标表
    di_ban_tunnel_row = models.ForeignKey(Tunnel, on_delete=models.CASCADE)  # 关联巷道
    di_ban_tunnel_lun_kuo_x = models.FloatField(max_length=10, null=True, blank=True)  # 底板巷巷道轮廓坐标x
    di_ban_tunnel_lun_kuo_y = models.FloatField(max_length=10, null=True, blank=True)  # 底板巷巷道轮廓坐标y
    di_ban_tunnel_lun_kuo_z = models.FloatField(max_length=10, null=True, blank=True)  # 底板巷巷道轮廓坐标z

    class Meta:
        db_table = 'di_ban_tunnel_lun_kuo'
        verbose_name = '底板巷轮廓坐标表'
        verbose_name_plural = verbose_name


class Row(models.Model):  # 排号管理
    tunnel = models.ForeignKey(Tunnel, on_delete=models.CASCADE, verbose_name="所属巷道")  # 关联Tunnel
    row_id = models.CharField(max_length=30, null=True, blank=True, verbose_name='排号')  # 排号,这个是char是因为J1-15,16-94
    mei_qing_jiao = models.FloatField(max_length=10, null=True, blank=True, verbose_name='单排煤层倾角')  # 单排煤层倾角
    current_tunnel_depth = models.FloatField(max_length=10, null=True, blank=True, verbose_name='当前排的巷道深度')  # 当前排的巷道深度
    row_x = models.FloatField(max_length=10, editable=False, null=True, blank=True, verbose_name='排x坐标')  # 排x坐标=控制范围x
    row_y = models.FloatField(max_length=10, editable=False, null=True, blank=True, verbose_name="排y坐标")  # 排y坐标
    row_z = models.FloatField(max_length=10, editable=False, null=True, blank=True, verbose_name='排z坐标')  # 排z坐标
    pillar_thickness = models.FloatField(max_length=10, editable=False, null=True, blank=True,
                                         verbose_name='岩柱厚度')  # 岩柱厚度
    coal_seam_thickness = models.FloatField(max_length=10, editable=False, null=True, blank=True,
                                            verbose_name='煤层厚度')  # 煤层厚度
    left_number = models.FloatField(max_length=10, editable=False, null=True, blank=True,
                                    verbose_name='左侧最新孔号')  # 左侧最新孔号
    right_number = models.FloatField(max_length=10, editable=False, null=True, blank=True,
                                     verbose_name='右侧最新孔号')  # 右侧最新孔号

    class Meta:
        db_table = 'row'
        verbose_name = "排管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.row_id

    # 重写save方法
    def save(self, *args, **kwargs):
        row_id = self.row_id
        tunnel_name = self.tunnel.tunnel_name
        current_tunnel_depth = self.current_tunnel_depth
        hole_number = self.tunnel.tunnel_first_hole_number
        logging.INFO = "row_id=" + row_id
        logging.INFO = "tunnel_name" + tunnel_name
        if row_id is not None and tunnel_name is not None:
            print(self.tunnel)
            arch_radius = self.tunnel.arch_radius
            work_face_id = self.tunnel.work_face
            tunnel_first_hole_number = self.tunnel.tunnel_first_hole_number  # 首孔号
            qi_dian_x = self.tunnel.di_ban_tunnel_qi_dian_x  # 起点坐标
            qi_dian_y = self.tunnel.di_ban_tunnel_qi_dian_y
            zhong_dian_x = self.tunnel.di_ban_tunnel_zhong_dian_x  # 终点坐标
            zhong_dian_y = self.tunnel.di_ban_tunnel_zhong_dian_y
            tunnel_length = self.tunnel.tunnel_length
            row_x = round(qi_dian_x + (current_tunnel_depth / tunnel_length) * (zhong_dian_x - qi_dian_x), 2)
            row_y = round(qi_dian_y + (current_tunnel_depth / tunnel_length) * (zhong_dian_y - qi_dian_y), 2)
            data1 = list(di_ban_hang_xiuzheng_ding_ban.objects.filter().all().values_list('di_I_x', 'di_J_Z'))
            data2 = list(xiu_zheng_mei_ceng_ding_ban.objects.filter().all().values_list('Xiu_x', 'xiu_z'))
            data3 = list(
                xiu_zheng_hou_meiceng_di_ban.objects.filter().all().values_list('xiu_zheng_x', 'xiu_zheng_z'))
            if row_x < data1[0][0] or row_x > data1[-1][0]:
                print('不在修正底板巷范围内！')
            elif row_x < data2[0][0] or row_x > data2[-1][0]:
                print('不在修正煤顶范围内！')
            elif row_x < data3[0][0] or row_x > data3[-1][0]:
                print('不在修正煤底范围内！')
            else:
                # 1:底板巷修正后顶板坐标
                x_1_hang, x_2_hang, z_1_hang, z_2_hang = None, None, None, None
                for data in data1:
                    if (data[0] <= row_x):
                        x_1_hang = data[0]
                        z_1_hang = data[1]
                    else:
                        if x_2_hang is None:
                            x_2_hang = data[0]
                        if z_2_hang is None:
                            z_2_hang = data[1]
                # x_1_hang = data1[data1[:, 0] <= row_x].tail(1).iloc[0, 0]
                # x_2_hang = data1[data1[:, 0] > row_x].head(1).iloc[0, 0]
                # z_1_hang = data1[data1[:, 0] <= row_x].tail(1).iloc[0, 1]
                # z_2_hang = data1[data1[:, 0] > row_x].head(1).iloc[0, 1]
                # 2：修正后煤层顶板坐标
                x_1_ding, x_2_ding, z_1_ding, z_2_ding = None, None, None, None
                for data in data2:
                    if (data[0] <= row_x):
                        x_1_ding = data[0]
                        z_1_ding = data[1]
                    else:
                        if x_2_ding is None:
                            x_2_ding = data[0]
                        if z_2_ding is None:
                            z_2_ding = data[1]
                # x_1_ding = data2[data2.iloc[:, 0] <= row_x].tail(1).iloc[0, 0]
                # x_2_ding = data2[data2.iloc[:, 0] > row_x].head(1).iloc[0, 0]
                # z_1_ding = data2[data2.iloc[:, 0] <= row_x].tail(1).iloc[0, 1]
                # z_2_ding = data2[data2.iloc[:, 0] > row_x].head(1).iloc[0, 1]
                # 3：修正后煤层底板坐标
                x_1_di, x_2_di, z_1_di, z_2_di = None, None, None, None
                for data in data3:
                    if (data[0] <= row_x):
                        x_1_di = data[0]
                        z_1_di = data[1]
                    else:
                        if x_2_di is None:
                            x_2_di = data[0]
                        if z_2_di is None:
                            z_2_di = data[1]
                # x_1_di = data3[data3.iloc[:, 0] <= row_x].tail(1).iloc[0, 0]
                # x_2_di = data3[data3.iloc[:, 0] > row_x].head(1).iloc[0, 0]
                # z_1_di = data3[data3.iloc[:, 0] <= row_x].tail(1).iloc[0, 1]
                # z_2_di = data3[data3.iloc[:, 0] > row_x].head(1).iloc[0, 1]
                di_ban_hang_hight = self.tunnel.di_ban_hang_hight
                qi_dian_x = self.tunnel.di_ban_tunnel_qi_dian_x  # 起点坐标
                qi_dian_y = self.tunnel.di_ban_tunnel_qi_dian_y
                zhong_dian_x = self.tunnel.di_ban_tunnel_zhong_dian_x  # 终点坐标
                zhong_dian_y = self.tunnel.di_ban_tunnel_zhong_dian_y
                design_hole_height = 1.2
                z_hang = z_1_hang + (z_2_hang - z_1_hang) * (row_x - x_1_hang) / (x_2_hang - x_1_hang)
                z_ding = z_1_ding + (z_2_ding - z_1_ding) * (row_x - x_1_ding) / (x_2_ding - x_1_ding)
                z_di = z_1_di + (z_2_di - z_1_di) * (row_x - x_1_di) / (x_2_di - x_1_di)
                #   求z坐标 z巷 - 3.3(底板巷巷道高度) +1.2
                z = round(z_hang - di_ban_hang_hight + design_hole_height, 2)
                #   求岩柱厚度
                pillar_thickness = round(z_di - z_hang, 2)
                #   求煤层厚度
                coal_seam_thickness = round(z_ding - z_di, 2)
                self.row_x = row_x
                self.row_y = row_y
                self.row_z = z
                self.coal_seam_thickness = coal_seam_thickness
                self.pillar_thickness = pillar_thickness
                #   求岩柱厚度
                rock_section = pillar_thickness
                #   求煤层厚度
                coal_section = coal_seam_thickness
                see_ceil = coal_section + rock_section
                chuan_ding_length = self.tunnel.work_face.chuan_ding_length
                hole_depth = see_ceil + float(chuan_ding_length)
                design_elevation_angel = 90  # 首孔仰角
                deflection_angle = 0  # 设计偏角
                single_row = 2
                chong_mei_standard = float(self.tunnel.work_face.chong_mei_standard)
                weight_of_flush_coal = round(coal_section * chong_mei_standard, 2)
                super(Row, self).save(*args, **kwargs)
                design_elevation_angel = 90  # 首孔仰角
                my_record = Hole_Design(hole_number=self.tunnel.tunnel_first_hole_number,
                                        design_hole_height=design_hole_height,
                                        deflection_angle=deflection_angle,
                                        design_elevation_angel=90,  # 首孔仰角
                                        rock_section=rock_section,
                                        coal_section=coal_section,
                                        see_ceil=see_ceil,
                                        hole_depth=hole_depth,
                                        single_row=single_row, isFirstHole='0', row_id=self.id, weight_of_flush_coal = weight_of_flush_coal)
                # 保存首孔信息
                my_record.save()


class Every_Row_Con_Id(models.Model):  # 每排钻孔编号及编号次序表
    row_every = models.ForeignKey(Row, on_delete=models.CASCADE)  # 关联排，通过外键关系就可以查找row数据表中的详细信息，比如排号之类的
    number_order = models.CharField(max_length=256)  # 每排编号次序

    class Mata:
        db_table = 'every_row_con_id'
        verbose_name = '每排钻孔编号及编号次序表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.number_order


class Gas_content_diagram(models.Model):  # 每个孔的瓦斯含量表
    row_gas = models.ForeignKey(Row, on_delete=models.CASCADE)  # 关联的是哪一个巷道下具体的哪一排
    hole_number = models.CharField(max_length=30, null=True, blank=True)  # 孔号,因为不知道孔号是数字类型的还是字符类型的，所以最好还是存储为字符类型
    position_gas = models.FloatField(max_length=10, null=True, blank=True)  # 位置
    deflection_angle_construction = models.FloatField(max_length=10, null=True, blank=True)  # 偏角
    elevation_angle_construction = models.FloatField(max_length=10, null=True, blank=True)  # 仰角
    see_coal = models.FloatField(max_length=10, null=True, blank=True)  # 见煤深度
    sampling_depth = models.FloatField(max_length=10, null=True, blank=True)  # 取样深度
    see_ceil = models.FloatField(max_length=10, null=True, blank=True)  # 见顶深度
    gas_content = models.FloatField(max_length=10, null=True, blank=True)  # 瓦斯含量
    gas_press = models.FloatField(max_length=10, null=True, blank=True)  # 瓦斯压力
    construction_name = models.CharField(max_length=30, null=True, blank=True)  # 施工人姓名
    sampling_name = models.CharField(max_length=30, null=True, blank=True)  # 取样人姓名
    problem_position = models.FloatField(max_length=10, null=True, blank=True)  # 异常位置
    problem_situation = models.CharField(max_length=256, null=True, blank=True)  # 异常情况

    class Meta:
        db_table = 'gas_content_diagram'

    def __str__(self):
        return f"gas_content_diagram:{self.gas_content}"  # 瓦斯含量


class Hole_Design(models.Model):  # 设计孔
    row = models.ForeignKey(Row, on_delete=models.CASCADE)  # 关联Row
    hole_number = models.CharField(max_length=30)  # 孔号，由系统自动根据排序列出
    # -----------------------------------------------------------------
    design_hole_height = models.FloatField(max_length=10, null=True, blank=True, default=1.2)  # 设计开孔高度
    single_row = models.FloatField(max_length=10, null=True, blank=True)  # 单排列数
    # -----------------------------------------------------------------
    deflection_angle = models.FloatField(max_length=10, null=True, blank=True)  # 设计偏角
    design_elevation_angel = models.FloatField(max_length=10, null=True, blank=True)  # 设计仰角
    rock_section = models.FloatField(max_length=10, null=True, blank=True)  # 设计岩段 = 设计见煤
    coal_section = models.FloatField(max_length=10, null=True, blank=True)  # 设计煤段
    see_ceil = models.FloatField(max_length=10, null=True, blank=True)  # 设计见顶
    hole_depth = models.FloatField(max_length=10, null=True, blank=True)  # 设计孔深
    weight_of_flush_coal = models.FloatField(max_length=10, null=True, blank=True)  # 设计冲煤量
    isFirstHole = models.CharField(max_length=10, null=False, blank=False, default="1")  # 是否是首孔 0为首孔，1为非首孔
    currentHoleFlag = models.CharField(max_length=10, null=False, blank=False, default="0")  # 当前孔标记字段 0为当前孔, 1为非当前孔
    isNext = models.CharField(max_length=10, null=False, blank=False, default="1")  # 下一个空标记字段 0为下一个孔, 1为非下一个孔
    status = models.CharField(max_length=10, null=False, blank=False, default="-1")  # 当前孔状态, -1为待申请，0为审批未通过，1为审批通过，2为驳回
    desc = models.CharField(max_length=50, null=True, blank=True)  # 状态描述
    reason = models.CharField(max_length=50, null=True, blank=True)  # 驳回原因描述
    class Meta:
        db_table = 'hole_design'

    def __str__(self):
        return f"hole_design:{self.design_hole_height}"


class Hole_Design_Ping_Mian(models.Model):  # 设计单孔平面图坐标
    hole_number = models.ForeignKey(Hole_Design, on_delete=models.CASCADE)
    design_jian_mei_x = models.FloatField(max_length=10, null=True, blank=True)  # 设计见煤平面坐标x
    design_jian_mei_y = models.FloatField(max_length=10, null=True, blank=True)  # 设计见煤平面坐标y
    design_jian_mei_z = models.FloatField(max_length=10, null=True, blank=True)  # 设计见煤平面坐标z

    design_jian_ding_x = models.FloatField(max_length=10, null=True, blank=True)  # 设计见顶平面坐标x
    design_jian_ding_y = models.FloatField(max_length=10, null=True, blank=True)  # 设计见顶平面坐标y
    design_jian_ding_z = models.FloatField(max_length=10, null=True, blank=True)  # 设计见顶平面坐标z

    design_zhong_kong_x = models.FloatField(max_length=10, null=True, blank=True)  # 设计终孔平面坐标x
    design_zhong_kong_y = models.FloatField(max_length=10, null=True, blank=True)  # 设计终孔平面坐标y
    design_zhong_kong_z = models.FloatField(max_length=10, null=True, blank=True)  # 设计终孔平面坐标z

    kai_kong_ping_x = models.FloatField(max_length=10, null=True, blank=True)  # 设计开孔平面坐标x
    kai_kong_ping_y = models.FloatField(max_length=10, null=True, blank=True)  # 设计开孔平面坐标y
    kai_kong_ping_z = models.FloatField(max_length=10, null=True, blank=True)  # 设计开孔平面坐标z

    class Meta:
        db_table = 'Hole_Design_Ping_Mian'

    def __str__(self):
        return f"Hole_Design_Ping_Mian:{self.hole_number}"


class Hole_Design_Pou_Mian(models.Model):  # 设计单孔平剖面图坐标
    hole_number = models.ForeignKey(Hole_Design, on_delete=models.CASCADE)
    design_jian_mei_x = models.FloatField(max_length=10, null=True, blank=True)  # 设计见煤剖面坐标x
    design_jian_mei_y = models.FloatField(max_length=10, null=True, blank=True)  # 设计见煤剖面坐标y
    design_jian_mei_z = models.FloatField(max_length=10, null=True, blank=True)  # 设计见煤剖面坐标z

    design_jian_ding_x = models.FloatField(max_length=10, null=True, blank=True)  # 设计见顶剖面坐标x
    design_jian_ding_y = models.FloatField(max_length=10, null=True, blank=True)  # 设计见顶剖面坐标y
    design_jian_ding_z = models.FloatField(max_length=10, null=True, blank=True)  # 设计见顶剖面坐标z

    design_zhong_kong_x = models.FloatField(max_length=10, null=True, blank=True)  # 设计终孔剖面坐标x
    design_zhong_kong_y = models.FloatField(max_length=10, null=True, blank=True)  # 设计终孔剖面坐标y
    design_zhong_kong_z = models.FloatField(max_length=10, null=True, blank=True)  # 设计终孔平面坐标z

    kai_kong_pou_x = models.FloatField(max_length=10, null=True, blank=True)  # 设计开孔剖面坐标x
    kai_kong_pou_y = models.FloatField(max_length=10, null=True, blank=True)  # 设计开孔剖面坐标y
    kai_kong_pou_z = models.FloatField(max_length=10, null=True, blank=True)  # 设计开孔剖面坐标z

    class Meta:
        db_table = 'Hole_Design_Pou_Mian'

    def __str__(self):
        return f"Hole_Design_Pou_Mian:{self.hole_number}"


#   新增表*********
class Hole_Design_Pou_Mian_Cad(models.Model):  # 设计单孔平剖面图坐标
    hole_number = models.ForeignKey(Hole_Design, on_delete=models.CASCADE)
    design_jian_mei_cad_x = models.FloatField(max_length=10, null=True, blank=True)  # 设计见煤剖面坐标cad_x
    design_jian_mei_cad_y = models.FloatField(max_length=10, null=True, blank=True)  # 设计见煤剖面坐标cad_y
    design_jian_mei_cad_z = models.FloatField(max_length=10, null=True, blank=True)  # 设计见煤剖面坐标cad_z

    design_jian_ding_cad_x = models.FloatField(max_length=10, null=True, blank=True)  # 设计见顶剖面坐标cad_x
    design_jian_ding_cad_y = models.FloatField(max_length=10, null=True, blank=True)  # 设计见顶剖面坐标cad_y
    design_jian_ding_cad_z = models.FloatField(max_length=10, null=True, blank=True)  # 设计见顶剖面坐标cad_z

    design_zhong_kong_cad_x = models.FloatField(max_length=10, null=True, blank=True)  # 设计终孔剖面坐标cad_x
    design_zhong_kong_cad_y = models.FloatField(max_length=10, null=True, blank=True)  # 设计终孔剖面坐标cad_y
    design_zhong_kong_cad_z = models.FloatField(max_length=10, null=True, blank=True)  # 设计终孔平面坐标cad_z

    design_kai_kong_pou_cad_x = models.FloatField(max_length=10, null=True, blank=True)  # 设计开孔剖面坐标cad_x     ******
    design_kai_kong_pou_cad_y = models.FloatField(max_length=10, null=True, blank=True)  # 设计开孔剖面坐标cad_y     ******
    design_kai_kong_pou_cad_z = models.FloatField(max_length=10, null=True, blank=True)  # 设计开孔剖面坐标cad_z     ******

    class Meta:
        db_table = 'Hole_Design_Pou_Mian_Cad'

    def __str__(self):
        return f"Hole_Design_Pou_Mian_Cad:{self.hole_number}"


class Hole_Construction(models.Model):  # 施工孔
    row = models.ForeignKey(Row, on_delete=models.CASCADE)  # 关联Row
    h_c_number = models.CharField(max_length=30)  # 孔号由系统自动根据排序列出
    hole_height = models.FloatField(max_length=10, null=True, blank=True)  # 开孔高度
    video_number = models.CharField(max_length=30, null=True, blank=True)  # 视频编号，这个还是不知道存储类型，所以就只接存储为字符类型
    time = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # 施工时间
    r_deflection_angle = models.FloatField(max_length=10, null=True, blank=True)  # 钻孔复核偏角
    r_elevation_angle = models.FloatField(max_length=10, null=True, blank=True)  # 钻孔复核仰角
    con_see_coal = models.FloatField(max_length=10, null=True, blank=True)  # 施工见煤
    con_see_ceil = models.FloatField(max_length=10, null=True, blank=True)  # 施工见顶
    con_hole_depth = models.FloatField(max_length=30, null=True, blank=True)  # 施工孔深
    remove_drill_start = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # 退钻开始时间
    remove_drill_end = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # 退钻结束时间
    construction_person_name = models.CharField(max_length=30, null=True, blank=True)  # 施工负责人姓名，手写板签字
    text_person = models.CharField(max_length=30, null=True, blank=True)  # 验收人员，手写板签字
    charge_person = models.CharField(max_length=30, null=True, blank=True)  # 值班人员，手写板签字
    drill_eval = models.CharField(max_length=30, null=True, blank=True)  # 钻孔评价，手写板签字
    hole_diameter = models.FloatField(max_length=10, null=True, blank=True)  # 孔径
    drill_depth = models.FloatField(max_length=10, null=True, blank=True)  # 当班钻进深度

    ab_hole_depth_position = models.FloatField(max_length=10, null=True, blank=True)  # 孔内瓦斯的异常孔深位置
    ab_situation = models.CharField(max_length=30, null=True, blank=True)  # 孔内瓦斯异常情况
    security_test_person = models.CharField(max_length=30, null=True, blank=True)  # 安检员，手写板签字
    shi_watcher = models.CharField(max_length=30, null=True, blank=True)  # 瓦检员，手写板签字
    drill_type = models.CharField(max_length=30, null=True, blank=True)  # 钻孔类别 ,顺层/穿孔
    status = models.CharField(max_length=10, null=False, blank=False, default="0")  # 当前申请状态，0为审批未通过，1为审批通过，2为驳回， 3为冲孔/封孔申请，4为冲孔/封孔申请通过
    desc = models.CharField(max_length=50, null=True, blank=True)  # 状态描述
    reason = models.CharField(max_length=50, null=True, blank=True)  # 原因描述

    class Meta:
        db_table = 'hole_construction'


# 瓦斯浓度测量表
class Test_Hole(models.Model):  # 测试孔
    row = models.ForeignKey(Row, on_delete=models.CASCADE)  # 关联Row
    hole_name = models.CharField(max_length=30)  # 孔的名字
    date_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # 测量日期
    chroma = models.FloatField(max_length=10, null=True, blank=True)  # 浓度
    mixed_flow = models.FloatField(max_length=10, null=True, blank=True)  # 混合流量，立方
    pressure = models.FloatField(max_length=10, null=True, blank=True)  # 负压
    test_person = models.CharField(max_length=30, null=True, blank=True)  # 测量人姓名
    check_person = models.CharField(max_length=30, null=True, blank=True)  # 验收人姓名

    class Meta:
        db_table = 'test_hole'

    def __str__(self):
        return f"test_hole:{self.chroma}"


class Hole_Eval(models.Model):  # 评价孔
    row = models.ForeignKey(Row, on_delete=models.CASCADE)  # 关联Row
    h_name = models.CharField(max_length=30)  # 孔的名字
    see_coal_eval = models.CharField(max_length=25, null=True, blank=True)  # 见煤评价
    see_ceil_eval = models.CharField(max_length=25, null=True, blank=True)  # 见顶评价
    flush_coal_eval = models.CharField(max_length=25, null=True, blank=True)  # 冲煤评价
    hole_distance_eval = models.CharField(max_length=25, null=True, blank=True)  # 孔间距评价
    is_not_add_hole = models.CharField(max_length=25, null=True, blank=True)  # 是否补孔
    add_hole_param = models.CharField(max_length=30, null=True, blank=True)  # 补孔参数
    emergency_handling = models.TextField(null=True, blank=True)  # 应急处置

    class Meta:
        db_table = 'hole_eval'

    def __str__(self):
        return f"hole_eval:{self.flush_coal_eval}"


# 以下是单孔施工之后要绘图的数据表
class Completion_plan_coordinate(models.Model):  # 竣工开孔平面坐标、竣工见煤平面坐标、竣工见顶平面坐标、喷孔点平面坐标、断杆/压钻点平面坐标
    completion_row = models.ForeignKey(Row, on_delete=models.CASCADE)  # 外键，关联排
    completion_hole_num = models.CharField(max_length=30, null=True, blank=True)  # 孔的编号
    kai_kong_x = models.FloatField(max_length=10, null=True, blank=True)  # 竣工开孔平面坐标x
    kai_kong_y = models.FloatField(max_length=10, null=True, blank=True)  # 竣工开孔平面坐标y
    kai_kong_z = models.FloatField(max_length=10, null=True, blank=True)  # 竣工开孔平面坐标z
    see_coal_x = models.FloatField(max_length=10, null=True, blank=True)  # 竣工见煤平面坐标x
    see_coal_y = models.FloatField(max_length=10, null=True, blank=True)  # 竣工见煤平面坐标y
    see_coal_z = models.FloatField(max_length=10, null=True, blank=True)  # 竣工见煤平面坐标z
    see_cile_x = models.FloatField(max_length=10, null=True, blank=True)  # 竣工见顶平面坐标x
    see_cile_y = models.FloatField(max_length=10, null=True, blank=True)  # 竣工见顶平面坐标y
    see_cile_z = models.FloatField(max_length=10, null=True, blank=True)  # 竣工见顶平面坐标z
    pen_hole_x = models.FloatField(max_length=10, null=True, blank=True)  # 喷孔点平面坐标x
    pen_hole_y = models.FloatField(max_length=10, null=True, blank=True)  # 喷孔点平面坐标y
    pen_hole_z = models.FloatField(max_length=10, null=True, blank=True)  # 喷孔点平面坐标z
    ya_zuan_x = models.FloatField(max_length=10, null=True, blank=True)  # 压钻点平面坐标x
    ya_zuan_y = models.FloatField(max_length=10, null=True, blank=True)  # 压钻点平面坐标y
    ya_zuan_z = models.FloatField(max_length=10, null=True, blank=True)  # 压钻点平面坐标z
    hole_depth_x = models.FloatField(max_length=10, null=True, blank=True)  # 竣工终孔x     *****
    hole_depth_y = models.FloatField(max_length=10, null=True, blank=True)  # 竣工终孔y     *****
    hole_depth_z = models.FloatField(max_length=10, null=True, blank=True)  # 竣工终孔z     *****

    class Meta:
        db_table = "completion_plan_coordinate"

    def __str__(self):
        return f"completion_plan_coordinate:{self.kai_kong_x}"


class Video_confirmation(models.Model):  # 地面视频确认表
    confir_row = models.ForeignKey(Row, on_delete=models.CASCADE)  # 外键，关联排
    confir_hole_num = models.CharField(max_length=30, null=True, blank=True)  # 孔的编号
    confir_chong_mei = models.CharField(max_length=30, null=True, blank=True)  # 确认冲煤量，合格、欠冲、超量
    confir_row_hole = models.CharField(max_length=30, null=True, blank=True)  # 排号、孔号确认
    confir_video_id = models.CharField(max_length=30, null=True, blank=True)  # 视频号确认，正确/手动修改
    confir_hole_depth = models.CharField(max_length=30, null=True, blank=True)  # 确认孔深
    confir_feng_kong = models.CharField(max_length=30, null=True, blank=True)  # 确认封孔，合格/注浆量不合格/未封孔
    confir_yi_chang = models.CharField(max_length=30, null=True, blank=True)  # 异常情况确认
    video_check_person = models.CharField(max_length=30, null=True, blank=True)  # 视频验收人员签字

    class Meta:
        db_table = "video_confirmation"

    def __str__(self):
        return f"video_confirmation:{self.video_check_person}"
#视频举牌验收
class vedioCheck(models.Model):
    row = models.ForeignKey(Row, on_delete=models.CASCADE)  # 关联Row
    h_c_number = models.CharField(max_length=30)  # 孔号由系统自动根据排序列出
    isKaiKongShenQing = models.CharField(max_length= 2, null = False, blank=False, default="0") #开孔申请
    isKaiKongJuPai = models.CharField(max_length= 2, null = False, blank=False, default="0") #开孔举牌
    isJianMeiJuPai = models.CharField(max_length= 2, null = False, blank=False, default="0") #见煤举牌
    isJianDingJuPai = models.CharField(max_length= 2, null = False, blank=False, default="0") #见顶举牌
    isZhongKongJuPai = models.CharField(max_length= 2, null = False, blank=False, default="0") #终孔举牌
    isTuiZuanYanShouJuPai = models.CharField(max_length= 2, null = False, blank=False, default="0") #退钻举牌
    isChongMeiYanShouJuPai = models.CharField(max_length= 2, null = False, blank=False, default="0") #冲煤验收举牌
    isFengKongKaiShiJuPai = models.CharField(max_length= 2, null = False, blank=False, default="0") #封孔开始举牌
    isFengKongYanShouJuPai = models.CharField(max_length= 2, null = False, blank=False, default="0") #封孔验收举牌
    date_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # 填写日期
    person = models.CharField(max_length=50, null=True, blank=True)  # 填写人
    desc = models.CharField(max_length= 50, null = True, blank = True) #反馈信息

    def __str__(self):
        return f"h_c_number:{self.h_c_number}"

#施工资料验收
class ShiGongCheck(models.Model):
    row = models.ForeignKey(Row, on_delete=models.CASCADE)  # 关联Row
    h_c_number = models.CharField(max_length=30)  # 孔号由系统自动根据排序列出
    isQiQuan = models.CharField(max_length= 2, null = False, blank=False, default="0") #钻进施工原始表填写齐全
    isCeXie = models.CharField(max_length= 2, null = False, blank=False, default="0") #是否按照要求测斜
    date_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # 填写日期
    person = models.CharField(max_length =50, null=True, blank=True)  # 填写人
    desc = models.CharField(max_length= 50, null = True, blank = True) #反馈信息

    def __str__(self):
        return f"h_c_number:{self.h_c_number}"

class Wash_Coal_Construction(models.Model):  # 冲煤表
    row = models.ForeignKey(Row, on_delete=models.CASCADE)  # 关联Row
    h_c_number = models.CharField(max_length=30)  # 孔号由系统自动根据排序列出
    video_number = models.CharField(max_length=30, null=True, blank=True)  # 视频编号，这个还是不知道存储类型，所以就只接存储为字符类型
    con_see_coal = models.FloatField(max_length=10, null=True, blank=True)  # 施工见煤
    con_see_ceil = models.FloatField(max_length=10, null=True, blank=True)  # 施工见顶
    chong_drill_eval = models.CharField(max_length=30, null=True, blank=True)  # 冲孔评价，手写板签字
    coal_rush_quantity_length = models.FloatField(max_length=10, null=True, blank=True)  # 当班冲煤量的长
    coal_rush_quantity_wide = models.FloatField(max_length=10, null=True, blank=True)  # 当班冲煤量的宽
    coal_rush_quantity_height = models.FloatField(max_length=10, null=True, blank=True)  # 当班冲煤量的高
    water_start_time = models.DateTimeField(auto_now_add=True)  # 水力冲孔开始时间
    water_end_time = models.DateTimeField(auto_now_add=True)  # 水力冲孔结束时间
    chong_security_test_person = models.CharField(max_length=30, null=True, blank=True)  # 安检员，手写板签字
    chong_watcher = models.CharField(max_length=30, null=True, blank=True)  # 瓦检员，手写板签字
    chong_grouting_person = models.CharField(max_length=30, null=True, blank=True)  # 注浆人姓名，手写板签字
    chong_grouting_abnormal_situation = models.CharField(max_length=30, null=True, blank=True)  # 注浆异常情况
    drill_type = models.CharField(max_length=30, null=True, blank=True)  # 钻孔类别 ,顺层/穿孔
    construction_person_name = models.CharField(max_length=30, null=True, blank=True)  # 施工负责人姓名，手写板签字
    text_person = models.CharField(max_length=30, null=True, blank=True)  # 验收人员，手写板签字
    status = models.CharField(max_length=10, null=False, blank=False, default="0")  # 当前申请状态,0为审批未通过，1为审批通过，2为驳回， 3为冲孔/封孔申请，4为冲孔/封孔申请通过
    desc = models.CharField(max_length=50, null=True, blank=True)  # 状态描述
    reason = models.CharField(max_length=50, null=True, blank=True)  # 原因描述
    actual_flush_mei = models.FloatField(max_length=10, null=True, blank=True)  #应冲煤量
    time = models.DateTimeField(auto_now_add=True)  # 冲孔时间
    flush_water_pressure =  models.FloatField(max_length=10, null=True, blank=True)  #冲孔水压
    kong_radius =  models.FloatField(max_length=10, null=True, blank=True)  #孔径

class zhu_jiang_Construction(models.Model):  # 注浆孔
    row = models.ForeignKey(Row, on_delete=models.CASCADE)  # 关联Row
    h_c_number = models.CharField(max_length=30)  # 孔号由系统自动根据排序列出
    video_number = models.CharField(max_length=30, null=True, blank=True)  # 视频编号，字符类型
    zhu_drill_eval = models.CharField(max_length=30, null=True, blank=True)  # 注浆评价
    screening_length = models.FloatField(max_length=10, null=True, blank=True)  # 筛管长度
    grouting_pressure = models.FloatField(max_length=10, null=True, blank=True)  # 注浆压力
    grouting_amount = models.FloatField(max_length=10, null=True, blank=True)  # 注浆量
    start_hole_depth = models.FloatField(max_length=10, null=True, blank=True)  # 开始封孔孔深
    end_hole_depth = models.FloatField(max_length=10, null=True, blank=True)  # 结束封孔孔深
    zhu_security_test_person = models.CharField(max_length=30, null=True, blank=True)  # 安检员，手写板签字
    zhu_watcher = models.CharField(max_length=30, null=True, blank=True)  # 瓦检员，手写板签字
    grouting_person = models.CharField(max_length=30, null=True, blank=True)  # 注浆人姓名，手写板签字
    grouting_abnormal_situation = models.CharField(max_length=30, null=True, blank=True)  # 注浆异常情况
    drill_type = models.CharField(max_length=30, null=True, blank=True)  # 钻孔类别 ,顺层/穿孔
    construction_person_name = models.CharField(max_length=30, null=True, blank=True)  # 施工负责人姓名，手写板签字
    text_person = models.CharField(max_length=30, null=True, blank=True)  # 验收人员，手写板签字
    feng_time = models.DateTimeField(auto_now_add=True)  # 封孔时间
    status = models.CharField(max_length=10, null=False, blank=False, default="0")  # 当前申请状态,0为审批未通过，1为审批通过，2为驳回, 3为冲孔/封孔申请，4为冲孔/封孔申请通过, 5为冲孔/封孔申请驳回
    desc = models.CharField(max_length=50, null=True, blank=True)  # 状态描述
    reason = models.CharField(max_length=50, null=True, blank=True)  # 原因描述


class Wen_zi(models.Model):  # 竣工平面图文字（孔号）  具体内容参考文字1  九里山矿不纳入数据库，直接留在底图上
    wen_zi_row = models.ForeignKey(Row, on_delete=models.CASCADE)  # 外键，关联排
    wen_zi_hole_num = models.CharField(max_length=30, null=True, blank=True)  # 孔的编号
    wen_zi_x = models.FloatField(max_length=10, null=True, blank=True)  # 竣工孔号文字起点坐标x
    wen_zi_y = models.FloatField(max_length=10, null=True, blank=True)  # 竣工孔号文字起点坐标y
    wen_zi_z = models.FloatField(max_length=10, null=True, blank=True)  # 竣工孔号文字起点坐标z
    wen_zi_content = models.CharField(max_length=256, null=True, blank=True)  # 文字内容

    class Meta:
        db_table = "wen_zi"

    def __str__(self):
        return f"wen_zi:{self.wen_zi_content}"


class zhun_kong_graph1(models.Model):  # 竣工剖面图钻孔图形1（见煤、见顶、冲煤、喷孔、异常）
    graph1_row = models.ForeignKey(Row, on_delete=models.CASCADE)  # 外键，关联排
    graph1_hole_num = models.CharField(max_length=30, null=True, blank=True)  # 孔的编号
    graph1_x = models.FloatField(max_length=30, null=True, blank=True)  # 竣工图钻孔图形标志坐标x
    graph1_y = models.FloatField(max_length=30, null=True, blank=True)  # 竣工图钻孔图形标志坐标y
    graph1_z = models.FloatField(max_length=30, null=True, blank=True)  # 竣工图钻孔图形标志坐标z
    graph1_style = models.CharField(max_length=100, null=True, blank=True)  # 备注：包含图样、颜色及线型、图层
    graph2_x = models.FloatField(max_length=30, null=True, blank=True)  # 竣工图钻孔图形标志坐标x
    graph2_y = models.FloatField(max_length=30, null=True, blank=True)  # 竣工图钻孔图形标志坐标y
    graph2_z = models.FloatField(max_length=30, null=True, blank=True)  # 竣工图钻孔图形标志坐标z
    graph2_style = models.CharField(max_length=100, null=True, blank=True)  # 备注：包含图样、颜色及线型、图层
    graph3_x = models.FloatField(max_length=30, null=True, blank=True)  # 竣工图钻孔图形标志坐标x
    graph3_y = models.FloatField(max_length=30, null=True, blank=True)  # 竣工图钻孔图形标志坐标y
    graph3_z = models.FloatField(max_length=30, null=True, blank=True)  # 竣工图钻孔图形标志坐标z
    graph3_style = models.CharField(max_length=100, null=True, blank=True)  # 备注：包含图样、颜色及线型、图层
    graph4_x = models.FloatField(max_length=30, null=True, blank=True)  # 竣工图钻孔图形标志坐标x
    graph4_y = models.FloatField(max_length=30, null=True, blank=True)  # 竣工图钻孔图形标志坐标y
    graph4_z = models.FloatField(max_length=30, null=True, blank=True)  # 竣工图钻孔图形标志坐标z
    graph4_style = models.CharField(max_length=100, null=True, blank=True)  # 备注：包含图样、颜色及线型、图层
    graph5_x = models.FloatField(max_length=30, null=True, blank=True)  # 竣工图钻孔图形标志坐标x
    graph5_y = models.FloatField(max_length=30, null=True, blank=True)  # 竣工图钻孔图形标志坐标y
    graph5_z = models.FloatField(max_length=30, null=True, blank=True)  # 竣工图钻孔图形标志坐标z
    graph5_style = models.CharField(max_length=100, null=True, blank=True)  # 备注：包含图样、颜色及线型、图层

    class Meta:
        db_table = "zhun_kong_graph1"

    def __str__(self):
        return f"zhun_kong_graph1:{self.graph1_style}"


class jun_zhong_hole(models.Model):  # 竣工终孔平面坐标表
    zhong_row = models.ForeignKey(Row, on_delete=models.CASCADE)  # 外键，关联排
    zhong_hole_num = models.CharField(max_length=30, null=True, blank=True)  # 孔的编号
    zhong_x = models.CharField(max_length=30, null=True, blank=True)  # 终孔坐标x
    zhong_y = models.CharField(max_length=30, null=True, blank=True)  # 终孔坐标y
    zhong_z = models.CharField(max_length=30, null=True, blank=True)  # 终孔坐标z
    jun_pao_position_pen_cad_x = models.FloatField(max_length=10, null=True, blank=True)  # 喷孔点平面坐标cad_x    *****
    jun_pao_position_pen_cad_y = models.FloatField(max_length=10, null=True, blank=True)  # 喷孔点平面坐标cad_y    *****
    jun_pao_position_pen_cad_z = models.FloatField(max_length=10, null=True, blank=True)  # 喷孔点平面坐标cad_z    *****
    jun_pao_position_ya_cad_x = models.FloatField(max_length=10, null=True, blank=True)  # 压钻点平面坐标cad_x     *****
    jun_pao_position_ya_cad_y = models.FloatField(max_length=10, null=True, blank=True)  # 压钻点平面坐标cad_y     *****
    jun_pao_position_ya_cad_z = models.FloatField(max_length=10, null=True, blank=True)  # 压钻点平面坐标cad_z     *****
    jun_pao_see_coal_cad_x = models.FloatField(max_length=10, null=True, blank=True)  # 见煤平面坐标cad_x     *****
    jun_pao_see_coal_cad_y = models.FloatField(max_length=10, null=True, blank=True)  # 见煤平面坐标cad_y     *****
    jun_pao_see_coal_cad_z = models.FloatField(max_length=10, null=True, blank=True)  # 见煤平面坐标cad_z     *****
    jun_pao_see_ceil_cad_x = models.FloatField(max_length=10, null=True, blank=True)  # 见顶平面坐标cad_x     *****
    jun_pao_see_ceil_cad_y = models.FloatField(max_length=10, null=True, blank=True)  # 见顶平面坐标cad_y     *****
    jun_pao_see_ceil_cad_z = models.FloatField(max_length=10, null=True, blank=True)  # 见顶平面坐标cad_z     *****
    jun_pao_zhong_kong_cad_x = models.FloatField(max_length=10, null=True, blank=True)  # 终孔平面坐标cad_x     *****
    jun_pao_zhong_kong_cad_y = models.FloatField(max_length=10, null=True, blank=True)  # 终孔平面坐标cad_y     *****
    jun_pao_zhong_kong_cad_z = models.FloatField(max_length=10, null=True, blank=True)  # 终孔平面坐标cad_z     *****

    class Meta:
        db_table = "jun_zhong_hole"

    def __str__(self):
        return f"jun_zhong_hole:{self.zhong_x}"
        return f"jun_zhong_hole:{self.zhong_x}"


class pao_wen_zi(models.Model):  # 竣工剖面图文字（孔号）  具体内容参考文字1  九里山矿不纳入数据库，直接留在底图上
    pao_row = models.ForeignKey(Row, on_delete=models.CASCADE)  # 外键，关联排
    pao_hole_num = models.CharField(max_length=10, null=True, blank=True)  # 孔的编号
    pao_wen_zi_x = models.FloatField(max_length=10, null=True, blank=True)  # 剖面竣工孔号文字起点坐标x
    pao_wen_zi_y = models.FloatField(max_length=10, null=True, blank=True)  # 剖面竣工孔号文字起点坐标y
    pao_wen_zi_z = models.FloatField(max_length=10, null=True, blank=True)  # 剖面竣工孔号文字起点坐标z
    pao_wen_zi_content = models.CharField(max_length=100, null=True, blank=True)  # 文字内容,包含文字、数字以及特殊字符
    pao_wen_zi1_x = models.FloatField(max_length=10, null=True, blank=True)  # 剖面竣工孔号下平面文字起点坐标x     *****
    pao_wen_zi1_y = models.FloatField(max_length=10, null=True, blank=True)  # 剖面竣工孔号下平面文字起点坐标y     *****
    pao_wen_zi1_z = models.FloatField(max_length=10, null=True, blank=True)  # 剖面竣工孔号下平面文字起点坐标z     *****

    class Meta:
        db_table = "pao_wen_zi"

    def __str__(self):
        return f"pao_wen_zi:{self.pao_wen_zi_content}"


class pao_graph1(models.Model):  # 竣工剖面图钻孔图形1（见煤、见顶、冲煤、喷孔、异常）
    pao_graph1_row = models.ForeignKey(Row, on_delete=models.CASCADE)  # 外键，关联排
    pao_graph1_hole_num = models.CharField(max_length=30, null=True, blank=True)  # 孔的编号
    pao_graph1_x = models.FloatField(max_length=30, null=True, blank=True)  # 剖面竣工孔号文字起点坐标x
    pao_graph1_y = models.FloatField(max_length=30, null=True, blank=True)  # 剖面竣工孔号文字起点坐标y
    pao_graph1_z = models.FloatField(max_length=30, null=True, blank=True)  # 剖面竣工孔号文字起点坐标z
    pao_graph2_x = models.FloatField(max_length=30, null=True, blank=True)  # *****
    pao_graph2_y = models.FloatField(max_length=30, null=True, blank=True)  # *****
    pao_graph2_z = models.FloatField(max_length=30, null=True, blank=True)  # *****
    pao_graph3_x = models.FloatField(max_length=30, null=True, blank=True)  # *****
    pao_graph3_y = models.FloatField(max_length=30, null=True, blank=True)  # *****
    pao_graph3_z = models.FloatField(max_length=30, null=True, blank=True)  # *****
    pao_graph4_x = models.FloatField(max_length=30, null=True, blank=True)  # *****
    pao_graph4_y = models.FloatField(max_length=30, null=True, blank=True)  # *****
    pao_graph4_z = models.FloatField(max_length=30, null=True, blank=True)  # *****
    pao_graph5_x = models.FloatField(max_length=30, null=True, blank=True)  # *****
    pao_graph5_y = models.FloatField(max_length=30, null=True, blank=True)  # *****
    pao_graph5_z = models.FloatField(max_length=30, null=True, blank=True)  # *****
    pao_graph1_content = models.CharField(max_length=100, null=True, blank=True)  # 文字内容,包含文字、数字以及特殊字符
    pao_graph2_content = models.CharField(max_length=100, null=True, blank=True)  # 文字内容,包含文字、数字以及特殊字符*****
    pao_graph3_content = models.CharField(max_length=100, null=True, blank=True)  # 文字内容,包含文字、数字以及特殊字符*****
    pao_graph4_content = models.CharField(max_length=100, null=True, blank=True)  # 文字内容,包含文字、数字以及特殊字符*****
    pao_graph5_content = models.CharField(max_length=100, null=True, blank=True)  # 文字内容,包含文字、数字以及特殊字符*****

    class Meta:
        db_table = "pao_graph1"

    def __str__(self):
        return f"pao_graph1:{self.pao_graph1_content}"


class jun_pao(models.Model):  # 竣工开孔剖面坐标、竣工见煤剖面坐标、竣工见顶剖面坐标、竣工终孔剖面坐标
    jun_pao_row = models.ForeignKey(Row, on_delete=models.CASCADE)  # 外键，关联排
    jun_pao_hole_num = models.CharField(max_length=30, null=True, blank=True)  # 孔的编号
    jun_pao_kai_x = models.FloatField(max_length=10, null=True, blank=True)  # 竣工开孔剖面坐标x
    jun_pao_kai_y = models.FloatField(max_length=10, null=True, blank=True)  # 竣工开孔剖面坐标y
    jun_pao_kai_z = models.FloatField(max_length=10, null=True, blank=True)  # 竣工开孔剖面坐标z
    jun_pao_see_coal_x = models.FloatField(max_length=10, null=True, blank=True)  # 竣工见煤剖面坐标x
    jun_pao_see_coal_y = models.FloatField(max_length=10, null=True, blank=True)  # 竣工见煤剖面坐标y
    jun_pao_see_coal_z = models.FloatField(max_length=10, null=True, blank=True)  # 竣工见煤剖面坐标z
    jun_pao_see_ceil_x = models.FloatField(max_length=10, null=True, blank=True)  # 竣工见顶剖面坐标x
    jun_pao_see_ceil_y = models.FloatField(max_length=10, null=True, blank=True)  # 竣工见顶剖面坐标y
    jun_pao_see_ceil_z = models.FloatField(max_length=10, null=True, blank=True)  # 竣工见顶剖面坐标z
    jun_pao_zhong_kong_x = models.FloatField(max_length=10, null=True, blank=True)  # 竣工终孔剖面坐标x
    jun_pao_zhong_kong_y = models.FloatField(max_length=10, null=True, blank=True)  # 竣工终孔剖面坐标y
    jun_pao_zhong_kong_z = models.FloatField(max_length=10, null=True, blank=True)  # 竣工终孔剖面坐标z
    jun_pao_position_pen_x = models.FloatField(max_length=10, null=True, blank=True)  # 竣工喷孔剖面坐标x     *****
    jun_pao_position_pen_y = models.FloatField(max_length=10, null=True, blank=True)  # 竣工喷孔剖面坐标y     *****
    jun_pao_position_pen_z = models.FloatField(max_length=10, null=True, blank=True)  # 竣工喷孔剖面坐标z     *****
    jun_pao_position_ya_x = models.FloatField(max_length=10, null=True, blank=True)  # 竣工压孔剖面坐标x     *****
    jun_pao_position_ya_y = models.FloatField(max_length=10, null=True, blank=True)  # 竣工压孔剖面坐标y     *****
    jun_pao_position_ya_z = models.FloatField(max_length=10, null=True, blank=True)  # 竣工压孔剖面坐标z     *****

    class Meta:
        db_table = "jun_pao"

    def __str__(self):
        return f"jun_pao:{self.jun_pao_see_ceil_x}"


# ******************************
class jun_pao_cad(models.Model):  # cad坐标
    jun_pao_row = models.ForeignKey(Row, on_delete=models.CASCADE)  # 外键，关联排
    jun_pao_hole_num = models.CharField(max_length=30, null=True, blank=True)  # 孔的编号
    jun_pao_kai_cad_x = models.FloatField(max_length=10, null=True, blank=True)  # 竣工开孔剖面坐标cad_x
    jun_pao_kai_cad_y = models.FloatField(max_length=10, null=True, blank=True)  # 竣工开孔剖面坐标cad_y
    jun_pao_kai_cad_z = models.FloatField(max_length=10, null=True, blank=True)  # 竣工开孔剖面坐标cad_z
    jun_pao_see_coal_cad_x = models.FloatField(max_length=10, null=True, blank=True)  # 竣工见煤剖面坐标cad_x
    jun_pao_see_coal_cad_y = models.FloatField(max_length=10, null=True, blank=True)  # 竣工见煤剖面坐标cad_y
    jun_pao_see_coal_cad_z = models.FloatField(max_length=10, null=True, blank=True)  # 竣工见煤剖面坐标cad_z
    jun_pao_see_ceil_cad_x = models.FloatField(max_length=10, null=True, blank=True)  # 竣工见顶剖面坐标cad_x
    jun_pao_see_ceil_cad_y = models.FloatField(max_length=10, null=True, blank=True)  # 竣工见顶剖面坐标cad_y
    jun_pao_see_ceil_cad_z = models.FloatField(max_length=10, null=True, blank=True)  # 竣工见顶剖面坐标cad_z
    jun_pao_zhong_kong_cad_x = models.FloatField(max_length=10, null=True, blank=True)  # 竣工终孔剖面坐标cad_x
    jun_pao_zhong_kong_cad_y = models.FloatField(max_length=10, null=True, blank=True)  # 竣工终孔剖面坐标cad_y
    jun_pao_zhong_kong_cad_z = models.FloatField(max_length=10, null=True, blank=True)  # 竣工终孔剖面坐标cad_z
    jun_pao_position_pen_cad_x = models.FloatField(max_length=10, null=True, blank=True)  # 竣工喷孔剖面坐标cad_x
    jun_pao_position_pen_cad_y = models.FloatField(max_length=10, null=True, blank=True)  # 竣工喷孔剖面坐标cad_y
    jun_pao_position_pen_cad_z = models.FloatField(max_length=10, null=True, blank=True)  # 竣工喷孔剖面坐标cad_z
    jun_pao_position_ya_cad_x = models.FloatField(max_length=10, null=True, blank=True)  # 竣工压钻剖面坐标cad_x
    jun_pao_position_ya_cad_y = models.FloatField(max_length=10, null=True, blank=True)  # 竣工压钻剖面坐标cad_y
    jun_pao_position_ya_cad_z = models.FloatField(max_length=10, null=True, blank=True)  # 竣工压钻剖面坐标cad_z

    class Meta:
        db_table = "jun_pao_cad"

    def __str__(self):
        return f"jun_pao_cad:{self.jun_pao_see_ceil_cad_x}"


class jun_start_end(models.Model):  # 竣工剖面图煤层顶板起止线条坐标、竣工剖面图煤层底板起止线条坐标
    jun_start_end_row = models.ForeignKey(Row, on_delete=models.CASCADE)  # 外键，关联排
    jun_start_end_hole_num = models.CharField(max_length=30, null=True, blank=True)  # 孔的编号
    jun_start_ding_x = models.FloatField(max_length=10, null=True, blank=True)  # 竣工煤层顶板起点坐标x
    jun_start_ding_y = models.FloatField(max_length=10, null=True, blank=True)  # 竣工煤层顶板起点坐标y
    jun_start_ding_z = models.FloatField(max_length=10, null=True, blank=True)  # 竣工煤层顶板起点坐标z
    jun_end_ding_x = models.FloatField(max_length=10, null=True, blank=True)  # 竣工煤层顶板终点坐标x
    jun_end_ding_y = models.FloatField(max_length=10, null=True, blank=True)  # 竣工煤层顶板终点坐标y
    jun_end_ding_z = models.FloatField(max_length=10, null=True, blank=True)  # 竣工煤层顶板终点坐标z
    jun_start_di_x = models.FloatField(max_length=10, null=True, blank=True)  # 竣工煤层底板起点坐标x
    jun_start_di_y = models.FloatField(max_length=10, null=True, blank=True)  # 竣工煤层底板起点坐标y
    jun_start_di_z = models.FloatField(max_length=10, null=True, blank=True)  # 竣工煤层底板起点坐标z
    jun_end_di_x = models.FloatField(max_length=10, null=True, blank=True)  # 竣工煤层底板终点坐标x
    jun_end_di_y = models.FloatField(max_length=10, null=True, blank=True)  # 竣工煤层底板终点坐标y
    jun_end_di_z = models.FloatField(max_length=10, null=True, blank=True)  # 竣工煤层底板终点坐标z

    class Meta:
        db_table = "jun_start_end"

    def __str__(self):
        return f"jun_start_end:{self.jun_start_ding_x}"


class see_end_coal(models.Model):  # 竣工剖面图下垂线见止煤坐标表
    see_end_coal_row = models.ForeignKey(Row, on_delete=models.CASCADE)  # 外键，关联排
    see_end_coal_hole_num = models.CharField(max_length=30, null=True, blank=True)  # 孔的编号
    see_coal_x = models.FloatField(max_length=10, null=True, blank=True)  # 竣工剖面图下垂线见煤坐标x
    see_coal_y = models.FloatField(max_length=10, null=True, blank=True)  # 竣工剖面图下垂线见煤坐标y
    see_coal_z = models.FloatField(max_length=10, null=True, blank=True)  # 竣工剖面图下垂线见煤坐标z
    see_style = models.CharField(max_length=30, null=True, blank=True)  # 图形样式
    end_coal_x = models.FloatField(max_length=10, null=True, blank=True)  # 竣工剖面图下垂线见煤坐标x
    end_coal_y = models.FloatField(max_length=10, null=True, blank=True)  # 竣工剖面图下垂线见煤坐标y
    end_coal_z = models.FloatField(max_length=10, null=True, blank=True)  # 竣工剖面图下垂线见煤坐标z
    end_style = models.FloatField(max_length=10, null=True, blank=True)  # 图形样式

    class Meta:
        db_table = "see_end_coal"

    def __str__(self):
        return f"see_end_coal:{self.see_style}"


class pou_biao_zhu(models.Model):  # 竣工剖面图标注坐标（含煤厚、倾角、左右及总控制范围、岩柱厚度、垂距）
    pou_biao_row = models.ForeignKey(Row, on_delete=models.CASCADE)  # 外键，关联排
    pou_biao_hole_num = models.CharField(max_length=30, null=True, blank=True)  # 孔的编号
    designer_ding_start_x = models.FloatField(max_length=10, null=True, blank=True)  # 设计煤层顶板起点坐标x
    designer_ding_start_y = models.FloatField(max_length=10, null=True, blank=True)  # 设计煤层顶板起点坐标y
    designer_ding_start_z = models.FloatField(max_length=10, null=True, blank=True)  # 设计煤层顶板起点坐标z
    designer_ding_end_x = models.FloatField(max_length=10, null=True, blank=True)  # 设计煤层顶板终点坐标x
    designer_ding_end_y = models.FloatField(max_length=10, null=True, blank=True)  # 设计煤层顶板终点坐标y
    designer_ding_end_z = models.FloatField(max_length=10, null=True, blank=True)  # 设计煤层顶板终点坐标z
    biaozhu_wenzi = models.CharField(max_length=256, null=True, blank=True)  # 标注文字

    class Meta:
        db_table = "pou_biao_zhu"

    def __str__(self):
        return f"pou_biao_zhu:{self.biaozhu_wenzi}"


class ping_zhe(models.Model):  # 平面图控制范围折线段坐标表
    zhe_row = models.ForeignKey(Row, on_delete=models.CASCADE)  # 外键，关联排
    zhe_hole_num = models.CharField(max_length=30, null=True, blank=True)  # 孔的编号
    zhe_x = models.CharField(max_length=30, null=True, blank=True)  # 平面图控制范围折线段坐标x
    zhe_y = models.CharField(max_length=30, null=True, blank=True)  # 平面图控制范围折线段坐标x
    zhe_z = models.CharField(max_length=30, null=True, blank=True)  # 平面图控制范围折线段坐标x
    biao_ji = models.CharField(max_length=30, null=True, blank=True)  # 标记
    zhe_kong_hao1_x = models.CharField(max_length=30, null=True, blank=True)  # 每排最左侧孔号x    *****
    zhe_kong_hao1_y = models.CharField(max_length=30, null=True, blank=True)  # 每排最左侧孔号y    *****
    zhe_kong_hao1_z = models.CharField(max_length=30, null=True, blank=True)  # 每排最左侧孔号z    *****
    zhe_kong_hao2_x = models.CharField(max_length=30, null=True, blank=True)  # 每排最右侧孔号x    *****
    zhe_kong_hao2_y = models.CharField(max_length=30, null=True, blank=True)  # 每排最右侧孔号y    *****
    zhe_kong_hao2_z = models.CharField(max_length=30, null=True, blank=True)  # 每排最右侧孔号z    *****

    class Meta:
        db_table = "ping_zhe"
        verbose_name = "平面图控制范围折线段坐标表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"ping_zhe:{self.biao_ji}"


class pou_zhe_xian(models.Model):  # 剖面图煤巷折线段坐标
    pou_zhe_row = models.ForeignKey(Row, on_delete=models.CASCADE)  # 外键，关联排,由此查排号
    pou_zhe_hole_num = models.CharField(max_length=30, null=True, blank=True)  # 孔的编号
    pou_zhe_x = models.FloatField(max_length=10, null=True, blank=True)
    pou_zhe_y = models.FloatField(max_length=10, null=True, blank=True)
    pou_zhe_z = models.FloatField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = "pou_zhe_xian"
        verbose_name = "剖面图煤巷折线段坐标"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"pou_zhe_xian:{self.pou_zhe_x}"


class ping_mian_zuo_biao_kong_zhi(models.Model):  # 处理后的坐标轴（上部分）
    Chu_li_shang_X = models.FloatField(max_length=10, null=True, blank=True, verbose_name="X坐标")
    Chu_li_shang_Y = models.FloatField(max_length=10, null=True, blank=True, verbose_name="Y坐标")

    class Meta:
        db_table = 'ping_mian_zuo_biao_kong_zhi'
        verbose_name = "处理后的坐标轴(上部分)"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"ping_mian_zuo_biao_kong_zhi:{self.Chu_li_shang_X}"


class ping_mian_zuo_biao_kong_zhi_xia(models.Model):  # 处理后的坐标轴（下部分）
    Chu_li_xia_X = models.FloatField(max_length=10, null=True, blank=True, verbose_name="X坐标")
    Chu_li_xia_Y = models.FloatField(max_length=10, null=True, blank=True, verbose_name="Y坐标")

    class Meta:
        db_table = 'ping_mian_zuo_biao_kong_zhi_xia'
        verbose_name = "处理后的坐标轴(下部分)"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"ping_mian_zuo_biao_kong_zhi:{self.Chu_li_xia_X}"


class xie_ya_fan_wei(models.Model):  # 泄压范围坐标
    Xie_ya_x = models.FloatField(max_length=10, null=True, blank=True, verbose_name="X坐标")
    Xie_ya_y = models.FloatField(max_length=10, null=True, blank=True, verbose_name="Y坐标")

    class Meta:
        db_table = 'xie_ya_fan_wei'
        verbose_name = "泄压范围坐标"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"xie_ya_fan_wei:{self.Xie_ya_y}"

class cad_picture(models.Model):
    row = models.ForeignKey(Row, on_delete= models.CASCADE)
    type = models.CharField(max_length= 2, null = False, blank = False, verbose_name= "文件类型")
    file_root = models.CharField(max_length= 200, null = False, blank = False, verbose_name = "文件路径")
    file_name = models.CharField(max_length= 200, null = False, blank = False, verbose_name= "文件名称")
