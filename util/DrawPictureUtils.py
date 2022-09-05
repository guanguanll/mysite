# coding:utf-8
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
import matplotlib.ticker as mticker



def get_regression(chu_li_data2, X, Y):
    x = np.array(chu_li_data2[X]).reshape(-1, 1)
    y = np.array(chu_li_data2[Y]).reshape(-1, 1)
    hui_gui = linear_model.LinearRegression()
    hui_gui.fit(x, y)
    hui_gui_pred = hui_gui.predict(x)
    xie_lv = hui_gui.coef_
    jie_ju = hui_gui.intercept_
    return hui_gui_pred, xie_lv, jie_ju

#画孔间距图
def draw_picture1(Data):

    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    chu_li_data = pd.DataFrame(columns=['孔号', '开孔x', '开孔y', '见煤x', '见煤y', '见顶x', '见顶y', '终孔x', '终孔y'])
    for i in range(len(Data.iloc[:, 0])):
        # if (i + 1) % 2 == 0:
        chu_li_data = chu_li_data.append(Data.iloc[i, :])
    print("*****************************")
    print("chu_li_data2")
    print(chu_li_data)
    print(type(chu_li_data))
    print("*****************************")
    x_1 = np.array(chu_li_data['见顶x']).reshape(-1, 1)
    regression1 = get_regression(chu_li_data, '见顶x', '见顶y')
    y1_pred = regression1[0]

    x_2 = np.array(chu_li_data['见煤x']).reshape(-1, 1)
    regression2 = get_regression(chu_li_data, '见煤x', '见煤y')
    y2_pred = regression2[0]
    # ---------------------------------------------画图
    plt.plot(x_1, y1_pred, color='orange')  # 顶板回归线
    plt.plot(x_2, y2_pred, color='red')  # 底板回归线
    # plt.plot(Datas['X'], Datas['Y'], color='coral')
    plt.text(3, 0.5, '下部底板巷', fontsize=4)
    for i in range(len(chu_li_data)):
        a = chu_li_data.iloc[i, :]
        plt.plot([a['开孔x'], a['见煤x']], [a['开孔y'], a['见煤y']], color='y')
        plt.plot([a['见煤x'], a['见顶x']], [a['见煤y'], a['见顶y']], color='black', linewidth=2)
        plt.plot([a['见顶x'], a['终孔x']], [a['见顶y'], a['终孔y']], color='y')
        plt.text(a['终孔x'], a['终孔y'], str(a['孔号']) + '#', size=15, ha='center', va='center')
    x = np.linspace(0, 20, 100)
    plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f m'))
    plt.gca().xaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f m'))
    plt.title('钻孔竣工剖面图', fontsize=12)
    plt.axis('scaled')
    plt.grid(visible = True)
    # plt.show()
    plt.savefig('static/image/kongjianju.jpg')  # 保存成jpg格式
    plt.clf()

#画柱状图
def draw_picture2(chu_li_data2):
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    regression1 = get_regression(chu_li_data2,'见顶x', '见顶y')
    y1_pred = regression1[0]
    y1_pred = pd.DataFrame(y1_pred).iloc[:, 0]  # 二维转一维
    y_need = chu_li_data2['终孔y']
    # y_need.index = range(0, 11)
    # x_need = chu_li_data2['孔号']
    fan_yan_hole = y_need - y1_pred
    for i in range(len(fan_yan_hole)):
        color_text = 'blue'
        if fan_yan_hole[i] < 0:
            color_text = 'red'
        if i % 2 != 0:
            plt.text(i + 1, 0, i + 1, size=12, ha='center', va='center')
            plt.bar(i + 1, fan_yan_hole[i], color=color_text)
        else:
            plt.bar(i + 1, fan_yan_hole[i], color=color_text)
            plt.text(i + 1, 0, i + 1, size=12, ha='center', va='center')
    plt.title('顶板反验钻孔柱状图', fontsize=12)
    plt.xlabel('孔号', size=12)
    plt.ylabel('见顶误差', size=12)
    plt.xticks(np.arange(0, len(fan_yan_hole) + 1, 1), fontproperties='Times New Roman', size=10)
    plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f m'))
    plt.gca().xaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f #'))
    plt.grid(visible = True)
    plt.savefig('static/image/zhuzhuang.jpg', bbox_inches='tight')  # 保存成jpg格式
    # plt.show()
    plt.clf()
    return fan_yan_hole

#画散点图
def draw_picture3(Data3):
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.plot(Data3.iloc[:, 0], Data3.iloc[:, 1], 'o', c='b')
    plt.plot(Data3.iloc[:, 0], Data3.iloc[:, 1], 'o', c='r')
    plt.gca().xaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f #'))
    plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f m'))
    plt.title('钻孔施工见止煤误差散点图', fontsize=12)
    plt.xlabel('孔号', size=12)
    plt.ylabel('误差', size=12)
    plt.xticks(Data3.iloc[:, 1])
    plt.grid(visible = True)
    # plt.show()
    plt.savefig('static/image/sandian.jpg', bbox_inches='tight')  # 保存成jpg格式
    plt.close()

#画均匀度图
def draw_picture4(Data1, Data2, Data3):
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    line1_x = [-60.09641159, 60.43504929]
    line1_y = [6, 6]
    line2_x = [-60.09641159, 60.43504929]
    line2_y = [9, 9]
    line3_x = [-60.09641159, 60.43504929]
    line3_y = [0, 0]
    line4_x = [-60.09641159, 60.43504929]
    line4_y = [3, 3]
    line5_x = [-60.09641159, 60.43504929]
    line5_y = [-3, -3]
    line6_x = [-60.09641159, 60.43504929]
    line6_y = [-6, -6]

    plt.plot(line1_x, line1_y, linestyle='--', color='black')
    plt.plot(line2_x, line2_y, linestyle='--', color='black')
    plt.plot(line3_x, line3_y, linestyle='--', color='black')
    plt.plot(line4_x, line4_y, linestyle='--', color='black')
    plt.plot(line5_x, line5_y, linestyle='--', color='black')
    plt.plot(line6_x, line6_y, linestyle='--', color='black')

    row_x = -13.47579929
    row1_y = 7.5
    row2_y = 1.5
    row3_y = -4.5
    plt.text(row_x, row1_y, '第15排', size=12, ha='center', va='center')
    plt.text(row_x, row2_y, '第14排', size=12, ha='center', va='center')
    plt.text(row_x, row3_y, '第13排', size=12, ha='center', va='center')

    plt.axvline(x=-5, ls="-", c="red")  # 添加垂直直线
    plt.axvline(x=5, ls="-", c="red")
    plt.text(-5, -6, '16071运输巷', size=12, ha='right', va='bottom', rotation=30)
    plt.text(5, -6, '16071运输底抽巷', size=12, ha='left', va='bottom', rotation=30)

    for i in range(len(Data1.iloc[:, 1])):
        if (i + 1) % 2 != 0:
            row_ji1 = Data1.append(Data1.iloc[i, 0:3], ignore_index=False)
        else:
            row_ou1 = Data1.append(Data1.iloc[i, 0:3], ignore_index=False)
    plt.scatter(row_ji1['见顶x'], row_ji1['见顶y'], marker='o', facecolor='none', edgecolors='deeppink')
    for i in range(len(row_ji1)):
        plt.text(row_ji1.iloc[i, 1], row_ji1.iloc[i, 2], str(row_ji1.iloc[i, 0]) + '#', size=12, ha='center',va='bottom')
    plt.scatter(row_ou1['见顶x'], row_ou1['见顶y'], marker='o', facecolor='none', edgecolors='blue')
    for i in range(len(row_ou1)):
        plt.text(row_ou1.iloc[i, 1], row_ou1.iloc[i, 2], str(row_ou1.iloc[i, 0]) + '#', size=12, ha='center',va='bottom')

    for i in range(len(Data2.iloc[:, 1])):
        if (i + 1) % 2 != 0:
            row_ji2 = Data2.append(Data1.iloc[i, 0:3], ignore_index=False)
        else:
            row_ou2 = Data2.append(Data1.iloc[i, 0:3], ignore_index=False)
    plt.scatter(row_ji2['见顶x'], row_ji2['见顶y'], marker=',', facecolor='none', edgecolors='deeppink')
    for i in range(len(row_ji1)):
        plt.text(row_ji2.iloc[i, 1], row_ji2.iloc[i, 2], str(row_ji2.iloc[i, 0]) + '#', size=12, ha='center',
                 va='bottom')
    plt.scatter(row_ou2['见顶x'], row_ou2['见顶y'], marker=',', facecolor='none', edgecolors='blue')
    for i in range(len(row_ou2)):
        plt.text(row_ou2.iloc[i, 1], row_ou2.iloc[i, 2], str(row_ou2.iloc[i, 0]) + '#', size=12, ha='center',
                 va='bottom')

    for i in range(len(Data3.iloc[:, 1])):
        if (i + 1) % 2 != 0:
            row_ji3 = Data3.append(Data3.iloc[i, 0:3], ignore_index=False)
        else:
            row_ou3 = Data3.append(Data3.iloc[i, 0:3], ignore_index=False)
    plt.scatter(row_ji3['见顶x'], row_ji3['见顶y'], marker='v', facecolor='none', edgecolors='deeppink')
    for i in range(len(row_ji3)):
        plt.text(row_ji3.iloc[i, 1], row_ji3.iloc[i, 2], str(row_ji3.iloc[i, 0]) + '#', size=12, ha='center',
                 va='bottom')
    plt.scatter(row_ou3['见顶x'], row_ou3['见顶y'], marker='v', facecolor='none', edgecolors='blue')
    for i in range(len(row_ou3)):
        plt.text(row_ou3.iloc[i, 1], row_ou3.iloc[i, 2], str(row_ou3.iloc[i, 0]) + '#', size=12, ha='center',
                 va='bottom')
    plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f m'))
    plt.gca().xaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f m'))
    plt.title('钻孔施工均匀度平面图', fontsize=12)
    plt.savefig('static/image/junyundu.jpg', bbox_inches='tight')  # 保存成jpg格式
    plt.close()
