from pyautocad import Autocad, APoint

# 连接及库导入
acad = Autocad(create_if_not_exists=True)
acad.prompt("Hello! Autocad from Python.")
print(acad.doc.Name)

# 遍历CAD图像对象，修改对象属性
for text in acad.iter_objects('Text'):
    print('text: %s at: %s' % (text.TextString, text.InsertionPoint))
    # 将文本中的“Hi”字符替换为“OK”
    if 'Hi' in text.TextString:
        print('text: %s at: %s' % (text.TextString, text.InsertionPoint))
        # 修改對象屬性
        text1 = str(text.TextString)
        text1 = text1.replace('Hi', 'OK')
        text.TextString = text1
