#coding: utf-8
import qrcode
from flask import Flask, render_template_string, redirect, url_for
def qrcode_show():
    # 创建一个二维码对象
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # 添加数据
    qr.add_data('https://www.hlcode.cn/img')
    # qr.add_data('https://yiyan.baidu.com/chat/')
    qr.make(fit=True)

    # 创建一个PIL图像并保存
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("static\scan_qr.png")
qrcode_show()