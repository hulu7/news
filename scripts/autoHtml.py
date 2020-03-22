# coding:utf-8

import webbrowser

# 命名生成的html
GEN_HTML = "test.html"
# 打开文件，准备写入
f = open(GEN_HTML, 'w')

# 准备相关变量
str1 = 'my name is :'
str2 = '--MichaelAn--'

# 写入HTML界面中
message = """
<html>
<head></head>
<body>
<p>%s</p>
<p>%s</p>
</body>
</html>
""" % (str1, str2)

# 写入文件
f.write(message)
# 关闭文件
f.close()

# 运行完自动在网页中显示
webbrowser.open(GEN_HTML, new=1)