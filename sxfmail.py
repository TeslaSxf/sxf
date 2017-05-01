import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import poplib
import imaplib
from email.parser import Parser
from email import header

__all__ = ['SXFsmtp', 'SXFpop3', 'SXFimap', 'ParseContent']


class SXFsmtp:
    def __init__(self,
                 user_='sxf0207@163.com',
                 pass_='cjy001229',
                 host_='smtp.163.com'):
        self._user = user_
        self._pass = pass_
        self._host = host_

    def send(self, receivers, title, content, filename=None):
        try:
            msg = MIMEMultipart()
            msg['From'] = formataddr((self._user, self._user))
            msg['To'] = ','.join(formataddr((r, r)) for r in receivers)
            msg['Subject'] = title
            msg.attach(MIMEText(content, 'plain', 'utf-8'))

            if filename:
                with open(filename, 'rb') as f:
                    att = MIMEText(f.read(), 'plain', 'utf-8')
                    att['Content-Disposition'] = ('attachment; filename=' +
                                                  filename)
                    msg.attach(att)

            server = smtplib.SMTP_SSL(self._host)
            server.login(self._user, self._pass)
            server.sendmail(self._user, receivers, msg.as_string())
            server.quit()
            print('mail success')
        except Exception as e:
            print('mail failed ', e)


class ParseContent:
    def decode_str(self, s):
        ret = ''
        for t in header.decode_header(s):
            value, charset = t
            if charset:
                value = value.decode(charset)
            elif type(value) is bytes:
                value = value.decode()
            ret += value
        return ret

    def guess_charset(self, msg):
        charset = msg.get_charset()
        if charset is None:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset

    def show_msg(self, content):
        msg = Parser().parsestr(content)
        print('Date: {}'.format(self.decode_str(msg['Date'])))
        print('From: {}'.format(self.decode_str(msg['From'])))
        print('To: {}'.format(self.decode_str(msg['To'])))
        if msg['Cc']:
            print('Cc: {}'.format(self.decode_str(msg['Cc'])))
        print('Subject: {}'.format(self.decode_str(msg['Subject'])))
        part_cnt = 1
        for part in msg.walk():
            content_type = part.get_content_type()
            filename = part.get_filename()
            data = part.get_payload(decode=True)
            if filename:
                print('----part{}----'.format(part_cnt))
                with open(filename, 'wb') as f:
                    f.write(data)
                    print('file: {} has saved'.format(filename))
                part_cnt += 1
            elif content_type in ('text/plain', 'text/html'):
                print('----part{}----'.format(part_cnt))
                print(data.decode(self.guess_charset(part)))
                part_cnt += 1


class SXFpop3(ParseContent):
    def __init__(self,
                 user_='sxf0207@163.com',
                 pass_='cjy001229',
                 host_='pop.163.com'):
        self._user = user_
        self._pass = pass_
        self._host = host_

    # get one mail, default the last mail
    def receive(self, index=1):
        server = poplib.POP3_SSL(self._host)
        server.user(self._user)
        server.pass_(self._pass)
        cnt, size = server.stat()
        if index:
            index = abs(index) - 1
        resp, lines, octets = server.retr(cnt - index)
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        self.show_msg(msg_content)
        server.quit()


class SXFimap(ParseContent):
    def __init__(self,
                 user_='sxf0207@163.com',
                 pass_='cjy001229',
                 host_='imap.163.com'):
        self._user = user_
        self._pass = pass_
        self._host = host_

    # get one mail, default the last mail
    def reveive(self, index=1):
        conn = imaplib.IMAP4_SSL(self._host)
        conn.login(self._user, self._pass)
        conn.select()
        typ, dat = conn.search(None, 'ALL')
        if index > 0:
            index = -index
        elif index == 0:
            index = -1
        msg_st = dat[0].split()[index]
        typ, dat = conn.fetch(msg_st, '(RFC822)')
        self.show_msg(dat[0][1].decode('utf-8'))
        conn.close()
        conn.logout()
