# -*- coding: UTF-8 -*-
from email.parser import Parser
from email.header import decode_header, Header
from email.mime.text import MIMEText
from email import encoders
from email.utils import parseaddr, formataddr
from pyeoskit import eosapi
from pyeoskit import db
from pyeoskit import wallet

import poplib
import time
import smtplib
import pymysql
import os
import logging
import traceback

os.chdir('/home/uuos2/pyeos/build/programs/data-dir')
def Checkemail(email):
    emailid = email
    sql = 'SELECT emailID FROM Email.email_info;'
    cursor.execute(sql)
    emailinfo_id = cursor.fetchall()
    for einfo in emailinfo_id:#T IS EMAIL ALREADY REGIDTERED, F IS EMAIL FIRST REG...
        if ''.join(einfo) == emailid:
            #print(''.join(einfo))
            return False
        else:
            return True

def SetLog(s):
    s = s
    logging.basicConfig(level=logging.DEBUG,filename='emaillog.log',filemode='a',format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    logger = logging.error(s)
    return logger

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def CreateFail(email, s):
    to_addr = email
    toemailID = '1148017729@qq.com'
    password = 'mlsysdzdxtbrhcbi'
    smtp_server = 'smtp.qq.com'
    server = smtplib.SMTP(smtp_server, 587)
    server.set_debuglevel(0)
    server.starttls()
    server.login(toemailID, password)
    if s:  # S=1 email already registered
        msg = MIMEText('Sorry,your email has already registered,please check it.', 'plain', 'utf-8')
        msg['Subject'] = Header('Your email has already been registered.', 'utf-8').encode()
        msg['From'] = _format_addr('UUOS <%s>') % emailID
        msg['To'] = _format_addr('member <%s>') % to_addr
        server.sendmail(toemailID, to_addr, msg.as_string())
    else:  # S=0 public key is wrong
        msg = MIMEText('Sorry,the public key is wrong, please check it or contact us.', 'plain', 'utf-8')
        msg['Subject'] = Header('The public key is wrong.', 'utf-8').encode()
        msg['From'] = _format_addr('UUOS <%s>') % emailID
        msg['To'] = _format_addr('member <%s>') % to_addr
        server.sendmail(toemailID, to_addr, msg.as_string())
    #server.quit()


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def GetEmail():
    email = '1148017729'
    password = 'mlsysdzdxtbrhcbi'
    pop3_server = 'pop.qq.com'
    server = poplib.POP3_SSL(pop3_server)
    server.set_debuglevel(0)
    server.user(email)
    server.pass_(password)
    resp, mails, octes = server.list()
    index = len(mails)
    resp, lines, octes = server.retr(index)
    msg_content = b'\r\n'.join(lines).decode('utf-8')
    msg = Parser().parsestr(msg_content)
    hdr = msg.get('From')
    emailID = ''.join(hdr).split('<')[1].split('>')[0]
    return emailID
    #server.quit()

def GetInfo():
    email = '1148017729'
    password = 'mlsysdzdxtbrhcbi'
    pop3_server = 'pop.qq.com'
    server = poplib.POP3_SSL(pop3_server)
    server.set_debuglevel(0)
    server.user(email)
    server.pass_(password)
    resp, mails, octes = server.list()
    index = len(mails)
    resp, lines, octes = server.retr(index)
    msg_content = b'\r\n'.join(lines).decode('utf-8')
    msg = Parser().parsestr(msg_content)
    value = decode_str(msg.get('Subject'))
    valuesplit = value.split('+')
    if len(valuesplit) == 3:
        key1 = valuesplit[0]
        key2 = valuesplit[1]
        usrID = valuesplit[2]
        return key1, key2, usrID
    else:
        return None
    #server.quit()


def SaveInfo(emailinfo,usrinfo):
    emailinfo = emailinfo
    usrinfo = usrinfo
    publickey1 = usrinfo[0]
    publickey2 = usrinfo[1]
    emailID = emailinfo
    usrna = usrinfo[2]
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sql = "INSERT INTO Email.email_info(emailID,userID,key1,key2) VALUES (%r,%r,%r,%r)" % (
    emailID, usrna, publickey1, publickey2)
    cursor.execute(sql)
    db.commit()


def CreateSuccess(list):
    to_addr = list
    fromemailID = '1148017729@qq.com'
    password = 'mlsysdzdxtbrhcbi'
    smtp_server = 'smtp.qq.com'
    server = smtplib.SMTP(smtp_server, 587)
    server.set_debuglevel(0)
    server.starttls()
    server.login(fromemailID, password)
    msg = MIMEText('Congratulation! Create account success!', 'plain', 'utf-8')
    msg['Subject'] = Header('Congratulation! Create account success!', 'utf-8').encode()
    msg['From'] = _format_addr('UUOS <%s>') % fromemailID
    msg['To'] = _format_addr('member <%s>') % to_addr
    server.sendmail(fromemailID, [to_addr], msg.as_string())
    #server.quit()

def CleanSql(email):
    erroremail = email
    sql = 'DELETE FROM Email.email_info WHERE emailID = %r' % erroremail
    cursor.execute(sql)

if __name__ == "__main__":
    db = pymysql.connect("localhost", "root", "morning321", "Email")
    cursor = db.cursor()
    getinfo = GetInfo()
    emailID = GetEmail()
    checkemail = Checkemail(emailID)
    nodes = ['192.168.0.171:8888']
    eosapi.set_nodes(nodes)
    #print(eosapi.get_account('edson'))
    wallet.open('mywallet')
    wallet.unlock('mywallet','PW5K7NsAw2vatUubc4A2789fRZw8CpF65zdomnatpsJFvRYpAutdp')
    #wallet.import_key('mywallet','5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3')
    if checkemail:
        try:
            create = eosapi.create_account('eosio', getinfo[2], getinfo[0], getinfo[1])
            getaccount = eosapi.get_account(getinfo[2])
            print(create)
            while getaccount:
                CreateSuccess()
        except Exception:
            CreateFail(emailID,0)
            SetLog(traceback.format_exc())
        finally:
            CleanSql(emailID)

    else:
        CreateFail(emailID, 1)
    db.commit()
    db.close()

    





