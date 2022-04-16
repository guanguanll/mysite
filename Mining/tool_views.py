import os


# Json格式的http请求返回包
def message_data(code, msg, count, data):
    """
    :param code: 状态码 1：表示执行失败; 0: 表示执行成功
    :param msg: 返回执行结果的信息
    :param count: 返回数据长度
    :param data: 返回的数据包
    :return: 返回Json格式的数据包
    """
    message = {"code": code, "message": msg, "count": count, "data": data}

    return message
