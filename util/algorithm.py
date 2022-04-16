import math
import os
import re
import sys

import django
import pymysql

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Django.settings")

django.setup()  # 加载项目配置

from Mining.models import *

import pandas as pd
from django.forms import model_to_dict

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Django.settings")
django.setup()  # 加载项目配置


def get_mine_datas(mine_name):
    Datas = Mine.objects.filter(mine_name=mine_name).first()
    if Datas is not None:
        Data = model_to_dict(Datas)
    else:
        Data = {}
    return Data


def get_work_datas(mine_name):
    mine_data = get_mine_datas(mine_name)
    mine_id = mine_data['id']
    Datas = Work_face.objects.filter(mine_id=mine_id).first()
    if Datas is not None:
        Data = model_to_dict(Datas)
    else:
        Data = {}
    return Data


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
    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_insert = "UPDATE hpu_mining.row SET current_tunnel_depth = %s " \
                 "WHERE ( tunnel_id = %s and row_id = %s)"
    cur.execute(sql_insert, (current_tunnel_depth, tunnel_id, row_id))
    db.commit()
    db.close()
    return current_tunnel_depth


# 获取底板巷修正后顶板坐标
def get_di_ban_hang():
    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql = "select di_I_x,  di_J_Z from di_ban_hang_xiuzheng_ding_ban"
    cur.execute(sql)
    result = cur.fetchall()
    di_hang_result = pd.DataFrame(list(result))
    return di_hang_result


# 获取修正后煤层底板坐标
def get_mei_di():
    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql = "select xiu_zheng_x,  xiu_zheng_z from xiu_zheng_hou_meiceng_di_ban"
    cur.execute(sql)
    result = cur.fetchall()
    mei_di_result = pd.DataFrame(list(result))
    return mei_di_result


# 获取修正后煤层顶板坐标
def get_mei_ding():
    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql = "select Xiu_x,  xiu_z from xiu_zheng_mei_ceng_ding_ban"
    cur.execute(sql)
    result = cur.fetchall()
    mei_ding_result = pd.DataFrame(list(result))
    return mei_ding_result


# 获取处理后上部分
def get_chuli_shang():
    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql = "select Chu_li_shang_x, Chu_li_shang_y from ping_mian_zuo_biao_kong_zhi"
    cur.execute(sql)
    result = cur.fetchall()
    chuli_shang_result = pd.DataFrame(list(result))
    return chuli_shang_result


# 获取处理后下部分
def get_chuli_xia():
    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql = "select Chu_li_xia_x, Chu_li_xia_y from ping_mian_zuo_biao_kong_zhi_xia"
    cur.execute(sql)
    result = cur.fetchall()
    chuli_shang_result = pd.DataFrame(list(result))
    return chuli_shang_result


# 获取泄压范围
def get_xie_ya():
    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql = "select Xie_ya_x, Xie_ya_y from xie_ya_fan_wei"
    cur.execute(sql)
    result = cur.fetchall()
    xie_ya_result = pd.DataFrame(list(result))
    return xie_ya_result


# 获取设计孔数据
def get_hole_design_datas(tunnel_name, row_id, hole_number):
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']
    Datas = Hole_Design.objects.filter(row_id=id, hole_number=hole_number).first()
    if Datas is not None:
        Data = model_to_dict(Datas)
    else:
        Data = {}
    return Data


# 施工孔号获取施工孔数据
def get_hole_construction_datas(tunnel_name, row_id, h_c_number):
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']
    Datas = Hole_Construction.objects.filter(row_id=id, h_c_number=h_c_number).first()
    if Datas is not None:
        Data = model_to_dict(Datas)
    else:
        Data = {}
    return Data


# 获取钻孔质量评价
def get_hole_eval_datas(tunnel_name, row_id, hole_number):
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']
    Datas = Hole_Eval.objects.filter(row_id=id, h_name=hole_number).first()
    if Datas is not None:
        Data = model_to_dict(Datas)
    else:
        Data = {}
    return Data


# 通过id和孔号获取竣工开孔数据
def get_jun_pao(tunnel_name, row_id, jun_pao_hole_num):
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']
    Datas = jun_pao.objects.filter(jun_pao_row=id, jun_pao_hole_num=jun_pao_hole_num).first()
    if Datas is not None:
        Data = model_to_dict(Datas)
    else:
        Data = {}
    return Data


# 通过id 获取设计孔剖面数据
def get_hole_design_pou_mian_datas(tunnel_name, row_id, hole_number):
    design_data = get_hole_design_datas(tunnel_name, row_id, hole_number)
    id = design_data['id']
    Datas = Hole_Design_Pou_Mian.objects.filter(hole_number_id=id).first()
    if Datas is not None:
        Data = model_to_dict(Datas)
    else:
        Data = {}
    return Data


# 获取评价孔
def get_hole_eval(tunnel_name, row_id, h_name):
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']
    Datas = Hole_Eval.objects.filter(row=id, h_name=h_name).first()
    if Datas is not None:
        Data = model_to_dict(Datas)
    else:
        Data = {}
    return Data


# 通过巷道号排号孔号奇偶与x求y和z,只适用于首孔
def matching_function(tunnel_name, row_id, hole_number, x):
    number = get_numbers(hole_number)[1]  # 提取数字
    tunnel_Data = get_tunnel_datas(tunnel_name)
    row_Data = get_row_datas(tunnel_name, row_id)
    id = row_Data['id']
    current_tunnel_depth = row_Data['current_tunnel_depth']
    tunnel_length = tunnel_Data['tunnel_length']

    data1 = get_di_ban_hang()
    data2 = get_mei_ding()
    data3 = get_mei_di()
    # 判断在不在范围内，不在范围内结束程序
    if x < data1.iloc[0, 0] or x > data1.iloc[-1, 0]:
        print('不在修正底板巷范围内！')
        return False
        os._exit(0)
    elif x < data2.iloc[0, 0] or x > data2.iloc[-1, 0]:
        return print('不在修正煤顶范围内！')
        return False
        os._exit(0)
    elif x < data3.iloc[0, 0] or x > data3.iloc[-1, 0]:
        print('不在修正煤底范围内！')
        return False
        os._exit(0)
    else:
        # (x1, z1) 和 (x2, z2) 分别为上下相邻两个坐标点
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
        db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
        cur = db.cursor()
        sql_select = 'select design_hole_height from hpu_mining.hole_design where row_id = %s'
        cur.execute(sql_select, id)
        design_hole_heights = pd.DataFrame(cur.fetchall())
        # 如果设计孔高为空赋值1.2
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

    # 判断为施工孔还是设计孔，当pan_duan为空时为设计孔
    if pan_duan == None:
        hole_design_Data = get_hole_design_datas(tunnel_name, row_id, hole_number)
        y = hole_design_Data[iloc_name]
        design_elevation_angel = hole_design_Data['design_elevation_angel']  # 钻孔仰角
    else:  # 施工孔
        hole_construction_Data = get_hole_construction_datas(tunnel_name, row_id, hole_number)
        y = hole_construction_Data[iloc_name]
        design_elevation_angel = hole_construction_Data['r_elevation_angle']

    shou_kong_number = get_numbers(tunnel_first_hole_number)[1]  # 首孔号数字提取
    s = 1
    # 左右判定 左-1，右1
    if number < shou_kong_number:
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


# 目前没用
def get_kai_kong_zuo_biao(tunnel_name, row_id, hole_number):
    row_Data = get_row_datas(tunnel_name, row_id)
    id = row_Data['id']
    current_tunnel_depth = row_Data['current_tunnel_depth']
    tunnel_Data = get_tunnel_datas(tunnel_name)
    tunnel_length = tunnel_Data['tunnel_length']
    di_ban_hang_hight = tunnel_Data['di_ban_hang_hight']
    qi_dian_x = tunnel_Data['di_ban_tunnel_qi_dian_x']  # 起点坐标
    qi_dian_y = tunnel_Data['di_ban_tunnel_qi_dian_y']
    zhong_dian_x = tunnel_Data['di_ban_tunnel_zhong_dian_x']  # 终点坐标
    zhong_dian_y = tunnel_Data['di_ban_tunnel_zhong_dian_y']

    design_hole_data = get_hole_design_datas(tunnel_name, row_id, hole_number)
    design_hole_height = design_hole_data['design_hole_height']

    x = qi_dian_x + (current_tunnel_depth / tunnel_length) * (zhong_dian_x - qi_dian_x)
    y = qi_dian_y + (current_tunnel_depth / tunnel_length) * (zhong_dian_y - qi_dian_y)
    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_insert = 'update hpu_mining.row set row_x = %s, row_y = %s where id ="%s"'

    cur.execute(sql_insert, (x, y, id))
    db.commit()
    db.close()
    data1 = get_di_ban_hang()
    data2 = get_mei_ding()
    data3 = get_mei_di()
    # 1:底板巷修正后顶板坐标
    x_1_hang = data1[data1.iloc[:, 0] <= x].tail(1).iloc[0, 0]
    x_2_hang = data1[data1.iloc[:, 0] > x].head(1).iloc[0, 0]
    z_1_hang = data1[data1.iloc[:, 0] <= x].tail(1).iloc[0, 1]
    z_2_hang = data1[data1.iloc[:, 0] > x].head(1).iloc[0, 1]
    z_hang = z_1_hang + (z_2_hang - z_1_hang) * (x - x_1_hang) / (x_2_hang - x_1_hang)

    # 2：修正后煤层顶板坐标
    x_1_ding = data2[data2.iloc[:, 0] <= x].tail(1).iloc[0, 0]
    x_2_ding = data2[data2.iloc[:, 0] > x].head(1).iloc[0, 0]
    z_1_ding = data2[data2.iloc[:, 0] <= x].tail(1).iloc[0, 1]
    z_2_ding = data2[data2.iloc[:, 0] > x].head(1).iloc[0, 1]
    z_ding = z_1_ding + (z_2_ding - z_1_ding) * (x - x_1_ding) / (x_2_ding - x_1_ding)

    # 3：修正后煤层底板坐标
    x_1_di = data3[data3.iloc[:, 0] < x].tail(1).iloc[0, 0]
    x_2_di = data3[data3.iloc[:, 0] > x].head(1).iloc[0, 0]
    z_1_di = data3[data3.iloc[:, 0] < x].tail(1).iloc[0, 1]
    z_2_di = data3[data3.iloc[:, 0] > x].head(1).iloc[0, 1]
    z_di = z_1_di + (z_2_di - z_1_di) * (x - x_1_di) / (x_2_di - x_1_di)

    #   求z坐标 z巷 - 3.3(底板巷巷道高度) +1.2
    z = z_hang - di_ban_hang_hight + design_hole_height

    #   求岩柱厚度
    pillar_thickness = z_di - z_hang

    #   求煤层厚度
    coal_seam_thickness = z_ding - z_di
    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_insert = 'update hpu_mining.row set row_z = %s, pillar_thickness = %s, ' \
                 'coal_seam_thickness = %s where id = %s'
    cur.execute(sql_insert, (z, pillar_thickness, coal_seam_thickness, id))
    db.commit()
    db.close()
    return z, pillar_thickness, coal_seam_thickness


# 设计首孔
def design_first_hole(tunnel_name, row_id):
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
    # 如果存在此设计孔信息则结束程序
    if bool(weather_empty) is not False:
        return '存在此设计孔'
        os._exit(0)
    zuobiao = matching_function(tunnel_name, row_id, number, row_x)
    # 用匹配函数匹配不在范围内结束程序
    if zuobiao is False:
        print('匹配错误！')
        os._exit(0)
    rock_section = zuobiao[4]  # 设计岩段
    coal_section = zuobiao[5]  # 设计煤段
    see_ceil = coal_section + rock_section
    coal_seam_thickness = zuobiao[5]  # 煤层厚度

    # 设计孔深 穿顶长度 + 见顶长度
    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_select_chuan_ding = "select work_face.chuan_ding_length, work_face.chong_mei_standard " \
                            "from work_face where id = %s"
    cur.execute(sql_select_chuan_ding, work_face_id)
    chuan_ding_lengths = cur.fetchall()
    chuan_ding_lengths = pd.DataFrame(list(chuan_ding_lengths))

    chuan_ding_length = chuan_ding_lengths.iloc[0, 0]

    chong_mei_standards = chuan_ding_lengths.iloc[0, 1]
    db.close()

    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_insert_coal_seam_thickness = 'update hpu_mining.row set coal_seam_thickness = %s where row_id = %s'
    cur.execute(sql_insert_coal_seam_thickness, (coal_seam_thickness, row_id))
    db.commit()

    hole_depth = see_ceil + float(chuan_ding_length)

    design_hole_height = tunnel_Data['hole_height']  # 设计孔高度
    db.close()
    single_row = 2

    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_insert = "insert into hpu_mining.hole_design (hole_number, design_hole_height," \
                 " deflection_angle, rock_section, coal_section, see_ceil, hole_depth, row_id," \
                 " design_elevation_angel, single_row) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cur.execute(sql_insert, (number, design_hole_height, deflection_angle,
                             rock_section, coal_section, see_ceil, hole_depth,
                             id, design_elevation_angel, single_row))

    db.commit()
    db.close()
    weather_empty1 = get_hole_design_pou_mian_datas(tunnel_name, row_id, number)
    # 存在此设计孔的剖面信息则结束程序
    if bool(weather_empty1) is not False:
        return '存在此设计孔剖面信息'
        os._exit(0)
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

    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
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
    # 存在此设计孔信息则结束
    if bool(weather_empty) is not False:
        return number
        os._exit(0)
    zuobiao = matching_function(tunnel_name, row_id, number, row_x)
    # 匹配函数不在范围内结束
    if zuobiao is False:
        print('匹配错误！')
        os._exit(0)
    rock_section = zuobiao[4]  # 设计岩段
    coal_section = zuobiao[5]  # 设计煤段
    see_ceil = coal_section + rock_section
    coal_seam_thickness = zuobiao[5]  # 煤层厚度
    # 设计孔深 穿顶长度 + 见顶长度
    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_select_chuan_ding = "select work_face.chuan_ding_length, work_face.chong_mei_standard " \
                            "from work_face where id = %s"
    cur.execute(sql_select_chuan_ding, work_face_id)
    chuan_ding_lengths = cur.fetchall()
    chuan_ding_lengths = pd.DataFrame(list(chuan_ding_lengths))

    chuan_ding_length = chuan_ding_lengths.iloc[0, 0]

    chong_mei_standards = chuan_ding_lengths.iloc[0, 1]
    db.close()

    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
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
    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
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
    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
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
    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_select_chuan_ding = "select work_face.chuan_ding_length, work_face.chong_mei_standard " \
                            "from work_face where id = %s"
    cur.execute(sql_select_chuan_ding, work_face_id)
    chuan_ding_lengths = cur.fetchall()
    chuan_ding_lengths = pd.DataFrame(list(chuan_ding_lengths))

    chuan_ding_length = chuan_ding_lengths.iloc[0, 0]

    chong_mei_standards = chuan_ding_lengths.iloc[0, 1]

    db.close()

    number = get_numbers(hole_number)[1]  # 上一孔号
    first_hole_number = get_numbers(tunnel_first_hole_number)[1]  # 首孔号
    # 如果pan_duan为True 说明此时需要向右边创建孔，新孔
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
    # 存在设计孔信息则结束
    if bool(weather_empty) is not False:
        return new_number
        os._exit(0)
    deflection_angle = 0  # 设计偏角

    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_select_h_c_number = 'select  r_elevation_angle, con_see_coal, con_see_ceil, ' \
                            'con_hole_depth from Hole_Construction where h_c_number = %s ' \
                            'and row_id = %s'
    cur.execute(sql_select_h_c_number, (hole_number, id))
    shang_kong_results = cur.fetchall()
    shang_kong = pd.DataFrame(list(shang_kong_results))  # 上一个孔的信息
    db.close()

    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_select_jun_pao_hole_num = 'select jun_pao_see_ceil_x, jun_pao_see_ceil_y from hpu_mining.jun_pao ' \
                                  'where jun_pao_row_id = %s and jun_pao_hole_num = %s'
    cur.execute(sql_select_jun_pao_hole_num, (id, hole_number))
    shang_yi_kong_results = cur.fetchall()
    shang_yi_kong = pd.DataFrame(list(shang_yi_kong_results))  # 上一孔需要坐标

    db.close()
    zuan_kong_jia_jiao = format(math.asin(zuan_kong_chui_ju /
                                          (arch_radius + float(shang_kong.iloc[0, 3]))) * 180 / math.pi, '.1f')  # 钻孔夹角

    # 设计仰角
    design_elevation_angel = format(float(shang_kong.iloc[0, 0]) - (float(zuan_kong_jia_jiao) - s * 0.1), '.1f')
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

    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_insert = "insert into hpu_mining.hole_design (hole_number, design_hole_height," \
                 " deflection_angle, rock_section, coal_section, see_ceil, hole_depth, row_id," \
                 " design_elevation_angel, single_row) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cur.execute(sql_insert, (new_number, design_hole_height, deflection_angle,
                             rock_section, coal_section, see_ceil, hole_depth,
                             id, design_elevation_angel, single_row))

    db.commit()
    db.close()
    weather_empty1 = get_hole_design_pou_mian_datas(tunnel_name, row_id, new_number)
    # 存在设计孔剖面信息则结束
    if bool(weather_empty1) is not False:
        return '存在此设计孔剖面信息'
        os._exit(0)
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

    # new_design_jian_ding_x = format(s * see_ceil * math.cos((design_elevation_angel / 180) * math.pi), '.2f')
    # new_design_jian_ding_y = format(design_hole_height + see_ceil *
    # math.sin((design_elevation_angel / 180) * math.pi), '.2f')
    # new_design_zhong_kong_results = jian_zuo_biao(tunnel_name, row_id, new_number, row_x, 'hole_depth',
    # new_design_kai_kong_x, new_design_kai_kong_y)
    # new_design_zhong_kong_x = new_design_zhong_kong_results[0]
    # new_design_zhong_kong_y = new_design_zhong_kong_results[1]
    zhong_kong_length = float(chuan_ding_length) + see_ceil  # 终孔长度
    new_design_zhong_kong_x = format(
        s * (zhong_kong_length + arch_radius) * math.cos((design_elevation_angel / 180) * math.pi), '.2f')
    new_design_zhong_kong_y = format(design_hole_height + (zhong_kong_length + arch_radius) *
                                     math.sin((design_elevation_angel / 180) * math.pi), '.2f')
    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_insert_new_hole_design_pou_mian = "insert into Hole_Design_Pou_Mian(design_jian_mei_x, design_jian_mei_y," \
                                          " design_jian_ding_x, design_jian_ding_y, " \
                                          " design_zhong_kong_x, design_zhong_kong_y," \
                                          " kai_kong_pou_x, kai_kong_pou_y,  hole_number_id" \
                                          ") values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cur.execute(sql_insert_new_hole_design_pou_mian, (new_design_jian_mei_x, new_design_jian_mei_y,
                                                      new_design_jian_ding_x, new_design_jian_ding_y,
                                                      new_design_zhong_kong_x, new_design_zhong_kong_y,
                                                      new_design_kai_kong_x, new_design_kai_kong_y, hole_number_id))
    db.commit()
    db.close()
    return new_number


# 设计偶数孔, hole_number为上一孔号
def design_even_hole(tunnel_name, row_id, hole_number, pan_duan=False):
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
    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_select_chuan_ding = "select work_face.chuan_ding_length, work_face.chong_mei_standard " \
                            "from work_face where id = %s"
    cur.execute(sql_select_chuan_ding, work_face_id)
    chuan_ding_lengths = cur.fetchall()
    chuan_ding_lengths = pd.DataFrame(list(chuan_ding_lengths))

    chuan_ding_length = chuan_ding_lengths.iloc[0, 0]

    chong_mei_standards = chuan_ding_lengths.iloc[0, 1]
    db.close()

    first_number = get_numbers(tunnel_first_hole_number)[1]
    number = get_numbers(hole_number)[1]
    s = 1
    # 如果pan_duan为True则向右创建孔，否则向左
    if pan_duan == True:
        if number % 2 == 0:
            # number 替换为为新孔号
            number = number + 2
        else:
            number = number + 1
    elif number <= first_number:
        if number % 2 == 0:
            number = number - 2
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
    # 存在设计孔信息则结束
    if bool(weather_empty) is not False:
        return number
        os._exit(0)
    xiang_lin_left_number = number - 1
    xiang_lin_right_number = number + 1
    xiang_lin_left_construction_data = get_hole_construction_datas(tunnel_name, row_id, xiang_lin_left_number)
    xiang_lin_right_construction_data = get_hole_construction_datas(tunnel_name, row_id, xiang_lin_right_number)
    # 如果左相邻为空设计孔等于右相邻孔的2倍减去上一孔的值
    if bool(xiang_lin_left_construction_data) is False:
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
    # 如果右相邻为空设计孔等于左相邻孔的2倍减去上一孔的值
    elif bool(xiang_lin_right_construction_data) is False:
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
    # 左右相邻都为空无法设计
    elif bool(xiang_lin_left_construction_data) is False and bool(xiang_lin_right_construction_data) is False:
        print('相邻孔为空无法设计！')
        os._exit(0)
    # 左右相邻孔都存在
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
    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_insert = "insert into hpu_mining.hole_design (hole_number, design_hole_height," \
                 " rock_section, coal_section, see_ceil, hole_depth, row_id," \
                 " design_elevation_angel, single_row) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cur.execute(sql_insert, (number, design_hole_height, rock_section, coal_section, see_ceil, hole_depth,
                             id, design_elevation_angel, single_row))
    db.commit()
    db.close()
    weather_empty1 = get_hole_design_pou_mian_datas(tunnel_name, row_id, number)
    # 设计孔剖面信息存在则结束
    if bool(weather_empty1) is not False:
        return '存在此设计孔剖面信息'
        os._exit(0)
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

    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
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


# ***************************************
def design_jun_pao(tunnel_name, row_id, hole_number):  # 竣工孔坐标
    # row_id = request.Post.get('row_id')
    # hole_number = request.Post.get('hole_number')
    # tunnel_name = request.Post.get('tunnel_id')
    weather_empty = get_jun_pao(tunnel_name, row_id, hole_number)
    if bool(weather_empty) is not False:
        return '存在此竣工孔坐标信息'
        os._exit(0)
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
    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_select_chuan_ding = "select work_face.chuan_ding_length, work_face.chong_mei_standard " \
                            "from work_face where id = %s"
    cur.execute(sql_select_chuan_ding, work_face_id)
    chuan_ding_lengths = cur.fetchall()
    chuan_ding_lengths = pd.DataFrame(list(chuan_ding_lengths))

    chuan_ding_length = chuan_ding_lengths.iloc[0, 0]
    chuan_ding_length = float(chuan_ding_length)
    chong_mei_standard = chuan_ding_lengths.iloc[0, 1]
    chong_mei_standard = float(chong_mei_standard)
    db.close()

    number = get_numbers(hole_number)[1]
    s = 1
    # 判断孔号是大于还是小于首孔号
    if number <= first_number:
        s = -1

    Data = get_hole_construction_datas(tunnel_name, row_id, hole_number)
    con_see_coal = Data['con_see_coal']  # 施工见煤
    con_see_ceil = Data['con_see_ceil']  # 施工见顶
    r_elevation_angle = Data['r_elevation_angle']
    hole_height = Data['hole_height']
    if con_see_coal or con_see_ceil == None:
        weight_of_flush_coal = None
        shi_gong_jian_mei_x = None
        shi_gong_jian_mei_y = None
        shi_gong_jian_ding_x = None
        shi_gong_jian_ding_y = None
        zhong_kong_length = None
        shi_gong_zhong_kong_x = None
        shi_gong_zhong_kong_y = None
    else:
        weight_of_flush_coal = (con_see_ceil - con_see_coal) * chong_mei_standard  # 设计冲煤量
        shi_gong_jian_mei_x = format(s * (con_see_coal + arch_radius) * math.cos((r_elevation_angle / 180) * math.pi),
                                     '.2f')
        shi_gong_jian_mei_y = format(hole_height + (con_see_coal + arch_radius) *
                                     math.sin((r_elevation_angle / 180) * math.pi), '.2f')

        shi_gong_jian_ding_x = format(s * (con_see_ceil + arch_radius) * math.cos((r_elevation_angle / 180) * math.pi),
                                      '.2f')
        shi_gong_jian_ding_y = format(hole_height + (con_see_ceil + arch_radius) *
                                      math.sin((r_elevation_angle / 180) * math.pi), '.2f')

        zhong_kong_length = float(chuan_ding_length) + con_see_ceil  # 终孔长度
        shi_gong_zhong_kong_x = format(
            s * (zhong_kong_length + arch_radius) * math.cos((r_elevation_angle / 180) * math.pi), '.2f')
        shi_gong_zhong_kong_y = format(hole_height + (zhong_kong_length + arch_radius) *
                                       math.sin((r_elevation_angle / 180) * math.pi), '.2f')

    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_insert_weight_of_flush_coal = 'update Hole_Design set weight_of_flush_coal = %s where id = %s '
    cur.execute(sql_insert_weight_of_flush_coal, (weight_of_flush_coal, design_id))
    db.commit()
    db.close()

    Hole_design_pou_mian_Data = get_hole_design_pou_mian_datas(tunnel_name, row_id, hole_number)
    jun_pao_kai_x = Hole_design_pou_mian_Data['kai_kong_pou_x']  # 竣工剖面开孔x
    jun_pao_kai_y = Hole_design_pou_mian_Data['kai_kong_pou_y']  # 竣工剖面开孔y
    # 施工见煤坐标

    # shi_gong_jian_mei_results = jian_zuo_biao(tunnel_name, row_id, hole_number, jun_pao_kai_x, 'con_see_coal',
    #                                           jun_pao_kai_x, jun_pao_kai_y, 1)
    # shi_gong_jian_mei_x = shi_gong_jian_mei_results[0]
    # shi_gong_jian_mei_y = shi_gong_jian_mei_results[1]
    # 施工见顶坐标
    # shi_gong_jian_ding_results = jian_zuo_biao(tunnel_name, row_id, hole_number, jun_pao_kai_x, 'con_see_ceil',
    #                                            jun_pao_kai_x, jun_pao_kai_y, 1)
    # shi_gong_jian_ding_x = shi_gong_jian_ding_results[0]
    # shi_gong_jian_ding_y = shi_gong_jian_ding_results[1]

    # 施工终孔坐标
    # shi_gong_zhong_kong_results = jian_zuo_biao(tunnel_name, row_id, hole_number, jun_pao_kai_x, 'con_hole_depth',
    #                                             jun_pao_kai_x, jun_pao_kai_y, 1)
    # shi_gong_zhong_kong_x = shi_gong_zhong_kong_results[0]
    # shi_gong_zhong_kong_y = shi_gong_zhong_kong_results[1]
    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_insert_jun_pao = 'insert into jun_pao(jun_pao_row_id, jun_pao_hole_num, jun_pao_kai_x, ' \
                         'jun_pao_kai_y, jun_pao_see_coal_x, jun_pao_see_coal_y, ' \
                         'jun_pao_see_ceil_x, jun_pao_see_ceil_y, jun_pao_zhong_kong_x, ' \
                         'jun_pao_zhong_kong_y) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cur.execute(sql_insert_jun_pao, (id, hole_number, jun_pao_kai_x, jun_pao_kai_y,
                                     shi_gong_jian_mei_x, shi_gong_jian_mei_y,
                                     shi_gong_jian_ding_x, shi_gong_jian_ding_y,
                                     shi_gong_zhong_kong_x, shi_gong_zhong_kong_y))
    db.commit()
    db.close()


def hole_design_estimate(tunnel_name, row_id, hole_number):  # 设计孔评价
    row_Data = get_row_datas(tunnel_name, row_id)
    row_x = row_Data['row_x']
    row_y = row_Data['row_y']
    data1 = get_xie_ya()  # 获取泄压范围
    # 匹配泄压范围(x1, y1), (x2, y2)为上下相邻匹配坐标
    x_1_xie = data1[data1.iloc[:, 0] < row_x].tail(1).iloc[0, 0]
    x_2_xie = data1[data1.iloc[:, 0] > row_x].head(1).iloc[0, 0]
    y_1_xie = data1[data1.iloc[:, 0] < row_x].tail(1).iloc[0, 1]
    y_2_xie = data1[data1.iloc[:, 0] > row_x].head(1).iloc[0, 1]
    y_xie = y_1_xie + (y_2_xie - y_1_xie) * (row_x - x_1_xie) / (x_2_xie - x_1_xie)
    y_xie_cha = abs(y_xie - row_y)
    # 是否右侧创建孔
    you_kai = False

    hole_design_data = get_hole_design_datas(tunnel_name, row_id, hole_number)
    design_elevation_angel = hole_design_data['design_elevation_angel']

    hole_number_id = hole_design_data['id']
    hole_design_pou_mian_data = get_hole_design_pou_mian_datas(tunnel_name, row_id, hole_number)
    design_jian_mei_x = hole_design_pou_mian_data['design_jian_mei_x']
    design_jian_ding_x = hole_design_pou_mian_data['design_jian_ding_x']
    kai_kong_pou_x = hole_design_pou_mian_data['kai_kong_pou_x']

    kong_sub_mei = abs(kai_kong_pou_x - design_jian_mei_x)  # 孔见煤
    kong_sub_ding = abs(kai_kong_pou_x - design_jian_ding_x)  # 孔见顶
    # 删除左侧孔向右侧设计!!!!!
    if kong_sub_mei >= y_xie_cha:
        db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
        cur = db.cursor()

        sql_delete_hole_design_pou_mian = "delete  from hole_design_pou_mian where hole_number_id = %s"
        cur.execute(sql_delete_hole_design_pou_mian, hole_number_id)

        db.commit()
        db.close()

        db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
        cur = db.cursor()

        sql_delete_hole_design_pou_mian = "delete  from hole_design where id = %s"
        cur.execute(sql_delete_hole_design_pou_mian, hole_number_id)
        db.commit()
        db.close()
        you_kai = True
    # （设计 见顶-开孔）≥xie控制范围，修改设计孔孔深
    elif kong_sub_ding >= y_xie_cha:
        equal_value = y_xie_cha / math.cos((design_elevation_angel) / 180 * math.pi)
        db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
        cur = db.cursor()
        sql_update = "update Hole_Design set see_ceil = %s, hole_depth = %s  " \
                     "where hole_number = '%s' and id = %s "
        cur.execute(sql_update % (equal_value, equal_value, hole_number, hole_number_id))
        db.commit()
        db.close()
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

    # 匹配处理后下部分(x1, y1), (x2, y2)为上下相邻匹配坐标
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
    if jun_pao_see_ceil_x or jun_pao_see_coal_x == None:
        print('为空值不能评价')
        os._exit(0)
    else:
        coal_sub_kai = abs(jun_pao_see_coal_x - jun_pao_kai_x)  # 见煤 - 开孔
        ceil_sub_kai = abs(jun_pao_see_ceil_x - jun_pao_kai_x)  # 见顶 - 开孔

        right_number = None
        # 孔号小于首孔号不能评价
        if number < first_number:
            print("孔号小于首孔号不能评价")
        else:
            # 满足此条件设计奇数孔
            if coal_sub_kai < y_xia_cha:
                right_number = design_odd_hole(tunnel_name, row_id, hole_number)
            # 否则设计偶数孔
            else:
                print("不再设计新孔, 设计偶数孔")
                right_number = design_even_hole(tunnel_name, row_id, first_number)
        return right_number


def ping_jia_shi_gong_kong(tunnel_name, row_id, hole_number):  # 评价施工孔控制范围
    row_Data = get_row_datas(tunnel_name, row_id)
    row_x = row_Data['row_x']
    row_y = row_Data['row_y']
    tunnel_Data = get_tunnel_datas(tunnel_name)

    tunnel_first_hole_number = tunnel_Data['tunnel_first_hole_number']
    first_number = get_numbers(tunnel_first_hole_number)[1]

    hole_Data = get_jun_pao(tunnel_name, row_id, hole_number)
    jun_pao_see_coal_x = hole_Data['jun_pao_see_coal_x']  # 竣工见煤剖面坐标x
    jun_pao_kai_x = hole_Data['jun_pao_kai_x']  # 竣工开孔剖面坐标y
    jun_pao_see_ceil_x = hole_Data['jun_pao_see_ceil_x']  # 竣工见顶剖面坐标x
    if jun_pao_see_ceil_x or jun_pao_see_coal_x == None:
        print('为空值不能评价')
        os._exit(0)
    else:
        coal_sub_kai_x = abs(jun_pao_see_coal_x - jun_pao_kai_x)  # 见煤 - 开孔
        ceil_sub_kai_x = abs(jun_pao_see_ceil_x - jun_pao_kai_x)  # 见顶 - 开孔

        data1 = get_chuli_shang()
        # 处理上范围匹配(x1, y1), (x2, y2)为上下相邻匹配坐标
        x_1_shang = data1[data1.iloc[:, 0] < row_x].tail(1).iloc[0, 0]
        x_2_shang = data1[data1.iloc[:, 0] > row_x].head(1).iloc[0, 0]
        y_1_shang = data1[data1.iloc[:, 0] < row_x].tail(1).iloc[0, 1]
        y_2_shang = data1[data1.iloc[:, 0] > row_x].head(1).iloc[0, 1]
        y_shang = y_1_shang + (y_2_shang - y_1_shang) * (row_x - x_1_shang) / (x_2_shang - x_1_shang)
        y_shang_cha = abs(y_shang - row_y)

        data3 = get_xie_ya()
        # 泄压范围匹配(x1, y1), (x2, y2)为上下相邻匹配坐标
        x_1_xie = data3[data3.iloc[:, 0] < row_x].tail(1).iloc[0, 0]
        x_2_xie = data3[data3.iloc[:, 0] > row_x].head(1).iloc[0, 0]
        y_1_xie = data3[data3.iloc[:, 0] < row_x].tail(1).iloc[0, 1]
        y_2_xie = data3[data3.iloc[:, 0] > row_x].head(1).iloc[0, 1]
        y_xie = y_1_xie + (y_2_xie - y_1_xie) * (row_x - x_1_xie) / (x_2_xie - x_1_xie)
        y_xie_cha = abs(y_xie - row_y)

        left_number = None
        right_number = tunnel_first_hole_number

        number = get_numbers(hole_number)[1]  # 获取当前孔号
        # 孔号小于首孔号
        if number <= first_number:
            # 满足此条件向右侧创建
            if coal_sub_kai_x >= y_shang_cha and ceil_sub_kai_x >= y_xie_cha:
                # 判断设计奇数孔还是偶数孔
                if number % 2 == 0:
                    right_number = design_even_hole(tunnel_name, row_id, first_number, pan_duan=True)
                    left_number = hole_number
                else:
                    right_number = design_odd_hole(tunnel_name, row_id, first_number, pan_duan=True)
                    left_number = hole_number
                # 设计孔评价
                ping_jia_design = hole_design_estimate(tunnel_name, row_id, right_number)
                # 首次向右侧创建失败    you_kai = True
                if ping_jia_design == True:
                    left_number = hole_number
                    right_number = tunnel_first_hole_number
            # 继续左侧创建
            else:
                left_number = design_odd_hole(tunnel_name, row_id, hole_number)
                ping_jia_design = hole_design_estimate(tunnel_name, row_id, left_number)  # 设计孔评价
                # 是否创建失败
                if ping_jia_design == True:
                    left_number = hole_number
                    right_number = first_number
                    print("此时需要向右侧创建孔")
        # 孔号大于首孔号
        else:
            # 找出最左侧孔号
            db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
            cur = db.cursor()
            sql_select_all_numbers = 'select  h_c_number from  Hole_Construction where row_id = %s'
            cur.execute(sql_select_all_numbers, 1)
            all_numbers = cur.fetchall()
            all_number = pd.DataFrame(list(all_numbers))
            db.close()
            number_list = []
            # 所有孔号数字提取
            for i in range(len(all_number)):
                s = int(all_number.loc[i, 0])
                s = get_numbers(s)[1]
                number_list.append(s)
            # 排序
            number_list.sort()
            # 最左侧孔号
            left_number = number_list[0]
            # 对施工孔进行评价 与设计孔评价不同 包含有对新设计孔创建
            ping_jia_shi_gong = shi_gong_xia_estimate(tunnel_name, row_id, hole_number)
            right_number = number

        return left_number, right_number


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
    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_select_all_numbers = 'select  h_c_number from  Hole_Construction where row_id = %s'
    cur.execute(sql_select_all_numbers, id)
    all_numbers = cur.fetchall()
    all_number = pd.DataFrame(list(all_numbers))
    db.close()
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
        os._exit(0)
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
        db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
        cur = db.cursor()
        sql_insert = "insert into hpu_mining.hole_design (hole_number, design_hole_height," \
                     " deflection_angle, rock_section, coal_section, see_ceil, hole_depth, row_id," \
                     " design_elevation_angel, single_row) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(sql_insert, (new_number, design_hole_height, deflection_angle,
                                 rock_section, coal_section, see_ceil, hole_depth,
                                 id, design_elevation_angel, single_row))

        db.commit()
        db.close()

    elif '施工倾角误差大' in hole_eval_data['see_coal_eval'] and '施工倾角误差大' in hole_eval_data['see_ceil_eval']:
        design_hole_height = design_data['design_hole_height']
        deflection_angle = design_data['deflection_angle']
        design_elevation_angel = design_data['design_elevation_angel']
        rock_section = design_data['rock_section']
        coal_section = design_data['coal_section']
        see_ceil = design_data['see_ceil']
        hole_depth = design_data['hole_depth']
        db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
        cur = db.cursor()
        sql_insert = "insert into hpu_mining.hole_design (hole_number, design_hole_height," \
                     " deflection_angle, rock_section, coal_section, see_ceil, hole_depth, row_id," \
                     " design_elevation_angel, single_row) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(sql_insert, (new_number, design_hole_height, deflection_angle,
                                 rock_section, coal_section, see_ceil, hole_depth,
                                 id, design_elevation_angel, single_row))

        db.commit()
        db.close()
        define_hole_design_pou_mian(row_id, new_number)  # 新孔剖面坐标插入

    elif hole_eval_data['see_coal_eval'] == '钻孔偏斜' and hole_eval_data['see_ceil_eval'] == '钻孔偏斜':
        design_hole_height = design_data['design_hole_height']
        deflection_angle = design_data['deflection_angle']
        rock_section = design_data['rock_section']
        a = hole_design_pou_mian_data['design_jian_ding_x']
        b = number_jun_pao['jun_pao_see_ceil_y'] + (number_jun_pao['jun_pao_see_ceil_x'] - a) \
            * math.sin(mei_ceng_qing_jiao)
        design_elevation_angel = math.atan((b - hole_design_pou_mian_data['kai_kong_pou_y']) /
                                           a - hole_design_pou_mian_data['kai_kong_pou_x'])
        see_ceil = design_data['see_ceil'] * math.cos(design_data['design_elevation_angel']) / \
                   math.cos(number_hole_construction_Data['r_elevation_angle'])
        coal_section = design_data['coal_section'] * math.cos(design_data['design_elevation_angel']) / \
                       math.cos(number_hole_construction_Data['r_elevation_angle'])
        hole_depth = see_ceil + 1
        db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
        cur = db.cursor()
        sql_insert = "insert into hpu_mining.hole_design (hole_number, design_hole_height," \
                     " deflection_angle, rock_section, coal_section, see_ceil, hole_depth, row_id," \
                     " design_elevation_angel, single_row) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(sql_insert, (new_number, design_hole_height, deflection_angle,
                                 rock_section, coal_section, see_ceil, hole_depth,
                                 id, design_elevation_angel, single_row))

        db.commit()
        db.close()
    weather_empty1 = get_hole_design_pou_mian_datas(tunnel_name, row_id, new_number)
    # 判断设计孔剖面信息是否为空，为空结束
    if bool(weather_empty1) is not False:
        print('存在此设计孔剖面信息')
        return new_number
        os._exit(0)
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
    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_insert_new_hole_design_pou_mian = "insert into Hole_Design_Pou_Mian(design_jian_mei_x, design_jian_mei_y," \
                                          " design_jian_ding_x, design_jian_ding_y, " \
                                          " design_zhong_kong_x, design_zhong_kong_y," \
                                          " design_kai_kong_pou_x, design_kai_kong_pou_y,  hole_number_id" \
                                          ") values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cur.execute(sql_insert_new_hole_design_pou_mian, (new_design_jian_mei_x, new_design_jian_mei_y,
                                                      new_design_jian_ding_x, new_design_jian_ding_y,
                                                      new_design_zhong_kong_x, new_design_zhong_kong_y,
                                                      new_design_kai_kong_x, new_design_kai_kong_y, hole_number_id))
    db.commit()
    db.close()
    return new_number


def zuan_kong_quality_estimate(tunnel_name, row_id, hole_number):  # 钻孔施工质量评价 见止煤误差(单孔评价)
    # 数字提取
    number = get_numbers(hole_number)[1]  # 当前钻孔数字
    tunnel_Data = get_tunnel_datas(tunnel_name)
    mei_ceng_qing_jiao = tunnel_Data['mei_ceng_qing_jiao']
    tunnel_first_hole_number = tunnel_Data['tunnel_first_hole_number']  # 这一排的首孔号
    first_number = get_numbers(tunnel_first_hole_number)[1]
    first_hole_design_Data = get_hole_design_datas(tunnel_name, row_id, first_number)
    first_coal_section = first_hole_design_Data['coal_section']  # 首孔设计煤段

    first_hole_Construction_Data = get_hole_construction_datas(tunnel_name, row_id, first_number)
    first_hole_Construction_con_see_coal = first_hole_Construction_Data['con_see_coal']  # 首孔施工见煤
    first_hole_Construction_con_see_ceil = first_hole_Construction_Data['con_see_ceil']  # 首孔施工见顶

    Row_Data = get_row_datas(tunnel_name, row_id)
    id = Row_Data['id']

    hole_design_Data = get_hole_design_datas(tunnel_name, row_id, hole_number)
    hole_construction_Data = get_hole_construction_datas(tunnel_name, row_id, hole_number)
    if hole_construction_Data['con_see_ceil'] or hole_construction_Data['con_see_coal'] == None:
        os._exit(0)
    else:
        mei_duan_length = hole_construction_Data['con_see_ceil'] - hole_construction_Data['con_see_coal']  # 煤段长度
    # 判断当前孔在首孔哪一侧
    if number > first_number:
        s = 1
    else:
        s = -1
    judgment = abs(math.asin((first_hole_Construction_con_see_coal - first_hole_Construction_con_see_ceil +
                              first_coal_section) / 2) * 180 / math.pi * s - mei_ceng_qing_jiao)

    judgment1 = first_hole_Construction_con_see_ceil * math.cos((judgment) / 180 * math.pi) + \
                first_hole_Construction_con_see_ceil * math.sin((judgment) / 180 * math.pi) * \
                math.sin((90 - judgment + s * mei_ceng_qing_jiao) / 180 * math.pi)
    hole_eval_data = get_hole_eval_datas(tunnel_name, row_id, hole_number)

    # 如果孔评价存在则结束
    if bool(hole_eval_data) is True:
        print('存在此孔质量评价')
        os._exit(0)
    # 不同条件插入不同孔评价参数
    if hole_construction_Data['con_see_coal'] == None:
        os._exit(0)
    else:
        if abs(hole_construction_Data['con_see_coal'] - hole_design_Data['rock_section']) <= 5 and \
                abs(hole_construction_Data['con_see_ceil'] - hole_design_Data['see_ceil']) <= 5:
            db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
            cur = db.cursor()
            sql_insert_estimate = 'insert into Hole_Eval(see_coal_eval, see_ceil_eval, ' \
                                  'h_name, row_id) values(%s ,%s, %s, %s)'
            cur.execute(sql_insert_estimate, ('见煤合格', '见顶合格', hole_number, id))
            db.commit()
            db.close()
            new_number = hole_number
        elif abs(hole_construction_Data['con_see_coal'] - hole_design_Data['rock_section']) > 5 and \
                abs(hole_construction_Data['con_see_ceil'] - hole_design_Data['see_ceil']) > 5:
            if abs(judgment - hole_construction_Data['r_elevation_angle']) > 1:
                if abs(judgment1 - hole_construction_Data['con_see_ceil']) >= 3:
                    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining',
                                         port=3306)
                    cur = db.cursor()
                    sql_insert_estimate = 'insert into Hole_Eval(see_coal_eval, see_ceil_eval, ' \
                                          'h_name, row_id) values(%s ,%s, %s, %s)'
                    cur.execute(sql_insert_estimate, ('钻孔偏斜', '钻孔偏斜', hole_number, id))
                    db.commit()
                    db.close()
                    new_number = design_repair_hole(tunnel_name, row_id, hole_number)[0]
                else:
                    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining',
                                         port=3306)
                    cur = db.cursor()
                    sql_insert_estimate = 'insert into Hole_Eval(see_coal_eval, see_ceil_eval, ' \
                                          'h_name, row_id) values(%s ,%s, %s, %s)'
                    cur.execute(sql_insert_estimate, ('施工倾角误差大，为：' + str(judgment) + '°',
                                                      '施工倾角误差大, 为: ' + str(judgment), hole_number, id))
                    db.commit()
                    db.close()
                    new_number = design_repair_hole(tunnel_name, row_id, hole_number)[0]
            else:
                db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
                cur = db.cursor()
                sql_insert_estimate = 'insert into Hole_Eval(see_coal_eval, see_ceil_eval, ' \
                                      'h_name, row_id) values(%s ,%s, %s, %s)'
                cur.execute(sql_insert_estimate, ('有断层', '有断层', hole_number, id))
                db.commit()
                db.close()
                new_number = design_repair_hole(tunnel_name, row_id, hole_number)[0]
        else:
            db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
            cur = db.cursor()
            sql_insert_estimate = 'insert into Hole_Eval(see_coal_eval, see_ceil_eval, ' \
                                  'h_name, row_id) values(%s ,%s, %s, %s)'
            cur.execute(sql_insert_estimate, ('有断层', '有断层', hole_number, id))
            db.commit()
            db.close()
            new_number = design_repair_hole(tunnel_name, row_id, hole_number)[0]
        return new_number


# print(zuan_kong_quality_estimate('16071工作面上部底板巷', 15, 9))
# print(design_jun_pao('16071工作面上部底板巷', 15, 2))
# print(ping_jia_shi_gong_kong('16071工作面上部底板巷', 15, 2))
# print(hole_design_estimate())
# get_hole_design_datas('16071工作面上部底板巷', 15, 3)
# ______________________________________________________________________________
# ______________________________________________________________________________
# ______________________________________________________________________________
# ______________________________________________________________________________


def Insert_Hole_Design_Ping_Mian(tunnel_name, row_id, hole_number):
    tunnel_data = get_tunnel_datas(tunnel_name)
    tunnel_fang_wei_angle = tunnel_data['tunnel_fang_wei_angle']
    row_data = get_row_datas(tunnel_name, row_id)
    row_x = row_data['row_x']
    arch_radius = tunnel_data['arch_radius']
    hole_design_data = get_hole_design_datas(tunnel_name, row_id, hole_number)
    hole_number_id = hole_design_data['id']
    design_elevation_angel = hole_design_data['design_elevation_angel']
    hole_depth = hole_design_data['hole_depth']
    number = get_numbers(hole_number)[1]
    s = 1
    if number >= 11:
        s = -1
    hang_shen = tunnel_data['tunnel_length'] / tunnel_data['tunnel_row_numebers']
    pai_jian_ju = (tunnel_data['tunnel_length'] + 3) / tunnel_data['tunnel_row_numebers']
    kai_kong_ping_x = 104.06 + hang_shen * (656.04 - 104.06)  # 等同于每列钻孔开孔坐标算法
    kai_kong_ping_y = arch_radius * math.cos(math.radians(design_elevation_angel)) * s - 21.93 + pai_jian_ju * (
            -32.7 + 21.93)
    kai_kong_ping_z = row_x

    zuobiao = matching_function(tunnel_name, row_id, number, row_x)
    # 用匹配函数匹配不在范围内结束程序
    if zuobiao is False:
        print('匹配错误！')
        os._exit(0)
    rock_section = zuobiao[4]  # 设计岩段
    coal_section = zuobiao[5]  # 设计煤段
    design_jian_mei_x = kai_kong_ping_x + rock_section * math.cos(math.radians(design_elevation_angel)) * math.sin(
        math.radians(90 + tunnel_fang_wei_angle))
    design_jian_mei_y = kai_kong_ping_y + rock_section * math.cos(math.radians(design_elevation_angel)) * math.cos(
        math.radians(90 + tunnel_fang_wei_angle))
    design_jian_mei_z = kai_kong_ping_z + rock_section * math.sin(math.radians(design_elevation_angel))

    design_jian_ding_x = kai_kong_ping_x + (rock_section + coal_section) * math.cos(
        math.radians(design_elevation_angel)) * math.sin(math.radians(90 + tunnel_fang_wei_angle))
    design_jian_ding_y = kai_kong_ping_y + (rock_section + coal_section) * math.cos(
        math.radians(design_elevation_angel)) * math.cos(math.radians(90 + tunnel_fang_wei_angle))
    design_jian_ding_z = kai_kong_ping_z + (rock_section + coal_section) * math.sin(
        math.radians(design_elevation_angel))

    design_zhong_kong_x = kai_kong_ping_x + hole_depth * math.cos(math.radians(design_elevation_angel)) * math.sin(
        math.radians(90 + tunnel_fang_wei_angle))
    design_zhong_kong_y = kai_kong_ping_y + hole_depth * math.cos(math.radians(design_elevation_angel)) * math.cos(
        math.radians(90 + tunnel_fang_wei_angle))
    design_zhong_kong_z = kai_kong_ping_z + hole_depth * math.sin(math.radians(design_elevation_angel))

    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_insert_new_hole_design_ping_mian = "insert into  Hole_Design_Ping_Mian(design_jian_mei_x, design_jian_mei_y, " \
                                           "design_jian_mei_z, " \
                                           " design_jian_ding_x, design_jian_ding_y, design_jian_ding_z, " \
                                           " design_zhong_kong_x, design_zhong_kong_y, design_zhong_kong_z, " \
                                           " kai_kong_ping_x, kai_kong_ping_y, kai_kong_ping_z, hole_number_id" \
                                           ") values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cur.execute(sql_insert_new_hole_design_ping_mian, (design_jian_mei_x, design_jian_mei_y, design_jian_mei_z,
                                                       design_jian_ding_x, design_jian_ding_y, design_jian_ding_z,
                                                       design_zhong_kong_x, design_zhong_kong_y, design_zhong_kong_z,
                                                       kai_kong_ping_x, kai_kong_ping_y, kai_kong_ping_z,
                                                       hole_number_id))
    db.commit()
    db.close()


# Insert_Hole_Design_Ping_Mian('16071工作面中部底板巷', 15, 10)


def Insert_Hole_Design_Pou_Mian(tunnel_name, row_id, hole_number):
    row_data = get_row_datas(tunnel_name, row_id)
    row_x = row_data['row_x']
    hole_design_data = get_hole_design_datas(tunnel_name, row_id, hole_number)
    hole_number_id = hole_design_data['id']
    design_elevation_angel = hole_design_data['design_elevation_angel']
    design_hole_height = hole_design_data['design_hole_height']
    hole_depth = hole_design_data['hole_depth']
    number = get_numbers(hole_number)[1]
    zuobiao = matching_function(tunnel_name, row_id, number, row_x)
    # 用匹配函数匹配不在范围内结束程序
    if zuobiao is False:
        print('匹配错误！')
        os._exit(0)
    rock_section = zuobiao[4]  # 设计岩段
    coal_section = zuobiao[5]  # 设计煤段

    design_jian_mei_x = math.cos(math.radians(design_elevation_angel)) * rock_section
    design_jian_mei_y = math.sin(math.radians(design_elevation_angel)) * rock_section
    design_jian_mei_z = None

    design_jian_ding_x = math.cos(math.radians(design_elevation_angel)) * (rock_section + coal_section)
    design_jian_ding_y = math.sin(math.radians(design_elevation_angel)) * (rock_section + coal_section)
    design_jian_ding_z = None

    design_zhong_kong_x = math.cos(math.radians(design_elevation_angel)) * hole_depth
    design_zhong_kong_y = math.sin(math.radians(design_elevation_angel)) * hole_depth
    design_zhong_kong_z = None

    design_kai_kong_pou_x = 0
    design_kai_kong_pou_y = design_hole_height
    design_kai_kong_pou_z = None

    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_insert_new_hole_design_pou_mian = "insert into Hole_Design_Pou_Mian(design_jian_mei_x, design_jian_mei_y," \
                                          "  design_jian_mei_z, design_jian_ding_x, design_jian_ding_y, " \
                                          " design_jian_ding_z, design_zhong_kong_x, design_zhong_kong_y," \
                                          " design_zhong_kong_z, design_kai_kong_pou_x, design_kai_kong_pou_y,  " \
                                          "design_kai_kong_pou_z, hole_number_id" \
                                          ") values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cur.execute(sql_insert_new_hole_design_pou_mian, (design_jian_mei_x, design_jian_mei_y, design_jian_mei_z,
                                                      design_jian_ding_x, design_jian_ding_y, design_jian_ding_z,
                                                      design_zhong_kong_x, design_zhong_kong_y, design_zhong_kong_z,
                                                      design_kai_kong_pou_x, design_kai_kong_pou_y,
                                                      design_kai_kong_pou_z, hole_number_id))
    db.commit()
    db.close()


# Insert_Hole_Design_Pou_Mian('16071工作面中部底板巷', 15, 10)

def Pai_hao_ti_qu(numbers):
    n = list(str(numbers))
    ge_wei = int(n[-1])
    if ge_wei > 0:
        pai_hao = numbers // 10 + 1
    else:
        pai_hao = numbers // 10
    return pai_hao


# print(Pai_hao_ti_qu(13))

def Insert_Hole_Design_Pou_Mian_Cad(tunnel_name, row_id, hole_number):
    tunnel_Data = get_tunnel_datas(tunnel_name)
    she_pao_kai_x = tunnel_Data['she_pao_kai_x']
    she_pao_kai_y = tunnel_Data['she_pao_kai_y']
    heng_xiang_jian_ju = tunnel_Data['heng_xiang_jian_ju']
    shu_xiang_jian_ju = tunnel_Data['shu_xiang_jian_ju']
    mei_pai_zu_shu = tunnel_Data['mei_pai_zu_shu']
    row_data = get_row_datas(tunnel_name, row_id)
    row_x = row_data['row_x']
    current_row_number = int(row_data['row_id'])  # 该组钻孔排号数字
    pai_hao_ti_qu = Pai_hao_ti_qu(current_row_number)  # rundowm提取
    hole_design_data = get_hole_design_datas(tunnel_name, row_id, hole_number)
    hole_number_id = hole_design_data['id']

    number = get_numbers(hole_number)[1]
    zuobiao = matching_function(tunnel_name, row_id, number, row_x)
    # 用匹配函数匹配不在范围内结束程序
    if zuobiao is False:
        print('匹配错误！')
        os._exit(0)
    rock_section = zuobiao[4]  # 设计岩段
    coal_section = zuobiao[5]  # 设计煤段

    hole_design_pou_mian_datas = get_hole_design_pou_mian_datas(tunnel_name, row_id, hole_number)
    design_jian_mei_x = hole_design_pou_mian_datas['design_jian_mei_x']
    design_jian_mei_y = hole_design_pou_mian_datas['design_jian_mei_y']
    design_jian_mei_cad_x = design_jian_mei_x + she_pao_kai_x - heng_xiang_jian_ju * (
        int(current_row_number / mei_pai_zu_shu))
    design_jian_mei_cad_y = design_jian_mei_y + she_pao_kai_y + shu_xiang_jian_ju * (current_row_number - pai_hao_ti_qu)
    design_jian_mei_cad_z = None

    design_jian_ding_x = hole_design_pou_mian_datas['design_jian_ding_x']
    design_jian_ding_y = hole_design_pou_mian_datas['design_jian_ding_y']
    design_jian_ding_cad_x = design_jian_ding_x + she_pao_kai_x - heng_xiang_jian_ju * (
        int(current_row_number / mei_pai_zu_shu))
    design_jian_ding_cad_y = design_jian_ding_y + shu_xiang_jian_ju * (current_row_number - pai_hao_ti_qu)
    design_jian_ding_cad_z = None

    design_zhong_kong_x = hole_design_pou_mian_datas['design_zhong_kong_x']
    design_zhong_kong_y = hole_design_pou_mian_datas['design_zhong_kong_y']
    design_zhong_kong_cad_x = design_zhong_kong_x + she_pao_kai_x - heng_xiang_jian_ju * (
        int(current_row_number / mei_pai_zu_shu))
    design_zhong_kong_cad_y = design_zhong_kong_y + shu_xiang_jian_ju * (current_row_number - pai_hao_ti_qu)
    design_zhong_kong_cad_z = None

    design_kai_kong_pou_x = hole_design_pou_mian_datas['design_kai_kong_pou_x']
    design_kai_kong_pou_y = hole_design_pou_mian_datas['design_kai_kong_pou_y']
    design_kai_kong_pou_cad_x = design_kai_kong_pou_x + she_pao_kai_x - heng_xiang_jian_ju * (
        int(current_row_number / mei_pai_zu_shu))
    design_kai_kong_pou_cad_y = design_kai_kong_pou_y + shu_xiang_jian_ju * (current_row_number - pai_hao_ti_qu)
    design_kai_kong_pou_cad_z = None

    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_insert_new_hole_design_pou_mian = "insert into Hole_Design_Pou_Mian_Cad(design_jian_mei_cad_x, " \
                                          "design_jian_mei_cad_y, " \
                                          "design_jian_mei_cad_z," \
                                          " design_jian_ding_cad_x, design_jian_ding_cad_y, design_jian_ding_cad_z, " \
                                          " design_zhong_kong_cad_x, design_zhong_kong_cad_y, design_zhong_kong_cad_z, " \
                                          "design_kai_kong_pou_cad_x, design_kai_kong_pou_cad_y, " \
                                          "design_kai_kong_pou_cad_z, " \
                                          "hole_number_id" \
                                          ") values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cur.execute(sql_insert_new_hole_design_pou_mian,
                (design_jian_mei_cad_x, design_jian_mei_cad_y, design_jian_mei_cad_z,
                 design_jian_ding_cad_x, design_jian_ding_cad_y, design_jian_ding_cad_z,
                 design_zhong_kong_cad_x, design_zhong_kong_cad_y, design_zhong_kong_cad_z,
                 design_kai_kong_pou_cad_x, design_kai_kong_pou_cad_y,
                 design_kai_kong_pou_cad_z, hole_number_id))
    db.commit()
    db.close()


# Insert_Hole_Design_Pou_Mian_Cad('16071工作面中部底板巷', 15, 10)

def Insert_Completion_plan_coordinate(tunnel_name, row_id, hole_number):
    tunnel_Data = get_tunnel_datas(tunnel_name)
    tunnel_fang_wei_angle = tunnel_Data['tunnel_fang_wei_angle']
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']
    hole_construction_data = get_hole_construction_datas(tunnel_name, row_id, hole_number)
    con_see_ceil = hole_construction_data['con_see_ceil']
    con_see_coal = hole_construction_data['con_see_coal']
    r_elevation_angle = hole_construction_data['r_elevation_angle']
    ab_hole_depth_position = hole_construction_data['ab_hole_depth_position']
    con_hole_depth = hole_construction_data['con_hole_depth']
    row_x = row_data['row_x']
    arch_radius = tunnel_Data['arch_radius']
    number = get_numbers(hole_number)[1]
    s = 1
    if number >= 11:
        s = -1
    hang_shen = tunnel_Data['tunnel_length'] / tunnel_Data['tunnel_row_numebers']
    pai_jian_ju = (tunnel_Data['tunnel_length'] + 3) / tunnel_Data['tunnel_row_numebers']

    kai_kong_ping_x = 104.06 + hang_shen * (656.04 - 104.06)  # 等同于每列钻孔开孔坐标算法
    kai_kong_ping_y = arch_radius * math.cos(math.radians(r_elevation_angle)) * s - 21.93 + pai_jian_ju * (
            -32.7 + 21.93)
    kai_kong_ping_z = row_x

    see_coal_x = kai_kong_ping_x + con_see_coal * math.cos(math.radians(r_elevation_angle)) * math.sin(
        math.radians(90 + tunnel_fang_wei_angle))
    see_coal_y = kai_kong_ping_x + con_see_coal * math.cos(math.radians(r_elevation_angle)) * math.cos(
        math.radians(90 + tunnel_fang_wei_angle))
    see_coal_z = kai_kong_ping_x + con_see_coal * math.sin(math.radians(r_elevation_angle))

    see_cile_ding_x = kai_kong_ping_x + con_see_ceil * math.cos(math.radians(r_elevation_angle)) * math.sin(
        math.radians(90 + tunnel_fang_wei_angle))
    see_cile_ding_y = kai_kong_ping_y + con_see_ceil * math.cos(math.radians(r_elevation_angle)) * math.cos(
        math.radians(90 + tunnel_fang_wei_angle))
    see_cile_ding_z = kai_kong_ping_z + con_see_ceil * math.sin(math.radians(r_elevation_angle))

    pen_hole_x = kai_kong_ping_x + ab_hole_depth_position * math.cos(math.radians(r_elevation_angle)) * math.sin(
        math.radians(90 + tunnel_fang_wei_angle))
    pen_hole_y = kai_kong_ping_x + ab_hole_depth_position * math.cos(math.radians(r_elevation_angle)) * math.cos(
        math.radians(90 + tunnel_fang_wei_angle))
    pen_hole_z = kai_kong_ping_x + ab_hole_depth_position * math.sin(math.radians(r_elevation_angle))

    hole_depth_x = kai_kong_ping_x + con_hole_depth * math.cos(math.radians(r_elevation_angle)) * math.sin(
        math.radians(90 + tunnel_fang_wei_angle))
    hole_depth_y = kai_kong_ping_x + con_hole_depth * math.cos(math.radians(r_elevation_angle)) * math.cos(
        math.radians(90 + tunnel_fang_wei_angle))
    hole_depth_z = kai_kong_ping_x + con_hole_depth * math.sin(math.radians(r_elevation_angle))

    ya_zuan_x = kai_kong_ping_x + ab_hole_depth_position * math.cos(math.radians(r_elevation_angle)) * math.sin(
        math.radians(90 + tunnel_fang_wei_angle))
    ya_zuan_y = kai_kong_ping_x + ab_hole_depth_position * math.cos(math.radians(r_elevation_angle)) * math.cos(
        math.radians(90 + tunnel_fang_wei_angle))
    ya_zuan_z = kai_kong_ping_x + ab_hole_depth_position * math.sin(math.radians(r_elevation_angle))

    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_insert_completion_plan_coordinate = "insert into Completion_plan_coordinate(kai_kong_x, kai_kong_y, " \
                                            "kai_kong_z, see_coal_x, see_coal_y, see_coal_z, see_cile_x, see_cile_y, " \
                                            "see_cile_z, pen_hole_x, pen_hole_y, pen_hole_z, ya_zuan_x, ya_zuan_y, " \
                                            "ya_zuan_z, hole_depth_x, hole_depth_y, hole_depth_z, completion_row_id, " \
                                            "completion_hole_num" \
                                            ") values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                                            "%s, %s, %s, %s) "
    cur.execute(sql_insert_completion_plan_coordinate,
                (kai_kong_ping_x, kai_kong_ping_y, kai_kong_ping_z,
                 see_coal_x, see_coal_y, see_coal_z,
                 see_cile_ding_x, see_cile_ding_y, see_cile_ding_z,
                 pen_hole_x, pen_hole_y, pen_hole_z,
                 ya_zuan_x, ya_zuan_y, ya_zuan_z,
                 hole_depth_x, hole_depth_y, hole_depth_z,
                 id, hole_number))
    db.commit()
    db.close()


# Insert_Completion_plan_coordinate('16071工作面中部底板巷', 15, 10)


def get_Completion_plan_coordinate_datas(tunnel_name, row_id, hole_number):
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']
    Datas = Completion_plan_coordinate.objects.filter(completion_row=id, completion_hole_num=hole_number).first()
    if Datas is not None:
        Data = model_to_dict(Datas)
    else:
        Data = {}
    return Data


# print(get_Completion_plan_coordinate_datas('16071工作面中部底板巷', 15, 10))

def Insert_Wen_zi(tunnel_name, row_id, hole_number):
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']
    completion_plan_coordinate_data = get_Completion_plan_coordinate_datas(tunnel_name, row_id, hole_number)
    hole_depth_x = completion_plan_coordinate_data['hole_depth_x']
    hole_depth_y = completion_plan_coordinate_data['hole_depth_y']
    hole_depth_z = completion_plan_coordinate_data['hole_depth_z']
    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_insert_wen_zi = "insert into Wen_zi(wen_zi_row_id, wen_zi_hole_num,  wen_zi_x,  wen_zi_y,  wen_zi_z)" \
                        " values(%s, %s, %s, %s, %s) "
    cur.execute(sql_insert_wen_zi,
                (id, hole_number, hole_depth_x, hole_depth_y, hole_depth_z))
    db.commit()
    db.close()


# Insert_Wen_zi('16071工作面中部底板巷', 15, 10)


def Insert_jun_zhong_hole(tunnel_name, row_id, hole_number):
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']
    completion_plan_coordinate_data = get_Completion_plan_coordinate_datas(tunnel_name, row_id, hole_number)
    hole_depth_x = completion_plan_coordinate_data['hole_depth_x']
    hole_depth_y = completion_plan_coordinate_data['hole_depth_y']
    hole_depth_z = completion_plan_coordinate_data['hole_depth_z']
    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_insert_wen_zi = "insert into jun_zhong_hole(zhong_row_id, zhong_hole_num,  zhong_x,  zhong_y,  zhong_z)" \
                        " values(%s, %s, %s, %s, %s) "
    cur.execute(sql_insert_wen_zi,
                (id, hole_number, hole_depth_x, hole_depth_y, hole_depth_z))
    db.commit()
    db.close()


# Insert_jun_zhong_hole('16071工作面中部底板巷', 15, 10)


def Insert_jun_pao_cad(tunnel_name, row_id, hole_number):
    tunnel_Data = get_tunnel_datas(tunnel_name)
    she_pao_kai_x = tunnel_Data['she_pao_kai_x']
    heng_xiang_jian_ju = tunnel_Data['heng_xiang_jian_ju']
    shu_xiang_jian_ju = tunnel_Data['shu_xiang_jian_ju']
    mei_pai_zu_shu = tunnel_Data['mei_pai_zu_shu']
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']
    current_row_number = int(row_data['row_id'])  # 该组钻孔排号数字
    pai_hao_ti_qu = Pai_hao_ti_qu(current_row_number)  # rundowm提取

    jun_pao_data = get_jun_pao(tunnel_name, row_id, hole_number)
    jun_pao_kai_x = jun_pao_data['jun_pao_kai_x']
    jun_pao_kai_y = jun_pao_data['jun_pao_kai_y']
    jun_pao_kai_z = jun_pao_data['jun_pao_kai_z']
    jun_pao_kai_cad_x = jun_pao_kai_x + she_pao_kai_x + heng_xiang_jian_ju * (
        int(current_row_number / mei_pai_zu_shu))
    jun_pao_kai_cad_y = jun_pao_kai_y + she_pao_kai_x + shu_xiang_jian_ju * (current_row_number - pai_hao_ti_qu)
    jun_pao_kai_cad_z = jun_pao_kai_z

    if jun_pao_data['jun_pao_see_coal_x'] == None:
        jun_pao_see_coal_cad_x = None
        jun_pao_see_coal_cad_y = None
        jun_pao_see_coal_cad_z = None
    else:
        jun_pao_see_coal_x = jun_pao_data['jun_pao_see_coal_x']
        jun_pao_see_coal_y = jun_pao_data['jun_pao_see_coal_y']
        jun_pao_see_coal_z = jun_pao_data['jun_pao_see_coal_z']
        jun_pao_see_coal_cad_x = jun_pao_see_coal_x + she_pao_kai_x + heng_xiang_jian_ju * (
            int(current_row_number / mei_pai_zu_shu))
        jun_pao_see_coal_cad_y = jun_pao_see_coal_y + she_pao_kai_x + shu_xiang_jian_ju * (
                current_row_number - pai_hao_ti_qu)
        jun_pao_see_coal_cad_z = jun_pao_see_coal_z

    if jun_pao_data['jun_pao_see_ceil_x'] == None:
        jun_pao_see_ceil_cad_x = None
        jun_pao_see_ceil_cad_y = None
        jun_pao_see_ceil_cad_z = None
    else:
        jun_pao_see_ceil_x = jun_pao_data['jun_pao_see_ceil_x']
        jun_pao_see_ceil_y = jun_pao_data['jun_pao_see_ceil_y']
        jun_pao_see_ceil_z = jun_pao_data['jun_pao_see_ceil_z']
        jun_pao_see_ceil_cad_x = jun_pao_see_ceil_x + she_pao_kai_x + heng_xiang_jian_ju * (
            int(current_row_number / mei_pai_zu_shu))
        jun_pao_see_ceil_cad_y = jun_pao_see_ceil_y + she_pao_kai_x + shu_xiang_jian_ju * (
                current_row_number - pai_hao_ti_qu)
        jun_pao_see_ceil_cad_z = jun_pao_see_ceil_z

    jun_pao_zhong_kong_x = jun_pao_data['jun_pao_zhong_kong_x']
    jun_pao_zhong_kong_y = jun_pao_data['jun_pao_zhong_kong_y']
    jun_pao_zhong_kong_z = jun_pao_data['jun_pao_zhong_kong_z']
    jun_pao_zhong_kong_cad_x = jun_pao_zhong_kong_x + she_pao_kai_x + heng_xiang_jian_ju * (
        int(current_row_number / mei_pai_zu_shu))
    jun_pao_zhong_kong_cad_y = jun_pao_zhong_kong_y + she_pao_kai_x + shu_xiang_jian_ju * (
            current_row_number - pai_hao_ti_qu)
    jun_pao_zhong_kong_cad_z = jun_pao_zhong_kong_z

    if jun_pao_data['jun_pao_position_pen_x'] == None:
        jun_pao_position_pen_cad_x = None
        jun_pao_position_pen_cad_y = None
        jun_pao_position_pen_cad_z = None
    else:
        jun_pao_position_pen_x = jun_pao_data['jun_pao_position_pen_x']
        jun_pao_position_pen_y = jun_pao_data['jun_pao_position_pen_y']
        jun_pao_position_pen_z = jun_pao_data['jun_pao_position_pen_z']
        jun_pao_position_pen_cad_x = jun_pao_position_pen_x + she_pao_kai_x + heng_xiang_jian_ju * (
            int(current_row_number / mei_pai_zu_shu))
        jun_pao_position_pen_cad_y = jun_pao_position_pen_y + she_pao_kai_x + shu_xiang_jian_ju * (
                current_row_number - pai_hao_ti_qu)
        jun_pao_position_pen_cad_z = jun_pao_position_pen_z

    if jun_pao_data['jun_pao_position_ya_x'] == None:
        jun_pao_position_ya_cad_x = None
        jun_pao_position_ya_cad_y = None
        jun_pao_position_ya_cad_z = None
    else:
        jun_pao_position_ya_x = jun_pao_data['jun_pao_position_ya_x']
        jun_pao_position_ya_y = jun_pao_data['jun_pao_position_ya_y']
        jun_pao_position_ya_z = jun_pao_data['jun_pao_position_ya_z']
        jun_pao_position_ya_cad_x = jun_pao_position_ya_x + she_pao_kai_x + heng_xiang_jian_ju * (
            int(current_row_number / mei_pai_zu_shu))
        jun_pao_position_ya_cad_y = jun_pao_position_ya_y + she_pao_kai_x + shu_xiang_jian_ju * (
                current_row_number - pai_hao_ti_qu)
        jun_pao_position_ya_cad_z = jun_pao_position_ya_z

    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_insert_jun_pao_cad = "insert into jun_pao_cad(jun_pao_kai_cad_x, " \
                             "jun_pao_kai_cad_y, " \
                             "jun_pao_kai_cad_z," \
                             " jun_pao_see_coal_cad_x, jun_pao_see_coal_cad_y, jun_pao_see_coal_cad_z, " \
                             " jun_pao_see_ceil_cad_x, jun_pao_see_ceil_cad_y, jun_pao_see_ceil_cad_z, " \
                             "jun_pao_zhong_kong_cad_x, jun_pao_zhong_kong_cad_y, " \
                             "jun_pao_zhong_kong_cad_z, jun_pao_position_pen_cad_x, jun_pao_position_pen_cad_y, " \
                             "jun_pao_position_pen_cad_z, jun_pao_position_ya_cad_x, jun_pao_position_ya_cad_y, " \
                             "jun_pao_position_ya_cad_z, " \
                             "jun_pao_row_id, jun_pao_hole_num" \
                             ") values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cur.execute(sql_insert_jun_pao_cad,
                (jun_pao_kai_cad_x, jun_pao_kai_cad_y, jun_pao_kai_cad_z,
                 jun_pao_see_coal_cad_x, jun_pao_see_coal_cad_y, jun_pao_see_coal_cad_z,
                 jun_pao_see_ceil_cad_x, jun_pao_see_ceil_cad_y, jun_pao_see_ceil_cad_z,
                 jun_pao_zhong_kong_cad_x, jun_pao_zhong_kong_cad_y,
                 jun_pao_zhong_kong_cad_z, jun_pao_position_pen_cad_x, jun_pao_position_pen_cad_y,
                 jun_pao_position_pen_cad_z, jun_pao_position_ya_cad_x, jun_pao_position_ya_cad_y,
                 jun_pao_position_ya_cad_z, id, hole_number))
    db.commit()
    db.close()


# Insert_jun_pao_cad('16071工作面中部底板巷', 15, 10)


def get_jun_pao_cad(tunnel_name, row_id, hole_number):
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']
    Datas = jun_pao_cad.objects.filter(jun_pao_row=id, jun_pao_hole_num=hole_number).first()
    if Datas is not None:
        Data = model_to_dict(Datas)
    else:
        Data = {}
    return Data


# print(get_jun_pao_cad('16071工作面中部底板巷', 15, 11))


def Insert_zhun_kong_graph1(tunnel_name, row_id, hole_number):
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']
    jun_pao_cad_data = get_jun_pao_cad(tunnel_name, row_id, hole_number)
    graph1_x = jun_pao_cad_data['jun_pao_zhong_kong_cad_x']
    graph1_y = jun_pao_cad_data['jun_pao_zhong_kong_cad_y']
    graph1_z = jun_pao_cad_data['jun_pao_zhong_kong_cad_z']

    graph2_x = jun_pao_cad_data['jun_pao_see_ceil_cad_x']
    graph2_y = jun_pao_cad_data['jun_pao_see_ceil_cad_y']
    graph2_z = jun_pao_cad_data['jun_pao_see_ceil_cad_z']

    graph3_x = jun_pao_cad_data['jun_pao_see_coal_cad_x']
    graph3_y = jun_pao_cad_data['jun_pao_see_coal_cad_y']
    graph3_z = jun_pao_cad_data['jun_pao_see_coal_cad_z']

    graph4_x = jun_pao_cad_data['jun_pao_position_pen_cad_x']
    graph4_y = jun_pao_cad_data['jun_pao_position_pen_cad_y']
    graph4_z = jun_pao_cad_data['jun_pao_position_pen_cad_z']

    graph5_x = jun_pao_cad_data['jun_pao_position_ya_cad_x']
    graph5_y = jun_pao_cad_data['jun_pao_position_ya_cad_y']
    graph5_z = jun_pao_cad_data['jun_pao_position_ya_cad_z']

    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_insert_zhun_kong_graph1 = "insert into zhun_kong_graph1(graph1_x, graph1_y, graph1_z, graph2_x, graph2_y, " \
                                  "graph2_z, graph3_x, graph3_y, graph3_z, graph4_x, graph4_y, graph4_z, graph5_x," \
                                  " graph5_y, graph5_z, graph1_row_id, graph1_hole_num) values(%s, %s, %s, %s, %s, %s," \
                                  " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cur.execute(sql_insert_zhun_kong_graph1,
                (graph1_x, graph1_y, graph1_z, graph2_x, graph2_y,
                 graph2_z, graph3_x, graph3_y, graph3_z, graph4_x,
                 graph4_y, graph4_z, graph5_x, graph5_y, graph5_z,
                 id, hole_number))
    db.commit()
    db.close()


Insert_zhun_kong_graph1('16071工作面中部底板巷', 15, 10)


def Insert_pao_wen_zi(tunnel_name, row_id, hole_number):
    jun_pao_cad_data = get_jun_pao_cad(tunnel_name, row_id, hole_number)
    pao_wen_zi_x = jun_pao_cad_data['jun_pao_zhong_kong_cad_x']
    pao_wen_zi_y = jun_pao_cad_data['jun_pao_zhong_kong_cad_y']
    pao_wen_zi_z = jun_pao_cad_data['jun_pao_zhong_kong_cad_z']

    tunnel_Data = get_tunnel_datas(tunnel_name)
    she_pao_kai_x = tunnel_Data['she_pao_kai_x']
    shu_xiang_jian_ju = tunnel_Data['shu_xiang_jian_ju']
    pao_ping_xian = tunnel_Data['pao_ping_xian']
    ping_ping_xian = tunnel_Data['ping_ping_xian']
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']
    current_row_number = int(row_data['row_id'])  # 该组钻孔排号数字
    number = get_numbers(hole_number)[1]
    pai_hao_ti_qu = Pai_hao_ti_qu(current_row_number)  # rundowm提取

    pao_wen_zi1_x = jun_pao_cad_data['jun_pao_zhong_kong_cad_x']
    pao_wen_zi1_y = she_pao_kai_x + shu_xiang_jian_ju * (current_row_number - pai_hao_ti_qu) - pao_ping_xian - \
                    (number % int(row_id)) * ping_ping_xian

    pao_wen_zi1_z = jun_pao_cad_data['jun_pao_zhong_kong_cad_z']

    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_insert_pao_wen_zi = "insert into pao_wen_zi(pao_wen_zi_x, pao_wen_zi_y, pao_wen_zi_z, pao_wen_zi1_x, " \
                            "pao_wen_zi1_y, " \
                            "pao_wen_zi1_z, pao_row_id, pao_hole_num) values(%s, %s, %s, %s, %s, %s," \
                            " %s, %s)"
    cur.execute(sql_insert_pao_wen_zi,
                (pao_wen_zi_x, pao_wen_zi_y, pao_wen_zi_z,
                 pao_wen_zi1_x, pao_wen_zi1_y, pao_wen_zi1_z,
                 id, hole_number))
    db.commit()
    db.close()


# Insert_pao_wen_zi('16071工作面中部底板巷', 15, 11)


def Insert_pao_graph1(tunnel_name, row_id, hole_number):
    jun_pao_cad_data = get_jun_pao_cad(tunnel_name, row_id, hole_number)

    tunnel_Data = get_tunnel_datas(tunnel_name)
    she_pao_kai_x = tunnel_Data['she_pao_kai_x']
    she_pao_kai_y = tunnel_Data['she_pao_kai_y']
    heng_xiang_jian_ju = tunnel_Data['heng_xiang_jian_ju']
    shu_xiang_jian_ju = tunnel_Data['shu_xiang_jian_ju']
    mei_pai_zu_shu = tunnel_Data['mei_pai_zu_shu']
    pao_ping_xian = tunnel_Data['pao_ping_xian']
    ping_ping_xian = tunnel_Data['ping_ping_xian']
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']
    row_x = row_data['row_x']
    current_row_number = int(row_data['row_id'])  # 该组钻孔排号数字
    pai_hao_ti_qu = Pai_hao_ti_qu(current_row_number)  # rundowm提取
    arch_radius = tunnel_Data['arch_radius']
    hole_design_data = get_hole_design_datas(tunnel_name, row_id, hole_number)
    hole_number_id = hole_design_data['id']
    design_elevation_angel = hole_design_data['design_elevation_angel']
    design_hole_height = hole_design_data['design_hole_height']
    hole_depth = hole_design_data['hole_depth']
    number = get_numbers(hole_number)[1]
    zuobiao = matching_function(tunnel_name, row_id, number, row_x)
    # 用匹配函数匹配不在范围内结束程序
    if zuobiao is False:
        print('匹配错误！')
        os._exit(0)
    rock_section = zuobiao[4]  # 设计岩段
    coal_section = zuobiao[5]  # 设计煤段
    see_ceil = coal_section + rock_section
    coal_seam_thickness = zuobiao[5]  # 煤层厚度

    pao_graph1_x = jun_pao_cad_data['jun_pao_zhong_kong_cad_x']
    pao_graph1_y = she_pao_kai_x + shu_xiang_jian_ju * (current_row_number - pai_hao_ti_qu) - pao_ping_xian - \
                   (number % int(row_id)) * ping_ping_xian
    pao_graph1_z = jun_pao_cad_data['jun_pao_zhong_kong_cad_z']

    pao_graph2_x = jun_pao_cad_data['jun_pao_see_ceil_cad_x']
    pao_graph2_y = she_pao_kai_x + shu_xiang_jian_ju * (current_row_number - pai_hao_ti_qu) - pao_ping_xian - \
                   (number % int(row_id)) * ping_ping_xian
    pao_graph2_z = jun_pao_cad_data['jun_pao_see_ceil_cad_z']

    pao_graph3_x = jun_pao_cad_data['jun_pao_see_coal_cad_x']
    pao_graph3_y = she_pao_kai_x + shu_xiang_jian_ju * (current_row_number - pai_hao_ti_qu) - pao_ping_xian - \
                   (number % int(row_id)) * ping_ping_xian
    pao_graph3_z = jun_pao_cad_data['jun_pao_see_coal_cad_z']

    pao_graph4_x = jun_pao_cad_data['jun_pao_position_pen_cad_x']
    pao_graph4_y = she_pao_kai_x + shu_xiang_jian_ju * (current_row_number - pai_hao_ti_qu) - pao_ping_xian - \
                   (number % int(row_id)) * ping_ping_xian
    pao_graph4_z = jun_pao_cad_data['jun_pao_position_pen_cad_z']

    pao_graph5_x = jun_pao_cad_data['jun_pao_position_ya_cad_x']
    pao_graph5_y = she_pao_kai_x + shu_xiang_jian_ju * (current_row_number - pai_hao_ti_qu) - pao_ping_xian - \
                   (number % int(row_id)) * ping_ping_xian
    pao_graph5_z = jun_pao_cad_data['jun_pao_position_ya_cad_z']

    db = pymysql.connect(host="localhost", user="root", password="123456", db='hpu_mining', port=3306)
    cur = db.cursor()
    sql_insert_pao_graph1 = "insert into pao_graph1(pao_graph1_x, pao_graph1_y, pao_graph1_z, pao_graph2_x," \
                            " pao_graph2_y, pao_graph2_z, pao_graph3_x, pao_graph3_y, pao_graph3_z," \
                            " pao_graph4_x, pao_graph4_y, pao_graph4_z, pao_graph5_x, pao_graph5_y," \
                            " pao_graph5_z, pao_graph1_row_id, pao_graph1_hole_num) values(%s, %s, %s, %s, %s, %s," \
                            " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cur.execute(sql_insert_pao_graph1,
                (pao_graph1_x, pao_graph1_y, pao_graph1_z, pao_graph2_x, pao_graph2_y, pao_graph2_z,
                 pao_graph3_x, pao_graph3_y, pao_graph3_z, pao_graph4_x, pao_graph4_y, pao_graph4_z,
                 pao_graph5_x, pao_graph5_y, pao_graph5_z, id, hole_number))
    db.commit()
    db.close()


# Insert_pao_graph1('16071工作面中部底板巷', 15, 11)
from pyautocad import *
import random
from sklearn import linear_model
import numpy as np

model = linear_model.LinearRegression()

acad = Autocad(create_if_not_exists=True)

clr = acad.Application.GetInterfaceObject("AutoCAD.AcCmcolor.24")


def set_color(color):
    if color == '白':
        r = 255
        g = 255
        b = 255
    elif color == '黑':
        r = 0
        g = 0
        b = 0
    elif color == '红':
        r = 255
        g = 0
        b = 0
    elif color == '黄':
        r = 255
        g = 255
        b = 0
    elif color == '蓝':
        r = 0
        g = 0
        b = 255
    elif color == '绿':
        r = 0
        g = 255
        b = 0
    elif color == '灰':
        r = 192
        g = 192
        b = 192
    return clr.setRGB(r, g, b)


def sui_ji(point):
    polygon = random.choice(['三角形', '正方形', '五边形'])
    pnts = []
    if polygon == '三角形':
        pnts = [point + APoint(0, 1), point + APoint(-1, -1), point + APoint(1, -1)]
    elif polygon == '正方形':
        pnts = [point + APoint(-1, 1), point + APoint(-1, -1), point + APoint(1, -1), point + APoint(1, 1)]
    elif polygon == '五边形':
        pnts = [point + APoint(-0.5, 1), point + APoint(-1, 0), point + APoint(-0.5, -1), point + APoint(0.5, -1),
                point + APoint(1, 0), point + APoint(0.5, 1)]
    pnts = [j for i in pnts for j in i]
    pnts = aDouble(pnts)
    pline = acad.model.AddPolyLine(pnts)
    pline.Closed = True


def get_regression(X, Y):
    x = np.array(X).reshape(-1, 1)
    y = np.array(Y).reshape(-1, 1)
    if not x and not y:
        print('列表为空！')
        return 0, 0, 0
    else:
        hui_gui = linear_model.LinearRegression()
        hui_gui.fit(x, y)
        hui_gui_pred = hui_gui.predict(x)
        xie_lv = hui_gui.coef_
        jie_ju = hui_gui.intercept_
        return hui_gui_pred, xie_lv, jie_ju


def draw_picture(tunnel_name, row_id):  # 预测顶板线
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']
    Datas = jun_pao_cad.objects.filter(jun_pao_row_id=id)
    cunchu = pd.DataFrame()
    for i in range(len(Datas)):
        Data = model_to_dict(Datas[i])
        if Data['jun_pao_see_ceil_cad_x'] or Data['jun_pao_see_ceil_cad_y'] is not None:
            cunchu = cunchu.append(Data, ignore_index=True)

    for i in range(len(cunchu)):
        cunchu['jun_pao_hole_num'].loc[i] = int((cunchu['jun_pao_hole_num'].loc[i]))
    cunchu = cunchu.sort_values('jun_pao_hole_num', ascending=True)
    hanshu = get_regression(cunchu['jun_pao_see_ceil_cad_x'], cunchu['jun_pao_see_ceil_cad_y'])
    y_pred = hanshu[0]
    color = input("请输入颜色：")
    set_color(color)
    p1 = APoint(cunchu['jun_pao_see_ceil_cad_x'].loc[0], y_pred[0])
    p2 = APoint(cunchu['jun_pao_see_ceil_cad_x'].loc[len(cunchu) - 1], y_pred[-1])
    line = acad.model.AddLine(p1, p2)
    line.TrueColor = clr
    line.LineWeight = 20
    # xian = APoint(cunchu['jun_pao_see_ceil_x'].loc[2], y_pred[2])
    # if hanshu[2]< 0:
    #     textString = "y = {}x{}".format(float(hanshu[1]), float(hanshu[2]))
    # else:
    #     textString = "y = {}x+{}".format(float(hanshu[1]), float(hanshu[2]))
    # textObj = acad.model.AddText(textString, xian, 1.25)
    # textObj.Alignment = 2
    # textObj.TrueColor = clr
    acad.ActiveDocument.preferences.LineweightDisplay = 1
    acad.ActiveDocument.Application.ZoomAll()
    acad.ActiveDocument.Application.Update()


# def draw_picture(tunnel_name, row_id):  # 预测顶板线
#     row_data = get_row_datas(tunnel_name, row_id)
#     id = row_data['id']
#     Datas = jun_pao.objects.filter(jun_pao_row_id=id)
#     cunchu = pd.DataFrame()
#     for i in range(len(Datas)):
#         Data = model_to_dict(Datas[i])
#         if Data['jun_pao_see_ceil_x'] or Data['jun_pao_see_ceil_y'] is not None:
#             cunchu = cunchu.append(Data, ignore_index=True)
#
#     for i in range(len(cunchu)):
#         cunchu['jun_pao_hole_num'].loc[i] = int((cunchu['jun_pao_hole_num'].loc[i]))
#     cunchu = cunchu.sort_values('jun_pao_hole_num', ascending=True)
#     hanshu = get_regression(cunchu['jun_pao_see_ceil_x'], cunchu['jun_pao_see_ceil_y'])
#     y_pred = hanshu[0]
#     color = input("请输入颜色：")
#     set_color(color)
#     p1 = APoint(cunchu['jun_pao_see_ceil_x'].loc[0], y_pred[0])
#     p2 = APoint(cunchu['jun_pao_see_ceil_x'].loc[len(cunchu)-1], y_pred[-1])
#     line = acad.model.AddLine(p1, p2)
#     line.TrueColor = clr
#     line.LineWeight = 20
#     AngleVertex = APoint(cunchu['jun_pao_see_ceil_x'].loc[0], y_pred[0])
#     FirstEndPoint = APoint(cunchu['jun_pao_see_ceil_x'].loc[2], y_pred[0])
#     SecondEndPoint = APoint(cunchu['jun_pao_see_ceil_x'].loc[2], y_pred[2])
#     TextPoint = APoint(cunchu['jun_pao_see_ceil_x'].loc[3], y_pred[3])
#     dimAngObj = acad.model.AddDimAngular(AngleVertex, FirstEndPoint, SecondEndPoint, TextPoint)
#     dimAngObj.TrueColor = clr
#
#     # xian = APoint(cunchu['jun_pao_see_ceil_x'].loc[2], y_pred[2])
#     # if hanshu[2]< 0:
#     #     textString = "y = {}x{}".format(float(hanshu[1]), float(hanshu[2]))
#     # else:
#     #     textString = "y = {}x+{}".format(float(hanshu[1]), float(hanshu[2]))
#     # textObj = acad.model.AddText(textString, xian, 1.25)
#     # textObj.Alignment = 2
#     # textObj.TrueColor = clr
#     acad.ActiveDocument.preferences.LineweightDisplay = 1
#     acad.ActiveDocument.Application.ZoomAll()
#     acad.ActiveDocument.Application.Update()

# draw_picture('16071工作面中部底板巷', 15)

def draw_picture1(tunnel_name, row_id):  # 预测底板线
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']
    Datas = jun_pao_cad.objects.filter(jun_pao_row_id=id)
    cunchu = pd.DataFrame()
    for i in range(len(Datas)):
        Data = model_to_dict(Datas[i])
        if Data['jun_pao_see_coal_cad_x'] or Data['jun_pao_see_coal_cad_y'] is not None:
            cunchu = cunchu.append(Data, ignore_index=True)

    for i in range(len(cunchu)):
        cunchu['jun_pao_hole_num'].loc[i] = int((cunchu['jun_pao_hole_num'].loc[i]))
    cunchu = cunchu.sort_values('jun_pao_hole_num', ascending=True)
    hanshu = get_regression(cunchu['jun_pao_see_coal_cad_x'], cunchu['jun_pao_see_coal_cad_y'])
    y_pred = hanshu[0]
    color = input("请输入颜色：")
    set_color(color)
    p1 = APoint(cunchu['jun_pao_see_coal_cad_x'].loc[0], y_pred[0])
    p2 = APoint(cunchu['jun_pao_see_coal_cad_x'].loc[len(cunchu) - 1], y_pred[-1])
    line = acad.model.AddLine(p1, p2)
    line.TrueColor = clr
    line.LineWeight = 20
    # xian = APoint(cunchu['jun_pao_see_ceil_x'].loc[2], y_pred[2])
    # if hanshu[2] < 0:
    #     textString = "y = {}x{}".format(float(hanshu[1]), float(hanshu[2]))
    # else:
    #     textString = "y = {}x+{}".format(float(hanshu[1]), float(hanshu[2]))
    # textObj = acad.model.AddText(textString, xian, 1.25)
    # textObj.Alignment = 2
    # textObj.TrueColor = clr
    acad.ActiveDocument.preferences.LineweightDisplay = 1
    acad.ActiveDocument.Application.ZoomAll()
    acad.ActiveDocument.Application.Update()


# draw_picture1('16071工作面中部底板巷', 15)


def draw_picture2(tunnel_name, row_id):  # 顶板连线
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']
    Datas = jun_pao.objects.filter(jun_pao_row_id=id)
    cunchu = pd.DataFrame()
    for i in range(len(Datas)):
        Data = model_to_dict(Datas[i])
        if Data['jun_pao_see_ceil_x'] or Data['jun_pao_see_ceil_y'] is not None:
            cunchu = cunchu.append(Data, ignore_index=True)

    for i in range(len(cunchu)):
        cunchu['jun_pao_hole_num'].loc[i] = int((cunchu['jun_pao_hole_num'].loc[i]))
    cunchu = cunchu.sort_values('jun_pao_hole_num', ascending=True)

    color = input("请输入颜色：")
    set_color(color)
    pnts = []
    for i in range(len(cunchu['jun_pao_see_ceil_x'])):
        if pd.isnull(cunchu['jun_pao_see_ceil_x'].loc[i]) is True:
            break
        else:
            p1 = APoint(cunchu['jun_pao_see_ceil_x'].loc[i], cunchu['jun_pao_see_ceil_y'].loc[i])
            pnts.append(p1)
            sui_ji(p1)
    pnts = [j for i in pnts for j in i]
    pnts = aDouble(pnts)  # 数据类型转化为双精度浮点数
    plineObj = acad.model.AddPolyLine(pnts)
    plineObj.SetWidth(15, 15, 15)
    plineObj.TrueColor = clr
    acad.ActiveDocument.preferences.LineweightDisplay = 1
    acad.ActiveDocument.Application.ZoomAll()
    acad.ActiveDocument.Application.Update()


# draw_picture2('16071工作面中部底板巷', 15)


def draw_picture3(tunnel_name, row_id):  # 孔号文字
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']
    Datas = pao_wen_zi.objects.filter(pao_row_id=id)
    cunchu = pd.DataFrame()
    for i in range(len(Datas)):
        Data = model_to_dict(Datas[i])
        if Data['pao_wen_zi_x'] or Data['pao_wen_zi_y'] is not None:
            cunchu = cunchu.append(Data, ignore_index=True)

    for i in range(len(cunchu)):
        cunchu['pao_hole_num'].loc[i] = int((cunchu['pao_hole_num'].loc[i]))
    cunchu = cunchu.sort_values('pao_hole_num', ascending=True)

    color = input("请输入颜色：")
    set_color(color)
    for i in range(len(cunchu)):
        if pd.isnull(cunchu['pao_wen_zi_x'].loc[i]) is True:
            break
        else:
            p1 = APoint(cunchu['pao_wen_zi_x'].loc[i], cunchu['pao_wen_zi_y'].loc[i])
            textString = "{}#".format(cunchu['pao_hole_num'].loc[i])
            textObj = acad.model.AddText(textString, p1, 1.25)
            textObj.TrueColor = clr


# draw_picture3('16071工作面中部底板巷', 15)


def draw_picture4(tunnel_name, row_id):  # 钻孔岩段坐标
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']
    Datas = jun_pao.objects.filter(jun_pao_row_id=id)
    cunchu = pd.DataFrame()
    for i in range(len(Datas)):
        Data = model_to_dict(Datas[i])
        if Data['jun_pao_kai_x'] or Data['jun_pao_kai_y'] is not None:
            cunchu = cunchu.append(Data, ignore_index=True)

    for i in range(len(cunchu)):
        cunchu['jun_pao_hole_num'].loc[i] = int((cunchu['jun_pao_hole_num'].loc[i]))
    cunchu = cunchu.sort_values('jun_pao_hole_num', ascending=True)

    color = input("请输入颜色：")
    set_color(color)
    for i in range(len(cunchu['jun_pao_kai_x'])):
        if pd.isnull(cunchu['jun_pao_kai_x'].loc[i]) is True:
            break
        else:
            p1 = APoint(cunchu['jun_pao_kai_x'].loc[i], cunchu['jun_pao_kai_y'].loc[i])
            p2 = APoint(cunchu['jun_pao_see_coal_x'].loc[i], cunchu['jun_pao_see_coal_y'].loc[i])
            line = acad.model.AddLine(p1, p2)
            line.TrueColor = clr
            line.LineWeight = 20


# draw_picture4('16071工作面中部底板巷', 15)


def draw_picture5(tunnel_name, row_id):  # 钻孔煤段坐标
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']
    Datas = jun_pao.objects.filter(jun_pao_row_id=id)
    cunchu = pd.DataFrame()
    for i in range(len(Datas)):
        Data = model_to_dict(Datas[i])
        if Data['jun_pao_see_coal_x'] or Data['jun_pao_see_coal_y'] is not None:
            cunchu = cunchu.append(Data, ignore_index=True)

    for i in range(len(cunchu)):
        cunchu['jun_pao_hole_num'].loc[i] = int((cunchu['jun_pao_hole_num'].loc[i]))
    cunchu = cunchu.sort_values('jun_pao_hole_num', ascending=True)

    color = input("请输入颜色：")
    set_color(color)
    for i in range(len(cunchu['jun_pao_see_coal_x'])):
        if pd.isnull(cunchu['jun_pao_see_coal_x'].loc[i]) is True:
            break
        else:
            p1 = APoint(cunchu['jun_pao_see_coal_x'].loc[i], cunchu['jun_pao_see_coal_y'].loc[i])
            p2 = APoint(cunchu['jun_pao_zhong_kong_x'].loc[i], cunchu['jun_pao_zhong_kong_y'].loc[i])
            line = acad.model.AddLine(p1, p2)
            line.TrueColor = clr
            line.LineWeight = 30


# draw_picture5('16071工作面中部底板巷', 15)


def draw_picture6(tunnel_name, row_id):  # 底板连线
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']
    Datas = jun_pao.objects.filter(jun_pao_row_id=id)
    cunchu = pd.DataFrame()
    for i in range(len(Datas)):
        Data = model_to_dict(Datas[i])
        if Data['jun_pao_see_coal_x'] or Data['jun_pao_see_coal_y'] is not None:
            cunchu = cunchu.append(Data, ignore_index=True)

    for i in range(len(cunchu)):
        cunchu['jun_pao_hole_num'].loc[i] = int((cunchu['jun_pao_hole_num'].loc[i]))
    cunchu = cunchu.sort_values('jun_pao_hole_num', ascending=True)

    color = input("请输入颜色：")
    set_color(color)
    pnts = []
    for i in range(len(cunchu['jun_pao_see_coal_x'])):
        if pd.isnull(cunchu['jun_pao_see_coal_x'].loc[i]) is True:
            break
        else:
            pnts.append(APoint(cunchu['jun_pao_see_coal_x'].loc[i], cunchu['jun_pao_see_coal_y'].loc[i]))
    pnts = [j for i in pnts for j in i]
    pnts = aDouble(pnts)  # 数据类型转化为双精度浮点数
    plineObj = acad.model.AddPolyLine(pnts)
    plineObj.SetWidth(15, 15, 15)
    plineObj.TrueColor = clr
    length = len(cunchu['jun_pao_see_coal_x'])
    half = len(cunchu['jun_pao_see_coal_x']) // 2
    p1 = APoint(cunchu['jun_pao_see_coal_x'].loc[0], cunchu['jun_pao_see_coal_y'].loc[0])
    p2 = APoint(cunchu['jun_pao_see_coal_x'].loc[half], cunchu['jun_pao_see_coal_y'].loc[half])
    p3 = APoint(cunchu['jun_pao_see_coal_x'].loc[length - 1], cunchu['jun_pao_see_coal_y'].loc[length - 1])
    TextPosition = APoint(cunchu['jun_pao_see_coal_x'].loc[half] + 10, cunchu['jun_pao_see_coal_y'].loc[half])
    dimAliObj1 = acad.model.AddDimAligned(p1, p2, TextPosition)
    dimAliObj2 = acad.model.AddDimAligned(p2, p3, TextPosition)
    dimAliObj1.TrueColor = clr
    dimAliObj2.TrueColor = clr
    acad.ActiveDocument.preferences.LineweightDisplay = 1
    acad.ActiveDocument.Application.ZoomAll()
    acad.ActiveDocument.Application.Update()


# draw_picture6('16071工作面中部底板巷', 15)


def draw_picture7(tunnel_name, row_id):  # 排号文字
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']
    Datas = jun_pao.objects.filter(jun_pao_row_id=id)
    cunchu = pd.DataFrame()
    for i in range(len(Datas)):
        Data = model_to_dict(Datas[i])
        if Data['jun_pao_kai_x'] or Data['jun_pao_kai_y'] is not None:
            cunchu = cunchu.append(Data, ignore_index=True)

    for i in range(len(cunchu)):
        cunchu['jun_pao_hole_num'].loc[i] = int((cunchu['jun_pao_hole_num'].loc[i]))
    cunchu = cunchu.sort_values('jun_pao_hole_num', ascending=True)

    color = input("请输入颜色：")
    set_color(color)
    if pd.isnull(cunchu['jun_pao_row'].loc[i]) is True:
        os._exit(0)
    else:
        p1 = APoint(cunchu['jun_pao_kai_x'].loc[i], cunchu['jun_pao_kai_y'].loc[i])
        textString = "{}".format(row_id)
        textObj = acad.model.AddText(textString, p1, 1.25)
        textObj.TrueColor = clr


# draw_picture7('16071工作面中部底板巷', 15)


def draw_picture8(mine_name, tunnel_name, row_id):  # 斜距标注坐标
    work_data = get_work_datas(mine_name)
    up_tunnel_up = work_data['up_tunnel_up']
    down_tunnel_tunnel = work_data['down_tunnel_tunnel']
    qie_yan_qie = work_data['qie_yan_qie']
    tunnel_data = get_tunnel_datas(tunnel_name)
    di_ban_hang_hight = tunnel_data['di_ban_hang_hight']
    hole_height = tunnel_data['hole_height']
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']
    Datas = jun_pao_cad.objects.filter(jun_pao_row_id=id)
    cunchu = pd.DataFrame()
    for i in range(len(Datas)):
        Data = model_to_dict(Datas[i])
        if Data['jun_pao_kai_cad_x'] or Data['jun_pao_kai_cad_y'] is not None:
            cunchu = cunchu.append(Data, ignore_index=True)

    for i in range(len(cunchu)):
        cunchu['jun_pao_hole_num'].loc[i] = int((cunchu['jun_pao_hole_num'].loc[i]))
    cunchu = cunchu.sort_values('jun_pao_hole_num', ascending=True)
    hanshu1 = get_regression(cunchu['jun_pao_kai_cad_x'], cunchu['jun_pao_kai_cad_y'])
    y1_pred = hanshu1[0]
    hanshu2 = get_regression(cunchu['jun_pao_see_coal_cad_x'], cunchu['jun_pao_see_coal_cad_y'])
    y2_pred = hanshu2[0]
    y2_pred_a = hanshu2[1]
    y2_pred_b = hanshu2[2]
    color = input("请输入颜色：")
    set_color(color)
    p1 = APoint(cunchu['jun_pao_kai_cad_x'].loc[0],
                cunchu['jun_pao_kai_cad_y'].loc[0] + di_ban_hang_hight - hole_height)
    p2 = APoint(cunchu['jun_pao_kai_x'].loc[0], y1_pred[0])
    textPoint1 = (p1 + p2) / 2
    dimRotObj1 = acad.model.AddDimAligned(p1, p2, textPoint1)
    dimRotObj1.TextOverride = cunchu['jun_pao_hole_num'].loc[0]

    p3 = APoint(cunchu['jun_pao_see_coal_cad_x'].loc[0], y2_pred[0])  # 左侧
    p4 = APoint(cunchu['jun_pao_kai_x'].loc[len(cunchu) - 1], y2_pred[-1])  # 右侧
    textPoint2 = (p3 + p4) / 2
    dimRotObj2 = acad.model.AddDimAligned(p3, p4, textPoint2)
    dimRotObj2.TextOverride = cunchu['jun_pao_hole_num'].loc[0]

    p5 = APoint(cunchu['jun_pao_see_coal_cad_x'].loc[12] + up_tunnel_up,
                y2_pred_a * (cunchu['jun_pao_see_coal_cad_x'].loc[12] + up_tunnel_up) + y2_pred_b)
    textPoint3 = (p3 + p5) / 2
    dimRotObj3 = acad.model.AddDimAligned(p3, p5, textPoint3)
    dimRotObj3.TextOverride = cunchu['jun_pao_hole_num'].loc[0]

    p6 = APoint(cunchu['jun_pao_see_coal_cad_x'].loc[12] + down_tunnel_tunnel,
                y2_pred_a * (cunchu['jun_pao_see_coal_cad_x'].loc[12] + down_tunnel_tunnel) + y2_pred_b)
    textPoint4 = (p4 + p6) / 2
    dimRotObj4 = acad.model.AddDimAligned(p4, p6, textPoint4)
    dimRotObj4.TextOverride = cunchu['jun_pao_hole_num'].loc[0]

    # dimRotObj.TrueColor = clr
    # dimRotObj.Update()


# draw_picture8('16071工作面中部底板巷', 15)


def draw_picture9(tunnel_name, row_id):  # 图例标注坐标
    row_data = get_row_datas(tunnel_name, row_id)
    id = row_data['id']
    Datas = Completion_plan_coordinate.objects.filter(completion_row_id=id)
    cunchu = pd.DataFrame()
    for i in range(len(Datas)):
        Data = model_to_dict(Datas[i])
        if Data['pen_hole_x'] or Data['pen_hole_y'] is not None:
            cunchu = cunchu.append(Data, ignore_index=True)

    for i in range(len(cunchu)):
        cunchu['completion_hole_num'].loc[i] = int((cunchu['completion_hole_num'].loc[i]))
    cunchu = cunchu.sort_values('completion_hole_num', ascending=True)

    color = input("请输入颜色：")
    set_color(color)
    for i in range(len(cunchu)):
        if pd.isnull(cunchu['pen_hole_x'].loc[i]) is True:
            break
        else:
            p1 = APoint(cunchu['pen_hole_x'].loc[i], cunchu['pen_hole_y'].loc[i])
            textString = "{}#".format(cunchu['completion_hole_num'].loc[i])
            textObj = acad.model.AddText(textString, p1, 1.25)
            textObj.TrueColor = clr
# draw_picture9('16071工作面中部底板巷', 15)
