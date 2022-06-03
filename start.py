import requests
from lxml import etree
import json


# 获取子网页中所需的内容, 传入具体命令的子网页 url、自定义的命令对象 command
def request_sub_url(url, command):
    # requests 获取子网页网页
    html = requests.get(url).text
    # etree 获取子网页 HTML 源代码
    etree_html = etree.HTML(html)

    # 获取所需内容 2: 命令的语法格式 (去除多余的冒号和空格)
    usage = etree_html.xpath("//p/strong[contains(text(), '语法格式')]//parent::node()/text()")[1].strip('：').strip()
    command["usage"] = usage

    # 获取所需内容 3: 命令的参数列表 (数组格式)
    params = etree_html.xpath("//article//table//td/text()")
    # 用于存储参数列表的数组
    command["params"] = []
    # 遍历 params
    # 从网页里获得数组中, 参数名称和参数描述成对出现
    # params[0] 中存储着一个参数名称, params[1] 中存储着对应的描述, 以此类推
    for index in range(int(len(params) / 2)):
        # 创建参数对象 param
        param = {
            "param": params[index * 2].strip(),
            "description": params[index * 2 + 1].strip()
        }
        command["params"].append(param)


# requests 获取网页
_html = requests.get("https://www.linuxcool.com/").text
# etree 获取网页 HTML 源代码
_etree_html = etree.HTML(_html)

# data 数组, 用于记录后续的所有数据, JSON 格式
_data = []

# 获取所需内容-1: 首页中跳转到对应命令子网页的 url 数组
_urls = _etree_html.xpath("""
  //div[
    @class='column col-half 1' or
    @class='column col-half 2' or
    @class='column col-half 3' or
    @class='column col-half 4' or
    @class='column col-half 5' or
    @class='column col-half 6' or
    @class='column col-half 7' or
    @class='column col-half 8' or
    @class='column col-half 9'
  ]/ul/li/a[1]/@href
""")
# 遍历 urls 数组
for _url in _urls:
    # 创建命令对象 command
    # command 的名称设置为 url 中最后一个 / 后面的值, 即命令的名称
    _command = {"command": _url.split("/")[-1]}
    # 将 command 加入到 data 数组中
    _data.append(_command)
    request_sub_url(_url, _command)

# 打印最终生成的 JSON 格式字符串到控制台预览
print(_data)

# 将数据转换成 JSON 格式
_data_json = json.dumps(_data, ensure_ascii=False)
# 写入到文件中
with open("data/data.json", "w", encoding="utf-8") as fp:
    fp.write(_data_json)
