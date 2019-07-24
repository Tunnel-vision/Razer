from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import parseaddr, formataddr
import smtplib
from email.mime.application import MIMEApplication
from datetime import datetime


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_email(num, excelpath):
    # Email地址和口令:
    from_addr = '290868461@qq.com'
    password = 'iusxtvyveqggcabh'
    # 收件人地址:
    to_addr = ['lei.guo@pactera.com', 'fei.wang28@pactera.com']
    # SMTP服务器地址:
    smtp_server = 'smtp.qq.com'

    msg = MIMEMultipart()
    msg['From'] = _format_addr('Pactera <%s>' % from_addr)
    msg['To'] = _format_addr('Razer <%s>' % to_addr)
    dt = datetime.now()
    dtformat = datetime.strftime(dt, '[%d %b %Y] at %H:%M%p')
    subject = 'Razer Daily SW Customer Tickets monitoring All Keywords %s(UTF+08:00)' % dtformat
    msg['Subject'] = Header(subject, 'utf-8').encode()
    # 邮件正文[7 Nov 2018] at 6:00PM
    html = '<html><body><h2>Hi All,</h2>' \
           '' \
           '<h3>In total, there are %d issues reported as of %s for ALL KEYWORDS.</h3></body></html>' % (num, dtformat)
    msg.attach(MIMEText(html, 'html', 'utf-8'))

    # 添加图片附件
    # with open('/Users/alex/Desktop/Result.xlsx', 'rb') as f:
    #     mime = MIMEBase('image', 'png', filename='screen.png')
    #     # 加上必要的头信息
    #     mime.add_header('Content-Disposition', 'attachment', filename='screen.png')
    #     mime.add_header('Content-ID', '<0>')
    #     mime.add_header('X-Attachment-Id', '0')
    #     # 把附件内容读进来
    #     mime.set_payload(f.read())
    #     # 用Base64编码
    #     encoders.encode_base64(mime)
    #     # 添加到MIMEMultipart
    #     msg.attach(mime)

    # 添加Excel附件
    part = MIMEApplication(open(excelpath, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename='All Keywords-Razer SW Customer Tickets monitoring.xlsx')
    msg.attach(part)

    server = smtplib.SMTP(smtp_server, 25)  # SMTP协议默认端口是25
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()

# if __name__ == '__main__':
#     send_email()
