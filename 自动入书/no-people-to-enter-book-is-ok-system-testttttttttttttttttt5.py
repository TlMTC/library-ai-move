import pandas as pd
import requests
from bs4 import BeautifulSoup

def search_isbn_in_excel(isbn):
    # 加载Excel文件
    excel_file = r'E:\桌面\class\code\no-people-to-enter-book-is-ok-system\mo-dou.xlsx'
    df = pd.read_excel(excel_file)  
    
    # 转换输入的ISBN为字符串并进行匹配
    isbn_str = str(isbn)
    
    # 在首列寻找与输入的ISBN相同的值，并返回所在行的索引
    matches_index = df.index[df.iloc[:, 0].astype(str) == isbn_str].tolist()
    
    # 提取匹配行的数据
    matches = df.loc[matches_index]
    
    # 格式化输出匹配行的内容
    output = ""
    for index, row in matches.iterrows():
        output += "isbn: {}\n".format(row['isbn'])
        output += "name: {}\n".format(row['name'])
        output += "出版社: {}\n".format(row['出版社'])
        output += "作者: {}\n".format(row['作者'])
        output += "\n"
    
    return output

isbn = input("请输入要查找的ISBN：")
matches_output = search_isbn_in_excel(isbn)
print("找到匹配行的内容：\n", matches_output)

# 登录页面的URL
login_url = "https://eclass.tongnam.edu.mo/login.php"

# 登录请求的参数
payload = {
    'UserLogin': 'helper',
    'UserPassword': 'tn1721605',
    'submit': '登入'
}

# 创建会话对象
session = requests.Session()

# 发送登录POST请求
response = session.post(login_url, data=payload)

# 检查登录是否成功
if response.status_code == 200:
    # 登录成功，继续其他操作
    print("登录成功")
else :
    print("登陆失败")

# 登录成功后的URL
home_url = "https://eclass.tongnam.edu.mo/home/library_sys/admin/book/book_new.php"

# 发送GET请求访问页面
response = session.get(home_url)

# 检查响应是否成功
if response.status_code == 200:
    # 页面访问成功，可以继续其他操作
    print("页面访问成功")
else:
    print("页面访问失败")

# 使用BeautifulSoup解析页面内容
soup = BeautifulSoup(response.content, 'html.parser')

# 查找目标输入框元素
input_element = soup.find('input', id='BookTitle')

# 修改输入框的值
if input_element is not None:
    input_element['value'] = '要填入的值'
    print("成功填入输入框")

    # 处理其他操作...
else:
    print("未找到目标输入框")

# 使用BeautifulSoup解析页面内容
soup = BeautifulSoup(response.content, 'html.parser')

# 查找目标按钮元素
button_element = soup.find('input', id='SubmitBtn')

# 模拟点击按钮
if button_element is not None:
    # 获取按钮的onclick属性值
    onclick_value = button_element['onclick']

    # 提取onclick中的函数名
    function_name = onclick_value.split('(')[0]

    # 构造调用JavaScript函数的语句
    javascript_code = '{}();'.format(function_name)

    # 执行JavaScript代码（这里只是示意，并不能直接在Python代码中执行 JavaScript）
    print("模拟点击按钮成功")

# 提交表单的URL
submit_url = "https://eclass.tongnam.edu.mo/home/library_sys/admin/book/book_new.php"

# 填写输入表单的数据
form_data = {
    'input_field1': 'value1',
    'input_field2': 'value2',
    # 其他表单字段...
}

# 发送POST请求
response = session.post(submit_url, data=form_data, allow_redirects=True)

# 检查响应是否成功
if response.status_code == 200:
    # 页面访问成功，可以继继续其他操作
    print("提交请求成功")
    # 获取跳转后的URL
    redirected_url = response.url
    print("跳转后的网址：", redirected_url)
else:
    print("提交请求失败")

# 使用保持会话的session对象继续发送请求
response = session.get(redirected_url)

# 检查响应是否成功
if response.status_code == 200:
    # 页面访问成功，可以进行后续操作
    print("继续保持会话，并访问跳转后的网址成功")
else:
    print("访问跳转后的网址失败")

# 处理跳转后的页面...
