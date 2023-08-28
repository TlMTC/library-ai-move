import requests
from bs4 import BeautifulSoup

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

    # 获取CSRF令牌
    csrf_token = session.cookies.get('csrf_token')

    if csrf_token:
        # 成功获取到CSRF令牌
        print("获取到CSRF令牌:", csrf_token)

        # 定义基础网址
        base_url = "https://eclass.tongnam.edu.mo/home/library_sys/admin/book/"

        # 定义按钮链接
        button_link = "book_item_edit.php?FromPage=item&UniqueID=71280"

        # 构建完整的请求网址
        url = base_url + button_link

        # 发送GET请求
        response = session.get(url)

        # 处理响应数据
        if response.status_code == 200:
            # 请求成功
            try:
                # 使用BeautifulSoup解析HTML
                soup = BeautifulSoup(response.text, 'html.parser')

                # 在这里处理返回的数据，例如提取所需信息
                # 示例：提取图书状态多选框选项列表
                select_element = soup.find('select', {'id': 'LocationCode'})

                if select_element:
                    options = select_element.find_all('option')

                    # 打印选项列表并为每个选项赋予序号
                    for index, option in enumerate(options):
                        value = option['value']
                        text = option.text.strip()

                        print(f"{index + 1}. 文本：{text}")

                    # 提示用户选择要更改为哪个选项
                    choice = int(input("请输入要更改为哪个选项的序号："))

                    # 获取用于提交表单的相关参数
                    submit_btn = soup.find('input', {'id': 'SubmitBtn'})
                    submit_name = submit_btn['name']
                    submit_value = submit_btn['value']

                    # 获取当前选中的选项文本
                    current_text = select_element.find('option', {'selected': True}).text.strip()
                    print("修改前的选项文本:", current_text)

                    # 构建提交表单数据，包括要更改的选项和其他必要参数
                    form_data = {
                        submit_name: submit_value,
                        'csrf_token': csrf_token,
                        'LocationCode': options[choice - 1]['value'],
                        'ItemID': '71280'
                    }

                    # 发送POST请求，点击提交按钮保存修改
                    response = session.post(url, data=form_data)

                    # 显示状态码
                    print("状态码:", response.status_code)

                    if response.status_code == 200:
                        print("修改已保存")

                        # 再次发送GET请求，获取修改后的页面并提取当前选中的选项文本
                        response = session.get(url)
                        soup = BeautifulSoup(response.text, 'html.parser')
                        current_text = soup.find('select', {'id': 'LocationCode'}).find('option', {'selected': True}).text.strip()
                        print("修改后的选项文本:", current_text)
                    else:
                        print("保存修改失败", response.status_code)

                else:
                    print("未找到<select>标签")
            except Exception as e:
                print("解析HTML发生异常", str(e))
        else:
            # 请求失败
            # 在这里处理错误信息，例如打印错误状态码
            print("请求失败", response.status_code)

    else:
        print("未获取到CSRF令牌")

else:
    # 登录失败，输出错误状态码
    print("登录失败", response.status_code)
