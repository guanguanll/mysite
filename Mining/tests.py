import re
from django.forms.models import model_to_dict
import os
import pandas as pd
import math

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Django.settings")
import django

django.setup()

from Mining.models import *


# 角度转弧度函数
def math_function_transform(value):
    transform_value = ((value / 180) * math.pi)
    return transform_value


def get_tunnel_datas(tunnel_name):  # 获取 tunnel数据
    Datas = Tunnel.objects.filter(tunnel_name=tunnel_name).first()
    if Datas is not None:
        Data = model_to_dict(Datas)
    else:
        Data = {}
    return Data


def get_row_datas(tunnel_name, row_id):  # 通过排号和巷道号获取数据
    tunnel_Data = get_tunnel_datas(tunnel_name)
    tunnel_id = tunnel_Data['id']
    Datas = Row.objects.filter(row_id=row_id, tunnel_id=tunnel_id).first()
    if Datas is not None:
        Data = model_to_dict(Datas)
    else:
        Data = {}
    return Data


def get_pai_jian_ju(tunnel_name):  # 通过排号获取排间距
    # row_id = request.Post.get('row_id')
    # tunnel_id = request.Post.get('tunnel_id')
    tunnel_data = get_tunnel_datas(tunnel_name)
    pai_jian_ju = tunnel_data['tunnel_length'] / tunnel_data['tunnel_row_numebers']
    return pai_jian_ju


def get_numbers(hole_number):  # 通过孔号提取数字
    te_shu = False  # 是否为特殊孔
    fen_number = False
    if 'D' in str(hole_number):
        number = re.findall(r"D(.+?)-", hole_number)
        number = int(number[0])
        fen_number = int(hole_number.split('-', 2)[1])  # 特殊孔号跟的分号
        te_shu = True
    elif 'B' in str(hole_number):
        number = re.findall(r"B(.+?)-", hole_number)
        number = int(number[0])
        fen_number = int(hole_number.split('-', 2)[1])
        te_shu = True
    else:
        number = int(hole_number)
    return te_shu, number, fen_number


def get_hang_shen(tunnel_name, row_id):  # 通过排号获取巷深
    # row_id = request.Post.get('row_id')
    # tunnel_id = request.Post.get('tunnel_name')
    number = get_numbers(row_id)[1]
    tunnel_data = get_tunnel_datas(tunnel_name)
    tunnel_id = tunnel_data['id']
    pai_jian_ju = get_pai_jian_ju(tunnel_name)
    current_tunnel_depth = pai_jian_ju * number
    Row.objects.filter(tunnel_id=tunnel_id, row_id=row_id).update(
        current_tunnel_depth=current_tunnel_depth)  # 更新current_tunnel_depth值


# 获取底板巷修正后顶板坐标
def get_di_ban_hang():
    data = di_ban_hang_xiuzheng_ding_ban.objects.values_list('di_I_x', 'di_J_Z')
    di_hang_result = pd.DataFrame(list(data))
    return di_hang_result

    # 获取修正后煤层底板坐标


def get_mei_di():
    data = xiu_zheng_hou_meiceng_di_ban.objects.values_list('xiu_zheng_x', 'xiu_zheng_z')
    mei_di_result = pd.DataFrame(list(data))
    return mei_di_result

    # 获取修正后煤层顶板坐标


def get_mei_ding():
    data = xiu_zheng_mei_ceng_ding_ban.objects.values_list('Xiu_x', 'xiu_z')
    mei_ding_result = pd.DataFrame(list(data))
    return mei_ding_result

    # 获取处理后上部分


def get_chuli_shang():
    data = ping_mian_zuo_biao_kong_zhi.objects.values_list('Chu_li_shang_x', 'Chu_li_shang_y')
    chuli_shang_result = pd.DataFrame(list(data))
    return chuli_shang_result

    # 获取处理后下部分


def get_chuli_xia():
    data = ping_mian_zuo_biao_kong_zhi_xia.objects.values_list('Chu_li_xia_x', 'Chu_li_xia_y')
    chuli_shang_result = pd.DataFrame(list(data))
    return chuli_shang_result

    # 获取泄压范围


def get_xie_ya():
    data = xie_ya_fan_wei.objects.values_list('Xie_ya_x', 'Xie_ya_y')
    xie_ya_result = pd.DataFrame(list(data))
    return xie_ya_result


def get_hole_design_datas(tunnel_name, row_id, hole_number):  # 获取设计孔数据
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']
    Datas = Hole_Design.objects.filter(row_id=id, hole_number=hole_number).first()
    if Datas is not None:
        Data = model_to_dict(Datas)
    else:
        Data = {}
    return Data


def get_hole_construction_datas(tunnel_name, row_id, h_c_number):  # 施工孔号获取施工孔数据
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']
    Datas = Hole_Construction.objects.filter(row_id=id, h_c_number=h_c_number).first()
    if Datas is not None:
        Data = model_to_dict(Datas)
    else:
        Data = {}
    return Data


def get_jun_pao(tunnel_name, row_id, jun_pao_hole_num):  # 通过id和孔号获取竣工开孔数据
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']
    Datas = jun_pao.objects.filter(jun_pao_row=id, jun_pao_hole_num=jun_pao_hole_num).first()
    if Datas is not None:
        Data = model_to_dict(Datas)
    else:
        Data = {}
    return Data


def get_hole_design_pou_mian_datas(tunnel_name, row_id, hole_number):  # 通过id 获取设计孔剖面数据
    design_data = get_hole_design_datas(tunnel_name, row_id, hole_number)
    id = design_data['id']
    Datas = Hole_Design_Pou_Mian.objects.filter(hole_number_id=id).first()
    if Datas is not None:
        Data = model_to_dict(Datas)
    else:
        Data = {}
    return Data


def get_hole_eval(tunnel_name, row_id, h_name):  # 评价孔
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']
    Datas = Hole_Eval.objects.filter(row=id, h_name=h_name).first()
    if Datas is not None:
        Data = model_to_dict(Datas)
    else:
        Data = {}
    return Data


def matching_function(tunnel_name, row_id, hole_number, x):  # 通过巷道号排号孔号奇偶与x求y和z,只适用于首孔
    number = get_numbers(hole_number)[1]  # 提取数字
    tunnel_Data = get_tunnel_datas(tunnel_name)
    row_Data = get_row_datas(tunnel_name, row_id)
    id = row_Data['id']
    current_tunnel_depth = row_Data['current_tunnel_depth']
    tunnel_length = tunnel_Data['tunnel_length']

    data1 = get_di_ban_hang()

    data2 = get_mei_ding()
    data3 = get_mei_di()
    if x < data1.iloc[0, 0] or x > data1.iloc[-1, 0]:
        print('不在修正底板巷范围内！')
        return False
    elif x < data2.iloc[0, 0] or x > data2.iloc[-1, 0]:
        return print('不在修正煤顶范围内！')
        return False
    elif x < data3.iloc[0, 0] or x > data3.iloc[-1, 0]:
        print('不在修正煤底范围内！')
        return False
    else:
        # 1:底板巷修正后顶板坐标
        x_1_hang = data1[data1.iloc[:, 0] <= x].tail(1).iloc[0, 0]
        x_2_hang = data1[data1.iloc[:, 0] > x].head(1).iloc[0, 0]
        z_1_hang = data1[data1.iloc[:, 0] <= x].tail(1).iloc[0, 1]
        z_2_hang = data1[data1.iloc[:, 0] > x].head(1).iloc[0, 1]

        # 2：修正后煤层顶板坐标
        x_1_ding = data2[data2.iloc[:, 0] <= x].tail(1).iloc[0, 0]
        x_2_ding = data2[data2.iloc[:, 0] > x].head(1).iloc[0, 0]
        z_1_ding = data2[data2.iloc[:, 0] <= x].tail(1).iloc[0, 1]
        z_2_ding = data2[data2.iloc[:, 0] > x].head(1).iloc[0, 1]

        # 3：修正后煤层底板坐标
        x_1_di = data3[data3.iloc[:, 0] <= x].tail(1).iloc[0, 0]
        x_2_di = data3[data3.iloc[:, 0] > x].head(1).iloc[0, 0]
        z_1_di = data3[data3.iloc[:, 0] <= x].tail(1).iloc[0, 1]
        z_2_di = data3[data3.iloc[:, 0] > x].head(1).iloc[0, 1]

        di_ban_hang_hight = tunnel_Data['di_ban_hang_hight']
        qi_dian_x = tunnel_Data['di_ban_tunnel_qi_dian_x']  # 起点坐标
        qi_dian_y = tunnel_Data['di_ban_tunnel_qi_dian_y']
        zhong_dian_x = tunnel_Data['di_ban_tunnel_zhong_dian_x']  # 终点坐标
        zhong_dian_y = tunnel_Data['di_ban_tunnel_zhong_dian_y']

        # db = pymysql.connect(host="localhost", user="root", password="5211314.Xm", db='hpu_mining', port=3306)
        # cur = db.cursor()
        # sql_select = 'select design_hole_height from hpu_mining.hole_design where row_id = %s'
        # cur.execute(sql_select, id)
        hole_design_data = Hole_Design.objects.filter(row_id=row_id, hole_number=hole_number)
        # design_hole_heights = pd.DataFrame(cur.fetchall())
        design_hole_heights = pd.DataFrame(hole_design_data)

        if design_hole_heights.empty:
            design_hole_heights = 1.2
        else:
            design_hole_heights = design_hole_heights.iloc[0, 0]
        design_hole_height = design_hole_heights
        row_x = qi_dian_x + (current_tunnel_depth / tunnel_length) * (zhong_dian_x - qi_dian_x)
        row_y = qi_dian_y + (current_tunnel_depth / tunnel_length) * (zhong_dian_y - qi_dian_y)

        z_hang = z_1_hang + (z_2_hang - z_1_hang) * (x - x_1_hang) / (x_2_hang - x_1_hang)
        z_ding = z_1_ding + (z_2_ding - z_1_ding) * (x - x_1_ding) / (x_2_ding - x_1_ding)
        z_di = z_1_di + (z_2_di - z_1_di) * (x - x_1_di) / (x_2_di - x_1_di)
        #   求z坐标 z巷 - 3.3(底板巷巷道高度) +1.2
        z = z_hang - di_ban_hang_hight + design_hole_height
        #   求岩柱厚度
        pillar_thickness = z_di - z_hang

        #   求煤层厚度
        coal_seam_thickness = z_ding - z_di

        """
        sql_insert = 'update hpu_mining.row set row_x = %s, row_y = %s where id ="%s"'

        cur.execute(sql_insert, (row_x, row_y, id))
        db.commit()
        db.close()
        """
        return x, row_x, row_y, z, pillar_thickness, coal_seam_thickness


def jian_zuo_biao(tunnel_name, row_id, hole_number, kai_kong_x, iloc_name, kai_kong_pou_x=None, kai_kong_pou_y=None,
                  pan_duan=None):
    # 各类见坐标(输入排号， 钻孔号， 开孔x， 输入y为hole_design对应列名)
    # 三维转二维
    number = get_numbers(hole_number)[1]  # 提取数字
    row_Data = get_row_datas(tunnel_name, row_id)
    tunnel_Data = get_tunnel_datas(tunnel_name)
    tunnel_first_hole_number = tunnel_Data['tunnel_first_hole_number']
    arch_radius = tunnel_Data['arch_radius']

    if pan_duan == None:  # 判断为施工孔还是设计孔，当pan_duan为空时为设计孔
        hole_design_Data = get_hole_design_datas(tunnel_name, row_id, hole_number)
        y = hole_design_Data[iloc_name]
        design_elevation_angel = hole_design_Data['design_elevation_angel']  # 钻孔仰角
    else:  # 施工孔
        hole_construction_Data = get_hole_construction_datas(tunnel_name, row_id, hole_number)
        y = hole_construction_Data[iloc_name]
        design_elevation_angel = hole_construction_Data['r_elevation_angle']

    shou_kong_number = get_numbers(tunnel_first_hole_number)[1]  # 首孔号数字提取
    s = 1
    if number < shou_kong_number:  # 左右判定 左-1，右1
        s = -1
    if kai_kong_pou_x == None and kai_kong_pou_y == None:
        zuo_biao = matching_function(tunnel_name, row_id, number, kai_kong_x)
        jian_x = format(zuo_biao[2] + s * (y + arch_radius) *
                        math.cos((design_elevation_angel / 180) * math.pi), '.2f')  # 三维转二维读取平面坐标
        jian_y = format(zuo_biao[3] + s *
                        (y + arch_radius) * math.sin((design_elevation_angel / 180) * math.pi), '.2f')
    else:
        jian_x = format(kai_kong_pou_x + s * (y + arch_radius) * math.cos(
            (design_elevation_angel / 180) * math.pi), '.2f')  # 三维转二维读取平面坐标
        jian_y = format(kai_kong_pou_y + s * (y + arch_radius) *
                        math.sin((design_elevation_angel / 180) * math.pi), '.2f')
    return jian_x, jian_y


def design_first_hole(tunnel_name, row_id):  # 设计首孔
    row_Data = get_row_datas(tunnel_name, row_id)
    id = row_Data['id']
    current_tunnel_depth = row_Data['current_tunnel_depth']
    tunnel_Data = get_tunnel_datas(tunnel_name)
    arch_radius = tunnel_Data['arch_radius']
    work_face_id = tunnel_Data['work_face']
    tunnel_first_hole_number = tunnel_Data['tunnel_first_hole_number']  # 首孔号
    qi_dian_x = tunnel_Data['di_ban_tunnel_qi_dian_x']  # 起点坐标
    qi_dian_y = tunnel_Data['di_ban_tunnel_qi_dian_y']
    zhong_dian_x = tunnel_Data['di_ban_tunnel_zhong_dian_x']  # 终点坐标
    zhong_dian_y = tunnel_Data['di_ban_tunnel_zhong_dian_y']
    tunnel_length = tunnel_Data['tunnel_length']
    # 194.06
    row_x = qi_dian_x + (current_tunnel_depth / tunnel_length) * (zhong_dian_x - qi_dian_x)
    row_y = qi_dian_y + (current_tunnel_depth / tunnel_length) * (zhong_dian_y - qi_dian_y)

    design_elevation_angel = 90  # 首孔仰角
    deflection_angle = 0  # 设计偏角
    number = get_numbers(tunnel_first_hole_number)[1]
    weather_empty = get_hole_design_datas(tunnel_name, row_id, number)
    if bool(weather_empty) is not False:
        return '存在此设计孔'
        os._exit(0)
    zuobiao = matching_function(tunnel_name, row_id, number, row_x)
    if zuobiao is False:
        print('匹配错误！')
        return -1
    rock_section = zuobiao[4]  # 设计岩段
    coal_section = zuobiao[5]  # 设计煤段
    see_ceil = coal_section + rock_section
    coal_seam_thickness = zuobiao[5]  # 煤层厚度

    # 设计孔深 穿顶长度 + 见顶长度
    data = Work_face.objects.filter(id=work_face_id)
    mydata = data.values_list('chuan_ding_length', 'chong_mei_standard')
    chuan_ding_lengths = pd.DataFrame(list(mydata))
    chuan_ding_length = chuan_ding_lengths.iloc[0, 0]
    Row.objects.filter(row_id=row_id).update(coal_seam_thickness=coal_seam_thickness)
    hole_depth = see_ceil + float(chuan_ding_length)
    design_hole_height = tunnel_Data['hole_height']  # 设计孔高度
    single_row = 2

    my_record = Hole_Design(hole_number=number, design_hole_height=design_hole_height,
                            deflection_angle=deflection_angle,
                            rock_section=rock_section, coal_section=coal_section, see_ceil=see_ceil,
                            hole_depth=hole_depth,
                            row_id=id, design_elevation_angel=design_elevation_angel, single_row=single_row)
    my_record.save()
    weather_empty1 = get_hole_design_pou_mian_datas(tunnel_name, row_id, number)
    if bool(weather_empty1) is not False:
        return '存在此设计孔剖面信息'
        return -1
    hole_design_Data = get_hole_design_datas(tunnel_name, row_id, number)
    hole_number_id = hole_design_Data['id']  # 新孔的id
    kai_kong_pou_x = 0
    kai_kong_pou_y = design_hole_height
    # design_jian_mei = jian_zuo_biao(tunnel_name, row_id, number, zuobiao[0], 'rock_section')
    # design_jian_mei_x = design_jian_mei[0]
    # design_jian_mei_y = design_jian_mei[1]
    design_jian_mei_x = format((rock_section + arch_radius) * math.cos((design_elevation_angel / 180) * math.pi), '.2f')
    design_jian_mei_y = format(design_hole_height + (rock_section + arch_radius) *
                               math.sin((design_elevation_angel / 180) * math.pi), '.2f')
    # design_jian_ding = jian_zuo_biao(tunnel_name, row_id, number, zuobiao[0], 'see_ceil')
    # design_jian_ding_x = design_jian_ding[0]
    # design_jian_ding_y = design_jian_ding[1]
    design_jian_ding_x = format((see_ceil + arch_radius) * math.cos((design_elevation_angel / 180) * math.pi), '.2f')
    design_jian_ding_y = format(design_hole_height + (see_ceil + arch_radius) *
                                math.sin((design_elevation_angel / 180) * math.pi), '.2f')
    # design_zhong_kong = jian_zuo_biao(tunnel_name, row_id, number, zuobiao[0], 'hole_depth')
    # design_zhong_kong_x = design_zhong_kong[0]
    # design_zhong_kong_y = design_zhong_kong[1]
    zhong_kong_length = float(chuan_ding_length) + see_ceil  # 终孔长度
    design_zhong_kong_x = format((zhong_kong_length + arch_radius) * math.cos((design_elevation_angel / 180) * math.pi),
                                 '.2f')
    design_zhong_kong_y = format(design_hole_height + (zhong_kong_length + arch_radius) *
                                 math.sin((design_elevation_angel / 180) * math.pi), '.2f')

    my_record1 = Hole_Design_Pou_Mian(design_jian_mei_x=design_jian_mei_x, design_jian_mei_y=design_jian_mei_y,
                                      design_jian_ding_x=design_jian_ding_x, design_jian_ding_y=design_jian_ding_y,
                                      design_zhong_kong_x=design_zhong_kong_x, design_zhong_kong_y=design_zhong_kong_y,
                                      kai_kong_pou_x=kai_kong_pou_x, kai_kong_pou_y=kai_kong_pou_y,
                                      hole_number_id=hole_number_id)
    my_record1.save()
    return number


def design_first_even_hole(tunnel_name, row_id):  # 设计首个偶数孔
    row_Data = get_row_datas(tunnel_name, row_id)
    id = row_Data['id']
    current_tunnel_depth = row_Data['current_tunnel_depth']
    tunnel_Data = get_tunnel_datas(tunnel_name)
    work_face_id = tunnel_Data['work_face']
    tunnel_first_hole_number = tunnel_Data['tunnel_first_hole_number']  # 首孔号
    qi_dian_x = tunnel_Data['di_ban_tunnel_qi_dian_x']  # 起点坐标
    qi_dian_y = tunnel_Data['di_ban_tunnel_qi_dian_y']
    zhong_dian_x = tunnel_Data['di_ban_tunnel_zhong_dian_x']  # 终点坐标
    zhong_dian_y = tunnel_Data['di_ban_tunnel_zhong_dian_y']
    tunnel_length = tunnel_Data['tunnel_length']

    row_x = qi_dian_x + (current_tunnel_depth / tunnel_length) * (zhong_dian_x - qi_dian_x)
    row_y = qi_dian_y + (current_tunnel_depth / tunnel_length) * (zhong_dian_y - qi_dian_y)

    design_elevation_angel = 90  # 首孔仰角
    deflection_angle = 0  # 设计偏角
    number = get_numbers(tunnel_first_hole_number)[1]
    number = number - 1  # 偶数首孔号 10
    weather_empty = get_hole_design_datas(tunnel_name, row_id, number)
    if bool(weather_empty) is not False:
        return number
        os._exit(0)
    zuobiao = matching_function(tunnel_name, row_id, number, row_x)
    if zuobiao is False:
        print('匹配错误！')
        os._exit(0)
    rock_section = zuobiao[4]  # 设计岩段
    coal_section = zuobiao[5]  # 设计煤段
    see_ceil = coal_section + rock_section
    coal_seam_thickness = zuobiao[5]  # 煤层厚度
    # 设计孔深 穿顶长度 + 见顶长度
    db = pymysql.connect(host="localhost", user="root", password="5211314.Xm", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_select_chuan_ding = "select work_face.chuan_ding_length, work_face.chong_mei_standard " \
                            "from work_face where id = %s"
    cur.execute(sql_select_chuan_ding, work_face_id)
    chuan_ding_lengths = cur.fetchall()
    chuan_ding_lengths = pd.DataFrame(list(chuan_ding_lengths))

    chuan_ding_length = chuan_ding_lengths.iloc[0, 0]

    chong_mei_standards = chuan_ding_lengths.iloc[0, 1]
    db.close()

    db = pymysql.connect(host="localhost", user="root", password="5211314.Xm", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_insert_coal_seam_thickness = 'update hpu_mining.row set coal_seam_thickness = %s where row_id = %s'
    cur.execute(sql_insert_coal_seam_thickness, (coal_seam_thickness, row_id))
    db.commit()

    hole_depth = see_ceil + float(chuan_ding_length)

    design_hole_height = tunnel_Data['hole_height']  # 设计孔高度
    db.close()
    single_row = 2
    weather_empty1 = get_hole_design_pou_mian_datas(tunnel_name, row_id, number)
    if bool(weather_empty1) is not False:
        return '存在此设计孔剖面信息'
        os._exit(0)
    db = pymysql.connect(host="localhost", user="root", password="5211314.Xm", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_insert = "insert into hpu_mining.hole_design (hole_number, design_hole_height," \
                 " deflection_angle, rock_section, coal_section, see_ceil, hole_depth, row_id," \
                 " design_elevation_angel, single_row) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cur.execute(sql_insert, (number, design_hole_height, deflection_angle,
                             rock_section, coal_section, see_ceil, hole_depth,
                             id, design_elevation_angel, single_row))

    db.commit()
    db.close()

    hole_design_Data = get_hole_design_datas(tunnel_name, row_id, number)
    hole_number_id = hole_design_Data['id']  # 新孔的id
    kai_kong_pou_x = 0
    kai_kong_pou_y = design_hole_height
    design_jian_mei_x = format(rock_section * math.cos((design_elevation_angel / 180) * math.pi), '.2f')
    design_jian_mei_y = format(design_hole_height + rock_section *
                               math.cos((design_elevation_angel / 180) * math.pi), '.2f')
    """
    design_jian_mei = jian_zuo_biao(tunnel_name, row_id, number, zuobiao[0], 'rock_section')
    design_jian_mei_x = design_jian_mei[0]
    design_jian_mei_y = design_jian_mei[1]
    design_jian_ding = jian_zuo_biao(tunnel_name, row_id, number, zuobiao[0], 'see_ceil')
    design_jian_ding_x = design_jian_ding[0]
    design_jian_ding_y = design_jian_ding[1]
    design_zhong_kong = jian_zuo_biao(tunnel_name, row_id, number, zuobiao[0], 'hole_depth')
    design_zhong_kong_x = design_zhong_kong[0]
    design_zhong_kong_y = design_zhong_kong[1]
    """
    db = pymysql.connect(host="localhost", user="root", password="5211314.Xm", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_insert_new_hole_design_pou_mian = "insert into Hole_Design_Pou_Mian(design_jian_mei_x, design_jian_mei_y," \
                                          " design_jian_ding_x, design_jian_ding_y, " \
                                          " design_zhong_kong_x, design_zhong_kong_y," \
                                          " kai_kong_pou_x, kai_kong_pou_y,  hole_number_id" \
                                          ") values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cur.execute(sql_insert_new_hole_design_pou_mian, (design_jian_mei_x, design_jian_mei_y,
                                                      design_jian_ding_x, design_jian_ding_y,
                                                      design_zhong_kong_x, design_zhong_kong_y,
                                                      kai_kong_pou_x, kai_kong_pou_y, hole_number_id))
    db.commit()
    db.close()
    return number


def design_odd_hole(tunnel_name, row_id, hole_number, pan_duan=False):  # 设计奇数孔，hole_number为上一孔号,pan_duan=True
    tunnel_Data = get_tunnel_datas(tunnel_name)  # 向右创建钻孔
    tunnel_first_hole_number = int(tunnel_Data['tunnel_first_hole_number'])
    zuan_kong_chui_ju = tunnel_Data['zuan_kong_chui_ju']  # 钻孔垂距
    arch_radius = tunnel_Data['arch_radius']  # 拱形半径
    mei_ceng_qing_jiao = float(tunnel_Data['mei_ceng_qing_jiao'])  # 煤层倾角
    work_face_id = tunnel_Data['work_face']
    row_Data = get_row_datas(tunnel_name, row_id)
    row_x = row_Data['row_x']
    row_y = row_Data['row_y']
    row_z = row_Data['row_z']
    id = row_Data['id']

    hole_design_data = get_hole_design_datas(tunnel_name, row_id, hole_number)
    single_row = hole_design_data['single_row']
    hole_id = hole_design_data['id']

    # 设计孔深 穿顶长度 + 见顶长度
    my_record = Work_face.objects.filter(id=work_face_id).values_list('chuan_ding_length', 'chong_mei_standard')

    chuan_ding_lengths = pd.DataFrame(list(my_record))

    chuan_ding_length = chuan_ding_lengths.iloc[0, 0]

    chong_mei_standards = chuan_ding_lengths.iloc[0, 1]
    number = get_numbers(hole_number)[1]  # 上一孔号
    first_hole_number = get_numbers(tunnel_first_hole_number)[1]  # 首孔号
    if pan_duan == True:
        new_number = int(number + single_row)
        s = 1
    elif number <= first_hole_number:
        new_number = int(number - single_row)
        s = -1
    else:
        new_number = int(number + single_row)
        s = 1
    weather_empty = get_hole_design_datas(tunnel_name, row_id, new_number)
    if bool(weather_empty) is not False:
        return new_number
    deflection_angle = 0  # 设计偏角

    my_record1 = Hole_Construction.objects.filter(h_c_number=hole_number, row_id=id).values_list('r_elevation_angle',
                                                                                                 'con_see_coal',
                                                                                                 'con_see_ceil',
                                                                                                 'con_hole_depth')

    shang_kong = pd.DataFrame(list(my_record1))  # 上一个孔的信息

    # print("debug inform:", shang_kong.iloc[0, 3])

    my_record2 = jun_pao.objects.filter(jun_pao_row_id=id, jun_pao_hole_num=hole_number).values_list(
        'jun_pao_see_ceil_x', 'jun_pao_see_ceil_y')
    shang_yi_kong = pd.DataFrame(list(my_record2))  # 上一孔需要坐标
    zuan_kong_jia_jiao = format(
        math.asin(zuan_kong_chui_ju / (arch_radius + float(shang_kong.iloc[0, 3]))) * 180 / math.pi, '.1f')  # 钻孔夹角

    # 设计仰角
    design_elevation_angel = format(float(shang_kong.iloc[0, 0]) - float(zuan_kong_jia_jiao) - s * 0.1, '.1f')
    design_elevation_angel = float(design_elevation_angel)

    # 设计新孔见顶x, y坐标

    new_design_jian_ding_x = float(shang_yi_kong.iloc[0, 0]) + zuan_kong_chui_ju / \
                             (s * math.cos(math.radians(90 - design_elevation_angel - s * mei_ceng_qing_jiao))) \
                             * math.cos(math.radians(mei_ceng_qing_jiao))

    #       第一个mei_ceng_qing_jiao 需要匹配，此处用的为tunnel.mei_ceng_qing_jiao
    new_design_jian_ding_y = float(shang_yi_kong.iloc[0, 1]) - zuan_kong_chui_ju / \
                             (s * math.cos((90 - design_elevation_angel - s * mei_ceng_qing_jiao) / 180 * math.pi)) \
                             * math.sin((mei_ceng_qing_jiao) / 180 * math.pi)

    #   设计孔起点坐标
    # new_design_kai_kong_zuo_biao = matching_function(tunnel_name, row_id, new_number, row_x)
    # if new_design_kai_kong_zuo_biao is False:
    # print('匹配错误！')
    # os._exit(0)
    design_hole_height = tunnel_Data['hole_height']  # 设计孔高度
    new_design_kai_kong_x = 0
    new_design_kai_kong_y = design_hole_height

    # new_design_kai_kong_x = new_design_kai_kong_zuo_biao[0]
    # new_design_kai_kong_y = new_design_kai_kong_zuo_biao[3]

    #   设计见顶
    see_ceil = math.sqrt(math.pow(new_design_jian_ding_x - new_design_kai_kong_x, 2)
                         + math.pow(new_design_jian_ding_y - new_design_kai_kong_y, 2)) - arch_radius

    #   设计煤段
    shou_kong_mei_duan_result = get_hole_design_datas(tunnel_name, row_id, tunnel_first_hole_number)

    shou_kong_mei_duan = shou_kong_mei_duan_result['coal_section']
    shou_kong_shi_gong_result = get_hole_construction_datas(tunnel_name, row_id, tunnel_first_hole_number)
    shou_kong_con_see_ceil = shou_kong_shi_gong_result['con_see_ceil']
    shou_kong_con_see_coal = shou_kong_shi_gong_result['con_see_coal']
    shou_kong_mei_duan_length = shou_kong_con_see_ceil - shou_kong_con_see_coal
    coal_section = abs((shou_kong_mei_duan + shou_kong_mei_duan_length) / 2
                       * math.cos((mei_ceng_qing_jiao) / 180 * math.pi)
                       / math.sin((design_elevation_angel - s * mei_ceng_qing_jiao) / 180 * math.pi))

    #   设计孔深
    hole_depth = see_ceil + float(chuan_ding_length)
    rock_section = see_ceil - coal_section  # 设计岩段 = 见煤长度

    my_record2 = Hole_Design(hole_number=new_number, design_hole_height=design_hole_height,
                             deflection_angle=deflection_angle,
                             rock_section=rock_section, coal_section=coal_section, see_ceil=see_ceil,
                             hole_depth=hole_depth,
                             row_id=id, design_elevation_angel=design_elevation_angel, single_row=single_row)
    my_record2.save()

    weather_empty1 = get_hole_design_pou_mian_datas(tunnel_name, row_id, new_number)
    if bool(weather_empty1) is not False:
        return '存在此设计孔剖面信息'
    rock_section = see_ceil - coal_section  # 设计岩段 = 见煤长度
    design_hole_height = tunnel_Data['hole_height']  # 设计孔高度

    hole_design_Data = get_hole_design_datas(tunnel_name, row_id, new_number)
    hole_number_id = hole_design_Data['id']  # 新孔的id
    new_design_jian_mei_results = jian_zuo_biao(tunnel_name, row_id, new_number, row_x, 'rock_section',
                                                new_design_kai_kong_x, new_design_kai_kong_y)
    # new_design_jian_mei_x = new_design_jian_mei_results[0]
    # new_design_jian_mei_y = new_design_jian_mei_results[1]
    new_design_jian_mei_x = format(
        s * (rock_section + arch_radius) * math.cos((design_elevation_angel / 180) * math.pi), '.2f')
    new_design_jian_mei_y = format(design_hole_height + (rock_section + arch_radius) *
                                   math.sin((design_elevation_angel / 180) * math.pi), '.2f')

    zhong_kong_length = float(chuan_ding_length) + see_ceil  # 终孔长度
    new_design_zhong_kong_x = format(
        s * (zhong_kong_length + arch_radius) * math.cos((design_elevation_angel / 180) * math.pi), '.2f')
    new_design_zhong_kong_y = format(design_hole_height + (zhong_kong_length + arch_radius) *
                                     math.sin((design_elevation_angel / 180) * math.pi), '.2f')

    my_record3 = Hole_Design_Pou_Mian(design_jian_mei_x=new_design_jian_mei_x, design_jian_mei_y=new_design_jian_mei_y,
                                      design_jian_ding_x=new_design_jian_ding_x,
                                      design_jian_ding_y=new_design_jian_ding_y,
                                      design_zhong_kong_x=new_design_zhong_kong_x,
                                      design_zhong_kong_y=new_design_zhong_kong_y,
                                      kai_kong_pou_x=new_design_kai_kong_x, kai_kong_pou_y=new_design_kai_kong_y,
                                      hole_number_id=hole_number_id)
    my_record3.save()
    return new_number


def design_even_hole(tunnel_name, row_id, hole_number, pan_duan=False):  # 设计偶数孔, hole_number为输入孔
    tunnel_Data = get_tunnel_datas(tunnel_name)
    tunnel_first_hole_number = int(tunnel_Data['tunnel_first_hole_number'])
    zuan_kong_chui_ju = tunnel_Data['zuan_kong_chui_ju']  # 钻孔垂距
    arch_radius = tunnel_Data['arch_radius']  # 拱形半径
    mei_ceng_qing_jiao = tunnel_Data['mei_ceng_qing_jiao']  # 煤层倾角
    work_face_id = tunnel_Data['work_face']
    row_Data = get_row_datas(tunnel_name, row_id)
    row_x = row_Data['row_x']
    row_y = row_Data['row_y']
    row_z = row_Data['row_z']
    id = row_Data['id']
    single_row = 2
    design_hole_height = 1.2

    # 设计孔深 穿顶长度 + 见顶长度
    my_record = Work_face.objects.filter(id=work_face_id).values_list('chuan_ding_length', 'chong_mei_standard')
    chuan_ding_lengths = pd.DataFrame(list(my_record))
    chuan_ding_length = chuan_ding_lengths.iloc[0, 0]
    chong_mei_standards = chuan_ding_lengths.iloc[0, 1]
    first_number = get_numbers(tunnel_first_hole_number)[1]
    number = get_numbers(hole_number)[1]
    s = 1
    if pan_duan == True:
        if number % 2 == 0:
            number = number + 2
        else:
            number = number + 1
    elif number <= first_number:
        if number % 2 == 0:
            number = number - 2  # number 替换为为新孔号
            s = -1
        else:
            number = number - 1
            s = -1
    else:
        if number % 2 == 0:
            number = number + 2
        else:
            number = number + 1
    weather_empty = get_hole_design_datas(tunnel_name, row_id, number)
    if bool(weather_empty) is not False:
        return number
    xiang_lin_left_number = number - 1
    xiang_lin_right_number = number + 1
    xiang_lin_left_construction_data = get_hole_construction_datas(tunnel_name, row_id, xiang_lin_left_number)
    xiang_lin_right_construction_data = get_hole_construction_datas(tunnel_name, row_id, xiang_lin_right_number)
    if bool(xiang_lin_left_construction_data) is False:  # 左相邻为空
        shangyi_construction_data = get_hole_construction_datas(tunnel_name, row_id, hole_number)
        # xiang_lin_right_deflection_angle = xiang_lin_right_construction_data['r_deflection_angle']
        xiang_lin_right_rock_section = xiang_lin_right_construction_data['con_see_coal']
        xiang_lin_right_see_ceil = xiang_lin_right_construction_data['con_see_ceil']
        xiang_lin_right_coal_section = xiang_lin_right_see_ceil - xiang_lin_right_rock_section
        xiang_lin_right_hole_depth = xiang_lin_right_construction_data['con_hole_depth']
        xiang_lin_right_design_elevation_angel = xiang_lin_right_construction_data['r_elevation_angle']
        # deflection_angle = 2 * xiang_lin_right_deflection_angle - shangyi_construction_data['r_deflection_angle']
        rock_section = 2 * xiang_lin_right_rock_section - shangyi_construction_data['con_see_coal']
        coal_section = 2 * xiang_lin_right_coal_section - (shangyi_construction_data['con_see_ceil'] -
                                                           shangyi_construction_data['con_see_coal'])
        see_ceil = 2 * xiang_lin_right_see_ceil - shangyi_construction_data['con_see_ceil']
        hole_depth = 2 * xiang_lin_right_hole_depth - shangyi_construction_data['con_hole_depth']
        design_elevation_angel = 2 * xiang_lin_right_design_elevation_angel - \
                                 shangyi_construction_data['r_elevation_angle']
    elif bool(xiang_lin_right_construction_data) is False:  # 右相邻为空
        shangyi_construction_data = get_hole_construction_datas(tunnel_name, row_id, hole_number)
        # xiang_lin_left_deflection_angle = xiang_lin_left_construction_data['r_deflection_angle']
        xiang_lin_left_rock_section = xiang_lin_left_construction_data['con_see_coal']
        xiang_lin_left_see_ceil = xiang_lin_left_construction_data['con_see_ceil']
        xiang_lin_left_coal_section = xiang_lin_left_see_ceil - xiang_lin_left_rock_section
        xiang_lin_left_hole_depth = xiang_lin_left_construction_data['con_hole_depth']
        xiang_lin_left_design_elevation_angel = xiang_lin_left_construction_data['r_elevation_angle']
        # deflection_angle = 2 * xiang_lin_left_deflection_angle - shangyi_construction_data['r_deflection_angle']
        rock_section = 2 * xiang_lin_left_rock_section - shangyi_construction_data['con_see_coal']
        coal_section = 2 * xiang_lin_left_coal_section - (shangyi_construction_data['con_see_ceil'] -
                                                          shangyi_construction_data['con_see_coal'])
        see_ceil = 2 * xiang_lin_left_see_ceil - shangyi_construction_data['con_see_ceil']
        hole_depth = 2 * xiang_lin_left_hole_depth - shangyi_construction_data['con_hole_depth']
        design_elevation_angel = 2 * xiang_lin_left_design_elevation_angel - \
                                 shangyi_construction_data['r_elevation_angle']
    elif bool(xiang_lin_left_construction_data) is False and bool(xiang_lin_right_construction_data) is False:
        print('相邻孔为空无法设计！')

    else:
        # xiang_lin_left_deflection_angle = xiang_lin_left_construction_data['r_deflection_angle']
        xiang_lin_left_rock_section = xiang_lin_left_construction_data['con_see_coal']
        xiang_lin_left_see_ceil = xiang_lin_left_construction_data['con_see_ceil']
        xiang_lin_left_coal_section = xiang_lin_left_see_ceil - xiang_lin_left_rock_section
        xiang_lin_left_hole_depth = xiang_lin_left_construction_data['con_hole_depth']
        xiang_lin_left_design_elevation_angel = xiang_lin_left_construction_data['r_elevation_angle']

        # xiang_lin_right_deflection_angle = xiang_lin_right_construction_data['r_deflection_angle']
        xiang_lin_right_rock_section = xiang_lin_right_construction_data['con_see_coal']
        xiang_lin_right_see_ceil = xiang_lin_right_construction_data['con_see_ceil']
        xiang_lin_right_coal_section = xiang_lin_right_see_ceil - xiang_lin_left_rock_section
        xiang_lin_right_hole_depth = xiang_lin_right_construction_data['con_hole_depth']
        xiang_lin_right_design_elevation_angel = xiang_lin_right_construction_data['r_elevation_angle']

        # deflection_angle = (xiang_lin_left_deflection_angle + xiang_lin_right_deflection_angle) / 2
        rock_section = (xiang_lin_left_rock_section + xiang_lin_right_rock_section) / 2
        coal_section = (xiang_lin_left_coal_section + xiang_lin_right_coal_section) / 2
        see_ceil = (xiang_lin_left_see_ceil + xiang_lin_right_see_ceil) / 2
        hole_depth = (xiang_lin_left_hole_depth + xiang_lin_right_hole_depth) / 2
        design_elevation_angel = (xiang_lin_left_design_elevation_angel + xiang_lin_right_design_elevation_angel) / 2

    # deflection_angle字段暂未使用，默认为0
    my_record2 = Hole_Design(hole_number=number, design_hole_height=design_hole_height, deflection_angle=0,
                             rock_section=rock_section, coal_section=coal_section, see_ceil=see_ceil,
                             hole_depth=hole_depth,
                             row_id=id, design_elevation_angel=design_elevation_angel, single_row=single_row)
    my_record2.save()

    weather_empty1 = get_hole_design_pou_mian_datas(tunnel_name, row_id, number)
    if bool(weather_empty1) is not False:
        return '存在此设计孔剖面信息'
    zuobiao = matching_function(tunnel_name, row_id, number, row_x)
    hole_design_Data = get_hole_design_datas(tunnel_name, row_id, number)
    hole_number_id = hole_design_Data['id']  # 新孔的id
    kai_kong_pou_x = 0
    kai_kong_pou_y = design_hole_height
    # design_jian_mei = jian_zuo_biao(tunnel_name, row_id, number, zuobiao[0], 'rock_section')
    # design_jian_mei_x = design_jian_mei[0]
    # design_jian_mei_y = design_jian_mei[1]
    design_jian_mei_x = format(s * (rock_section + arch_radius) * math.cos((design_elevation_angel / 180) * math.pi),
                               '.2f')
    design_jian_mei_y = format(design_hole_height + (rock_section + arch_radius) *
                               math.sin((design_elevation_angel / 180) * math.pi), '.2f')
    # design_jian_ding = jian_zuo_biao(tunnel_name, row_id, number, zuobiao[0], 'see_ceil')
    # design_jian_ding_x = design_jian_ding[0]
    # design_jian_ding_y = design_jian_ding[1]
    design_jian_ding_x = format(s * (see_ceil + arch_radius) * math.cos((design_elevation_angel / 180) * math.pi),
                                '.2f')
    design_jian_ding_y = format(design_hole_height + (see_ceil + arch_radius) *
                                math.sin((design_elevation_angel / 180) * math.pi), '.2f')
    # design_zhong_kong = jian_zuo_biao(tunnel_name, row_id, number, zuobiao[0], 'hole_depth')
    # design_zhong_kong_x = design_zhong_kong[0]
    # design_zhong_kong_y = design_zhong_kong[1]
    zhong_kong_length = float(chuan_ding_length) + see_ceil  # 终孔长度
    design_zhong_kong_x = format(
        s * (zhong_kong_length + arch_radius) * math.cos((design_elevation_angel / 180) * math.pi), '.2f')
    design_zhong_kong_y = format(design_hole_height + (zhong_kong_length + arch_radius) *
                                 math.sin((design_elevation_angel / 180) * math.pi), '.2f')

    my_record3 = Hole_Design_Pou_Mian(design_jian_mei_x=design_jian_mei_x, design_jian_mei_y=design_jian_mei_y,
                                      design_jian_ding_x=design_jian_ding_x, design_jian_ding_y=design_jian_ding_y,
                                      design_zhong_kong_x=design_zhong_kong_x, design_zhong_kong_y=design_zhong_kong_y,
                                      kai_kong_pou_x=kai_kong_pou_x, kai_kong_pou_y=kai_kong_pou_y,
                                      hole_number_id=hole_number_id)
    my_record3.save()
    return number


def design_jun_pao(tunnel_name, row_id, hole_number):  # 竣工孔坐标
    # row_id = request.Post.get('row_id')
    # hole_number = request.Post.get('hole_number')
    # tunnel_name = request.Post.get('tunnel_id')
    weather_empty = get_jun_pao(tunnel_name, row_id, hole_number)
    if bool(weather_empty) is not False:
        return '存在此竣工孔坐标信息'
    tunnel_Data = get_tunnel_datas(tunnel_name)
    arch_radius = tunnel_Data['arch_radius']
    tunnel_first_hole_number = tunnel_Data['tunnel_first_hole_number']
    first_number = get_numbers(tunnel_first_hole_number)[1]
    work_face_id = tunnel_Data['work_face']
    design_Data = get_hole_design_datas(tunnel_name, row_id, hole_number)
    design_id = design_Data['id']
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']  # 排id
    # 设计孔深 穿顶长度 + 见顶长度
    my_record = Work_face.objects.filter(id=work_face_id).values_list('chuan_ding_length', 'chong_mei_standard')
    chuan_ding_lengths = pd.DataFrame(list(my_record))

    chuan_ding_length = chuan_ding_lengths.iloc[0, 0]
    chuan_ding_length = float(chuan_ding_length)
    chong_mei_standard = chuan_ding_lengths.iloc[0, 1]
    chong_mei_standard = float(chong_mei_standard)

    Data = get_hole_construction_datas(tunnel_name, row_id, hole_number)
    con_see_coal = Data['con_see_coal']  # 施工见煤
    con_see_ceil = Data['con_see_ceil']  # 施工见顶
    r_elevation_angle = Data['r_elevation_angle']
    hole_height = Data['hole_height']
    weight_of_flush_coal = (con_see_ceil - con_see_coal) * chong_mei_standard  # 设计冲煤量

    Hole_Design.objects.filter(id=design_id).update(weight_of_flush_coal=weight_of_flush_coal)

    Hole_design_pou_mian_Data = get_hole_design_pou_mian_datas(tunnel_name, row_id, hole_number)
    jun_pao_kai_x = Hole_design_pou_mian_Data['kai_kong_pou_x']  # 竣工剖面开孔x
    jun_pao_kai_y = Hole_design_pou_mian_Data['kai_kong_pou_y']  # 竣工剖面开孔y
    # 施工见煤坐标

    shi_gong_jian_mei_results = jian_zuo_biao(tunnel_name, row_id, hole_number, jun_pao_kai_x, 'con_see_coal',
                                              jun_pao_kai_x, jun_pao_kai_y, 1)
    # shi_gong_jian_mei_x = shi_gong_jian_mei_results[0]
    # shi_gong_jian_mei_y = shi_gong_jian_mei_results[1]
    number = get_numbers(hole_number)[1]
    s = 1
    if number <= first_number:
        s = -1
    shi_gong_jian_mei_x = format(s * (con_see_coal + arch_radius) * math.cos((r_elevation_angle / 180) * math.pi),
                                 '.2f')
    shi_gong_jian_mei_y = format(hole_height + (con_see_coal + arch_radius) *
                                 math.sin((r_elevation_angle / 180) * math.pi), '.2f')
    # 施工见顶坐标
    shi_gong_jian_ding_results = jian_zuo_biao(tunnel_name, row_id, hole_number, jun_pao_kai_x, 'con_see_ceil',
                                               jun_pao_kai_x, jun_pao_kai_y, 1)
    # shi_gong_jian_ding_x = shi_gong_jian_ding_results[0]
    # shi_gong_jian_ding_y = shi_gong_jian_ding_results[1]
    shi_gong_jian_ding_x = format(s * (con_see_ceil + arch_radius) * math.cos((r_elevation_angle / 180) * math.pi),
                                  '.2f')
    shi_gong_jian_ding_y = format(hole_height + (con_see_ceil + arch_radius) *
                                  math.sin((r_elevation_angle / 180) * math.pi), '.2f')

    # 施工终孔坐标
    shi_gong_zhong_kong_results = jian_zuo_biao(tunnel_name, row_id, hole_number, jun_pao_kai_x, 'con_hole_depth',
                                                jun_pao_kai_x, jun_pao_kai_y, 1)
    # shi_gong_zhong_kong_x = shi_gong_zhong_kong_results[0]
    # shi_gong_zhong_kong_y = shi_gong_zhong_kong_results[1]
    zhong_kong_length = float(chuan_ding_length) + con_see_ceil  # 终孔长度
    shi_gong_zhong_kong_x = format(
        s * (zhong_kong_length + arch_radius) * math.cos((r_elevation_angle / 180) * math.pi), '.2f')
    shi_gong_zhong_kong_y = format(hole_height + (zhong_kong_length + arch_radius) *
                                   math.sin((r_elevation_angle / 180) * math.pi), '.2f')

    my_record2 = jun_pao(jun_pao_row_id=id, jun_pao_hole_num=hole_number, jun_pao_kai_x=jun_pao_kai_x,
                         jun_pao_kai_y=jun_pao_kai_y,
                         jun_pao_see_coal_x=shi_gong_jian_mei_x, jun_pao_see_coal_y=shi_gong_jian_mei_y,
                         jun_pao_see_ceil_x=shi_gong_jian_ding_x,
                         jun_pao_see_ceil_y=shi_gong_jian_ding_y, jun_pao_zhong_kong_x=shi_gong_zhong_kong_x,
                         jun_pao_zhong_kong_y=shi_gong_zhong_kong_y)
    my_record2.save()


def hole_design_estimate(tunnel_name, row_id, hole_number):  # 设计孔评价
    row_Data = get_row_datas(tunnel_name, row_id)
    row_x = row_Data['row_x']
    row_y = row_Data['row_y']
    data1 = get_xie_ya()  # 获取泄压范围
    # 匹配泄压范围
    x_1_xie = data1[data1.iloc[:, 0] < row_x].tail(1).iloc[0, 0]
    x_2_xie = data1[data1.iloc[:, 0] > row_x].head(1).iloc[0, 0]
    y_1_xie = data1[data1.iloc[:, 0] < row_x].tail(1).iloc[0, 1]
    y_2_xie = data1[data1.iloc[:, 0] > row_x].head(1).iloc[0, 1]
    y_xie = y_1_xie + (y_2_xie - y_1_xie) * (row_x - x_1_xie) / (x_2_xie - x_1_xie)
    y_xie_cha = abs(y_xie - row_y)

    you_kai = False  # 是否右侧创建孔

    hole_design_data = get_hole_design_datas(tunnel_name, row_id, hole_number)
    design_elevation_angel = hole_design_data['design_elevation_angel']

    hole_number_id = hole_design_data['id']
    hole_design_pou_mian_data = get_hole_design_pou_mian_datas(tunnel_name, row_id, hole_number)
    design_jian_mei_x = hole_design_pou_mian_data['design_jian_mei_x']
    design_jian_ding_x = hole_design_pou_mian_data['design_jian_ding_x']
    kai_kong_pou_x = hole_design_pou_mian_data['kai_kong_pou_x']

    kong_sub_mei = abs(kai_kong_pou_x - design_jian_mei_x)  # 孔见煤
    kong_sub_ding = abs(kai_kong_pou_x - design_jian_ding_x)  # 孔见顶

    if kong_sub_mei >= y_xie_cha:

        my_record = Hole_Design.objects.filter(id=hole_number_id)
        my_record.delete()
        # 删除左侧孔向右侧设计!!!!!
        you_kai = True
    elif kong_sub_ding >= y_xie_cha:  # （设计 见顶-开孔）≥xie控制范围，修改设计孔孔深
        equal_value = y_xie_cha / math.cos((design_elevation_angel) / 180 * math.pi)
        Hole_Design.objects.filter(hole_number=hole_number, id=hole_number_id).update(see_ceil=equal_value,
                                                                                      hole_depth=equal_value)
    # 都不满足就不修改设计孔
    return you_kai


def shi_gong_xia_estimate(tunnel_name, row_id, hole_number):  # 施工孔下部控制范围评价(一般为首孔右侧)
    row_Data = get_row_datas(tunnel_name, row_id)
    row_x = row_Data['row_x']
    row_y = row_Data['row_y']
    tunnel_Data = get_tunnel_datas(tunnel_name)
    tunnel_first_hole_number = tunnel_Data['tunnel_first_hole_number']
    first_number = get_numbers(tunnel_first_hole_number)[1]
    number = get_numbers(hole_number)[1]  # 获取当前孔号

    data1 = get_chuli_xia()

    # 匹配处理后下部分
    x_1_xia = data1[data1.iloc[:, 0] < row_x].tail(1).iloc[0, 0]
    x_2_xia = data1[data1.iloc[:, 0] > row_x].head(1).iloc[0, 0]
    y_1_xia = data1[data1.iloc[:, 0] < row_x].tail(1).iloc[0, 1]
    y_2_xia = data1[data1.iloc[:, 0] > row_x].head(1).iloc[0, 1]
    y_xia = y_1_xia + (y_2_xia - y_1_xia) * (row_x - x_1_xia) / (x_2_xia - x_1_xia)
    y_xia_cha = abs(y_xia - row_y)

    jun_pao_data = get_jun_pao(tunnel_name, row_id, hole_number)
    jun_pao_kai_x = jun_pao_data['jun_pao_kai_x']  # 竣工开孔剖面坐标x
    jun_pao_see_coal_x = jun_pao_data['jun_pao_see_coal_x']  # 竣工见煤剖面坐标x
    jun_pao_see_ceil_x = jun_pao_data['jun_pao_see_ceil_x']  # 竣工见顶剖面坐标x

    coal_sub_kai = abs(jun_pao_see_coal_x - jun_pao_kai_x)  # 见煤 - 开孔
    ceil_sub_kai = abs(jun_pao_see_ceil_x - jun_pao_kai_x)  # 见顶 - 开孔

    right_number = None
    if number < first_number:
        print("孔号小于首孔号不能评价")
    else:
        if coal_sub_kai < y_xia_cha:
            right_number = design_odd_hole(tunnel_name, row_id, hole_number)
        else:
            print("不再设计新孔, 设计偶数孔")
            right_number = design_even_hole(tunnel_name, row_id, first_number)
    return right_number


def ping_jia_shi_gong_kong(tunnel_name, row_id, hole_number):  # 评价施工孔控制范围
    row_Data = get_row_datas(tunnel_name, row_id)
    row_x = row_Data['row_x']
    row_y = row_Data['row_y']
    id = row_Data['id']
    tunnel_Data = get_tunnel_datas(tunnel_name)

    tunnel_first_hole_number = tunnel_Data['tunnel_first_hole_number']
    first_number = get_numbers(tunnel_first_hole_number)[1]

    hole_Data = get_jun_pao(tunnel_name, row_id, hole_number)
    jun_pao_see_coal_x = hole_Data['jun_pao_see_coal_x']  # 竣工见煤剖面坐标x
    jun_pao_kai_x = hole_Data['jun_pao_kai_x']  # 竣工开孔剖面坐标y
    jun_pao_see_ceil_x = hole_Data['jun_pao_see_ceil_x']  # 竣工见顶剖面坐标x
    coal_sub_kai_x = abs(jun_pao_see_coal_x - jun_pao_kai_x)  # 见煤 - 开孔
    ceil_sub_kai_x = abs(jun_pao_see_ceil_x - jun_pao_kai_x)  # 见顶 - 开孔

    data1 = get_chuli_shang()
    x_1_shang = data1[data1.iloc[:, 0] < row_x].tail(1).iloc[0, 0]
    x_2_shang = data1[data1.iloc[:, 0] > row_x].head(1).iloc[0, 0]
    y_1_shang = data1[data1.iloc[:, 0] < row_x].tail(1).iloc[0, 1]
    y_2_shang = data1[data1.iloc[:, 0] > row_x].head(1).iloc[0, 1]
    y_shang = y_1_shang + (y_2_shang - y_1_shang) * (row_x - x_1_shang) / (x_2_shang - x_1_shang)
    y_shang_cha = abs(y_shang - row_y)

    data3 = get_xie_ya()
    x_1_xie = data3[data3.iloc[:, 0] < row_x].tail(1).iloc[0, 0]
    x_2_xie = data3[data3.iloc[:, 0] > row_x].head(1).iloc[0, 0]
    y_1_xie = data3[data3.iloc[:, 0] < row_x].tail(1).iloc[0, 1]
    y_2_xie = data3[data3.iloc[:, 0] > row_x].head(1).iloc[0, 1]
    y_xie = y_1_xie + (y_2_xie - y_1_xie) * (row_x - x_1_xie) / (x_2_xie - x_1_xie)
    y_xie_cha = abs(y_xie - row_y)

    left_number = None
    right_number = tunnel_first_hole_number

    number = get_numbers(hole_number)[1]  # 获取当前孔号
    if number <= first_number:  # 孔号小于首孔号
        if coal_sub_kai_x >= y_shang_cha and ceil_sub_kai_x >= y_xie_cha:  # 向右侧创建
            if number % 2 == 0:
                right_number = design_even_hole(tunnel_name, row_id, first_number, pan_duan=True)
                left_number = hole_number
            else:
                right_number = design_odd_hole(tunnel_name, row_id, first_number, pan_duan=True)
                left_number = hole_number
            return right_number
            ping_jia_design = hole_design_estimate(tunnel_name, row_id, right_number)  # 设计孔评价
            if ping_jia_design == True:  # 首次向右侧创建失败    you_kai = True
                left_number = hole_number
                right_number = tunnel_first_hole_number
        else:  # 继续左侧创建
            left_number = design_odd_hole(tunnel_name, row_id, hole_number)
            ping_jia_design = hole_design_estimate(tunnel_name, row_id, left_number)  # 设计孔评价
            if ping_jia_design == True:  # 是否创建失败
                left_number = hole_number
                right_number = first_number
                print("此时需要向右侧创建孔")
    else:  # 孔号大于首孔号
        # 找出最左侧孔号
        my_record = Hole_Construction.objects.filter(row_id=id).values_list('h_c_number')
        all_number = pd.DataFrame(list(my_record))
        number_list = []
        for i in range(len(all_number)):  # 所有孔号数字提取
            s = int(all_number.loc[i, 0])
            s = get_numbers(s)[1]
            number_list.append(s)
        number_list.sort()  # 排序
        left_number = number_list[0]  # 最左侧孔号
        # 对施工孔进行评价 与设计孔评价不同 包含有对新设计孔创建
        ping_jia_shi_gong = shi_gong_xia_estimate(tunnel_name, row_id, hole_number)
        right_number = number

    return left_number, right_number


def zuan_kong_quality_estimate(tunnel_name, row_id, hole_number):  # 钻孔施工质量评价 见止煤误差(单孔评价)
    # 数字提取
    number = get_numbers(hole_number)[1]  # 当前钻孔数字
    tunnel_Data = get_tunnel_datas(tunnel_name)
    arch_radius = tunnel_Data['arch_radius']  # 弓形半径
    mei_ceng_qing_jiao = tunnel_Data['mei_ceng_qing_jiao']
    tunnel_first_hole_number = tunnel_Data['tunnel_first_hole_number']  # 这一排的首孔号
    first_number = get_numbers(tunnel_first_hole_number)[1]
    first_hole_design_Data = get_hole_design_datas(tunnel_name, row_id, first_number)
    first_coal_section = first_hole_design_Data['coal_section']  # 首孔设计煤段
    first_rock_section = first_hole_design_Data['rock_section']  # 首孔设计见煤

    first_hole_Construction_Data = get_hole_construction_datas(tunnel_name, row_id, first_number)
    first_hole_Construction_con_see_coal = first_hole_Construction_Data['con_see_coal']  # 首孔施工见煤
    first_hole_Construction_con_see_ceil = first_hole_Construction_Data['con_see_ceil']  # 首孔施工见顶

    Row_Data = get_row_datas(tunnel_name, row_id)
    id = Row_Data['id']

    hole_design_Data = get_hole_design_datas(tunnel_name, row_id, hole_number)
    hole_construction_Data = get_hole_construction_datas(tunnel_name, row_id, hole_number)

    mei_duan_length = hole_construction_Data['con_see_ceil'] - hole_construction_Data['con_see_coal']  # 煤段长度
    if number > first_number:
        s = 1
    else:
        s = -1  # 判断当前孔在首孔哪一侧

    judgment = abs(math.asin((first_hole_Construction_con_see_coal - first_hole_Construction_con_see_ceil +
                              first_coal_section) * math.cos(math.radians(mei_ceng_qing_jiao)) / 2 / (
                                 mei_duan_length)) * 180 / math.pi) - mei_ceng_qing_jiao * s

    mei_ceng_qing_jiao_sin = math.radians(90 + s * mei_ceng_qing_jiao)
    yan_daun_angle = math.asin(
        (first_hole_Construction_con_see_coal + first_rock_section + 2 * arch_radius) / 2 * math.sin(
            mei_ceng_qing_jiao_sin) / (hole_construction_Data['con_see_coal'] + arch_radius)) * 180 / math.pi
    judgment1 = yan_daun_angle + s * mei_ceng_qing_jiao

    if abs(hole_construction_Data['con_see_coal'] - hole_design_Data['rock_section']) <= 5 and \
            abs(hole_construction_Data['con_see_ceil'] - hole_design_Data['con_see_ceil']) <= 5:

        my_record = Hole_Eval(see_coal_eval='见煤合格', see_ceil_eval='见顶合格', h_name=hole_number, row_id=id)
        my_record.save()

    elif abs(hole_construction_Data['con_see_coal'] - hole_design_Data['rock_section']) > 5 and \
            abs(hole_construction_Data['con_see_ceil'] - hole_design_Data['see_ceil']) > 5:

        try:
            if abs(judgment - judgment1) >= 2:
                my_record1 = Hole_Eval(see_coal_eval='钻孔偏斜', see_ceil_eval='钻孔偏斜', h_name=hole_number, row_id=id)
                my_record1.save()
                new_number = design_repair_hole(tunnel_name, row_id, hole_number)[0]
            elif abs(judgment - judgment1) < 2 and abs(judgment1 - hole_construction_Data['r_elevation_angle']) < 2:
                my_record3 = Hole_Eval(see_coal_eval='有断层', see_ceil_eval='有断层', h_name=hole_number, row_id=id)
                my_record3.save()
                new_number = design_repair_hole(tunnel_name, row_id, hole_number)[0]
            elif abs(judgment - judgment1) < 2 and abs(judgment1 - hole_construction_Data['r_elevation_angle']) >= 2:
                my_record2 = Hole_Eval(see_coal_eval='施工倾角误差大，为：' + str(judgment) + '°',
                                       see_ceil_eval='施工倾角误差大，为：' + str(judgment) + '°',
                                       h_name=hole_number, row_id=id)
                my_record2.save()
                new_number = design_repair_hole(tunnel_name, row_id, hole_number)[0]

        except:
            my_record3 = Hole_Eval(see_coal_eval='有断层', see_ceil_eval='有断层', h_name=hole_number, row_id=id)
            my_record3.save()
            new_number = design_repair_hole(tunnel_name, row_id, hole_number)[0]

    else:
        my_record4 = Hole_Eval(see_coal_eval='有断层', see_ceil_eval='有断层', h_name=hole_number, row_id=id)
        my_record4.save()

        new_number = design_repair_hole(tunnel_name, row_id, hole_number)[0]

    return new_number


def design_repair_hole(tunnel_name, row_id, hole_number):  # 设计补孔 hole_number 为不合格孔
    tunnel_Data = get_tunnel_datas(tunnel_name)
    design_data = get_hole_design_datas(tunnel_name, row_id, hole_number)
    hole_design_pou_mian_data = get_hole_design_pou_mian_datas(tunnel_name, row_id, hole_number)
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']
    arch_radius = tunnel_Data['arch_radius']
    chuan_ding_length = 0.5
    hole_height = tunnel_Data['hole_height']
    single_row = design_data['single_row']  # 单排列数
    single_row = int(single_row)
    number_datas = get_numbers(hole_number)  # 获得不合格孔的孔号信息
    number = number_datas[1]  # 孔号
    new_number = None
    my_record = Hole_Construction.objects.filter(row_id=id).values_list('h_c_number')
    all_number = pd.DataFrame(list(my_record))
    # 所有孔号数字提取
    number_list = []
    for i in range(len(all_number)):
        s = int(all_number.loc[i, 0])
        s = get_numbers(s)[1]
        number_list.append(s)
    # 排序
    number_list.sort()
    # 最右侧孔号
    right_number = number_list[-1]
    # 相邻施工孔孔号：此孔好+单排列数是否大于最右侧孔号
    if number + single_row > right_number:
        xiang_lin_number = number - single_row
    else:
        xiang_lin_number = number + single_row

    xiang_lin_construction_Data = get_hole_construction_datas(tunnel_name, row_id, xiang_lin_number)  # 相邻孔施工信息
    xiang_lin_jun_pao = get_jun_pao(tunnel_name, row_id, xiang_lin_number)  # 相邻孔信息

    tunnel_data = get_tunnel_datas(tunnel_name)
    mei_ceng_qing_jiao = tunnel_data['mei_ceng_qing_jiao']  # 煤层倾角
    # 如果上一孔为补孔
    if number_datas[0] is True:
        fen_number = number_datas[2] + 1
        new_number = 'B' + str(number) + '-' + str(fen_number)
        number_hole_construction_Data = get_hole_construction_datas(tunnel_name, row_id, hole_number)  # 不合格孔施工信息
        number_jun_pao = get_jun_pao(tunnel_name, row_id, hole_number)  # 不合格孔坐标信息
    # 上一孔不是补孔
    else:
        fen_number = 1
        new_number = 'B' + str(number) + '-' + str(fen_number)
        number_hole_construction_Data = get_hole_construction_datas(tunnel_name, row_id, number)  # 不合格孔施工信息
        number_jun_pao = get_jun_pao(tunnel_name, row_id, number)  # 不合格孔坐标信息
    weather_empty = get_jun_pao(tunnel_name, row_id, new_number)
    # 判断竣工坐标信息是否存在，存在则结束
    if bool(weather_empty) is not False:
        print('存在此竣工孔坐标信息')
        return new_number
    hole_eval_data = get_hole_eval(tunnel_name, row_id, hole_number)  # 评价孔信息
    # 根据评价不同设置不同设计孔信息
    if hole_eval_data['see_coal_eval'] == '有断层' and hole_eval_data['see_ceil_eval'] == '有断层':
        design_hole_height = 0.75 * number_hole_construction_Data['hole_height'] + \
                             0.25 * xiang_lin_construction_Data['hole_height']

        deflection_angle = 0.75 * number_hole_construction_Data['r_deflection_angle'] \
                           + 0.25 * xiang_lin_construction_Data['r_deflection_angle']

        design_elevation_angel = 0.75 * number_hole_construction_Data['r_elevation_angle'] \
                                 + 0.25 * xiang_lin_construction_Data['r_elevation_angle']

        coal_section = 0.75 * number_hole_construction_Data['con_see_coal'] \
                       + 0.25 * xiang_lin_construction_Data['con_see_coal']
        see_ceil = 0.75 * number_hole_construction_Data['con_see_ceil'] \
                   + 0.25 * xiang_lin_construction_Data['con_see_ceil']
        hole_depth = 0.75 * number_hole_construction_Data['con_hole_depth'] \
                     + 0.25 * xiang_lin_construction_Data['con_hole_depth']

        rock_section = see_ceil - coal_section

        my_record1 = Hole_Design(hole_number=new_number, design_hole_height=design_hole_height,
                                 deflection_angle=deflection_angle,
                                 rock_section=rock_section, coal_section=coal_section, see_ceil=see_ceil,
                                 hole_depth=hole_depth,
                                 row_id=id, design_elevation_angel=design_elevation_angel, single_row=single_row)
        my_record1.save()


    elif '施工倾角误差大' in hole_eval_data['see_coal_eval'] and '施工倾角误差大' in hole_eval_data['see_ceil_eval']:
        design_hole_height = design_data['design_hole_height']
        deflection_angle = design_data['deflection_angle']
        design_elevation_angel = design_data['design_elevation_angel']
        rock_section = design_data['rock_section']
        coal_section = design_data['coal_section']
        see_ceil = design_data['see_ceil']
        hole_depth = design_data['hole_depth']

        my_record2 = Hole_Design(hole_number=new_number, design_hole_height=design_hole_height,
                                 deflection_angle=deflection_angle,
                                 rock_section=rock_section, coal_section=coal_section, see_ceil=see_ceil,
                                 hole_depth=hole_depth,
                                 row_id=id, design_elevation_angel=design_elevation_angel, single_row=single_row)
        my_record2.save()

    elif hole_eval_data['see_coal_eval'] == '钻孔偏斜' and hole_eval_data['see_ceil_eval'] == '钻孔偏斜':
        design_hole_height = design_data['design_hole_height']
        deflection_angle = design_data['deflection_angle']
        rock_section = design_data['rock_section']
        a = hole_design_pou_mian_data['design_jian_ding_x']
        b = number_jun_pao['jun_pao_see_ceil_y'] + (number_jun_pao['jun_pao_see_ceil_x'] - a) \
            * math.sin(math_function_transform(mei_ceng_qing_jiao))

        design_elevation_angel = math.degrees(math.atan(
            (b - hole_design_pou_mian_data['kai_kong_pou_y']) / (a - hole_design_pou_mian_data['kai_kong_pou_x'])))

        see_ceil = design_data['see_ceil'] * math.cos(math.radians(design_data['design_elevation_angel'])) / \
                   math.cos(math.radians(number_hole_construction_Data['r_elevation_angle']))
        coal_section = design_data['coal_section'] * math.cos(math.radians(design_data['design_elevation_angel'])) / \
                       math.cos(math.radians(number_hole_construction_Data['r_elevation_angle']))
        hole_depth = see_ceil + 1

        my_record3 = Hole_Design(hole_number=new_number, design_hole_height=design_hole_height,
                                 deflection_angle=deflection_angle,
                                 rock_section=rock_section, coal_section=coal_section, see_ceil=see_ceil,
                                 hole_depth=hole_depth,
                                 row_id=id, design_elevation_angel=design_elevation_angel, single_row=single_row)
        my_record3.save()

    weather_empty1 = get_hole_design_pou_mian_datas(tunnel_name, row_id, new_number)
    # 判断设计孔剖面信息是否为空，为空结束
    if bool(weather_empty1) is not False:
        print('存在此设计孔剖面信息')
        return new_number
    rock_section = see_ceil - coal_section  # 设计岩段 = 见煤长度
    design_hole_height = tunnel_Data['hole_height']  # 设计孔高度

    hole_design_Data = get_hole_design_datas(tunnel_name, row_id, new_number)
    hole_number_id = hole_design_Data['id']  # 新孔的id
    new_design_kai_kong_x = 0
    new_design_kai_kong_y = hole_height
    new_design_jian_mei_x = format(
        s * (rock_section + arch_radius) * math.cos((design_elevation_angel / 180) * math.pi), '.2f')
    new_design_jian_mei_y = format(design_hole_height + (rock_section + arch_radius) *
                                   math.sin((design_elevation_angel / 180) * math.pi), '.2f')

    new_design_jian_ding_x = format(
        s * (see_ceil + arch_radius) * math.cos((design_elevation_angel / 180) * math.pi), '.2f')
    new_design_jian_ding_y = format(design_hole_height + (see_ceil + arch_radius) *
                                    math.sin((design_elevation_angel / 180) * math.pi), '.2f')

    zhong_kong_length = float(chuan_ding_length) + see_ceil  # 终孔长度
    new_design_zhong_kong_x = format(
        s * (zhong_kong_length + arch_radius) * math.cos((design_elevation_angel / 180) * math.pi), '.2f')
    new_design_zhong_kong_y = format(design_hole_height + (zhong_kong_length + arch_radius) *
                                     math.sin((design_elevation_angel / 180) * math.pi), '.2f')

    my_record4 = Hole_Design_Pou_Mian(design_jian_mei_x=new_design_jian_mei_x, design_jian_mei_y=new_design_jian_mei_y,
                                      design_jian_ding_x=new_design_jian_ding_x,
                                      design_jian_ding_y=new_design_jian_ding_y,
                                      design_zhong_kong_x=new_design_zhong_kong_x,
                                      design_zhong_kong_y=new_design_zhong_kong_y,
                                      kai_kong_pou_x=new_design_kai_kong_x, kai_kong_pou_y=new_design_kai_kong_y,
                                      hole_number_id=hole_number_id)
    my_record4.save()
    return new_number


# print(design_even_hole('16071工作面上部底板巷', 15, 2))
# print(design_jun_pao('16071工作面上部底板巷', 15, 2))
# print(ping_jia_shi_gong_kong('16071工作面上部底板巷', 15, 2))
# print(hole_design_estimate())
# get_hole_design_datas('16071工作面上部底板巷', 15, 3)

# list_data = matching_function('160701工作面中部底板巷', 15, 11, 194.05673913043478)
# print(list_data)

# number = design_first_hole('160701工作面中部底板巷', 15)
# number = design_odd_hole('160701工作面中部底板巷', 15, 11)
# print(number)
# design_jun_pao('160701工作面中部底板巷', 15, 9)
# design_even_hole('160701工作面中部底板巷', 15, 11)

# number = hole_design_estimate('160701工作面中部底板巷', 15, 11)

# new_number = zuan_kong_quality_estimate('160701工作面中部底板巷', 15, 9)
# print("debug inform:", new_number)


hole_data = Hole_Design.objects.all()

hole_list = []

for item in hole_data:
    hole_list.append(model_to_dict(item))

for item in range(len(hole_list)):
    print(hole_list[item]["hole_number"])