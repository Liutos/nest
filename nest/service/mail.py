# -*- coding: utf8 -*-
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from nest.app.use_case.registration import IMailService


class SinaMailService(IMailService):
    """使用新浪邮箱的SMTP服务器发送激活码邮件。"""
    def __init__(self, *, password: str, user: str):
        self.password = password
        self.user = user

    def send_activate_code(self, *, activate_code: str, email: str):
        user = self.user
        pwd = self.password
        to = [email]
        msg = MIMEMultipart()
        msg['From'] = Header(user)
        msg['Subject'] = Header('Nest 激活码', 'utf-8')
        msg.attach(MIMEText('您的 Nest 激活码是：\n{}'.format(activate_code), 'plain', 'utf-8'))

        server = smtplib.SMTP('smtp.sina.com')
        server.set_debuglevel(1)
        server.starttls()
        server.login(user, pwd)
        server.sendmail(user, to, msg.as_string())
        server.quit()
