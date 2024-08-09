from flask import Flask, render_template_string, redirect, url_for
import qrcode
from qrcode_file import qrcode_show
from PIL import Image

app = Flask(__name__)


# 假设这是扫描二维码后要显示的页面
@app.route('/scanned/')
def scanned():
    # 这里可以渲染一个模板或返回简单的文本
    return '这是扫描二维码后显示的页面！'


# HTML模板，包含二维码图片（这里假设二维码已经生成并保存为static/scan_qr.png）
html_template = '''  
<!doctype html>  
<html>  
<head>  
    <title>二维码扫描页面</title>  
</head>  
<body>  
    <h1>请扫描以下二维码以访问特定页面：</h1>  
    <img src="{{ url_for('static', filename='scan_qr.png') }}" alt="Scan this QR code">  
</body>  
</html>  
'''


@app.route('/')
def index():
    # 返回一个包含二维码图片的HTML页面
    return render_template_string(html_template)


if __name__ == '__main__':
    # 注意：这里我们没有在main中调用generate_qr_code，因为它应该在应用部署时完成
    qrcode_show()
    app.run(host='0.0.0.0', port=4000)

# 注意：上面的generate_qr_code调用被注释掉了，因为在实际应用中，
# 您可能希望在应用部署到服务器之前或作为构建过程的一部分来生成二维码。
# 此外，由于url_for在生成二维码时需要一个请求上下文，因此在实际应用中，
# 您可能需要将URL硬编码为字符串，或者在生成二维码时使用一个不同的方法来获取URL。