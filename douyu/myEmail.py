#！/usr/bin/env python3
# _*_ coding=utf-8 _*_

import smtplib
from email.mime.image import MIMEImage  # MIME二进制文件对象
from email.mime.multipart import MIMEMultipart  # 多个MIME对象的集合
from email.mime.text import MIMEText  # MIME文本对象
from email.header import Header
import email


class myEmail:
    def __init__(self):
        pass

    def send_email(self, html_msg):
        sender = "xxxxx"  # 发件人(string)
        sander_name = "xxxxx"  # 登录用户名
        sander_password = "xxxxx"  # 登录密码
        receivers = ["xxxx"]  # 收件人

        msgRoot = MIMEMultipart("related")  # 构造MIMEMultipart对象做为根容器,使用related类型
        msgRoot["From"] = Header("xxxxx")  # 设置根容器属性：发件人名称
        msgRoot["To"] = Header("myself", "utf-8")  # 设置根容器属性：收件人名称
        subject = "XXXXXX"  # 设置根容器属性：邮件主题
        msgRoot["Subject"] = Header(subject, 'utf-8')  # 设置根容器属性：邮件主题

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        # 邮件正文
        mail_msg = html_msg
        msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))

        # 添加附件
        # 构造MIMEBase对象做为文件附件内容并附加到根容器
        contype = 'application/octet-stream'
        maintype, subtype = contype.split('/', 1)

        # ## 读入文件内容并格式化
        # data = open('lijierui_work_log.csv', 'rb')
        # file_msg = email.mime.base.MIMEBase(maintype, subtype)
        # file_msg.set_payload(data.read())
        # data.close()
        # email.encoders.encode_base64(file_msg)
        #
        # ## 设置附件头
        # basename = os.path.basename('lijierui_work_log.csv')
        # file_msg.add_header('Content-Disposition',
        #                     'attachment', filename=basename)
        # msgAlternative.attach(file_msg)

        try:
            """
            smtplib.SMTP()：构造函数，功能是与smtp服务器建立连接， 
            连接成功后，就可以向服务器发送相关请求，比如登录，校验，发送，退出
            """
            smtpObj = smtplib.SMTP(host='smtp.qq.com', port=25)
            smtpObj.login(sander_name, sander_password)
            smtpObj.sendmail(sender, receivers, msgRoot.as_string())
            print("邮件发送成功···")
        except smtplib.SMTPException:
            print("Error: 无法发送邮件！！！")

