#!/usr/bin/python3
#coding=utf-8
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import Header
from email.utils import parseaddr, formataddr
from email.mime.base import MIMEBase
from email import encoders
import smtplib,sys,os,time,re,requests
from smtplib import SMTP
import requests
import json



def get_itemid():
    itemid=re.search(r'ITEM.ID:(\d+)',sys.argv[3]).group(1)
    return itemid
def get_graph(itemid):
    session=requests.Session()
    user=configSwitchDict("/usr/lib/zabbix/alertscripts/login.conf")
    try:
        loginheaders={            
            "Host":user['host'],            
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,\*/\*;q=0.8"
        }
        payload = {            
             "name":user['user'],
             "password":user['password'],  
              "autologin":"1",            
             "enter":"Sign in",
        }
        session.post(url=user['loginurl'],headers=loginheaders,data=payload)
        graph_params={
            "from" :"now-20m",
            "to" : "now",           
            "itemids" : itemid,                       
            "width" : "600",
        }
        graph_req=session.get(url=user['graph_url'],params=graph_params)
        time_tag=time.strftime("%Y%m%d%H%M%S", time.localtime())
        graph_name='warning_'+time_tag+'.png'
        if os.path.exists(user['graph_path'])==0:
            os.makedirs(user['graph_path'])    
        with open(os.path.join(user['graph_path'], graph_name),'wb') as f:
            f.write(graph_req.content)
        return graph_name

    except Exception as e:        
        print (e)        
        return False


def configSwitchDict(filename):
    with open(filename, 'rb') as f:
        lines= f.readlines()
        tmp= {}
        for l in lines:
            x=l.decode("utf-8").split("=")           
            init = {x[0].strip():x[1].strip()}
            tmp.update(init)
    return tmp 
def text_to_html(text):
    d=text.splitlines()   
    html_text=''
    for i in d:
        i='' + i + '<br>'
        html_text+=i + '\n'
    return html_text

def send_mail(graph_name):
    smtpuser=configSwitchDict("/usr/lib/zabbix/alertscripts/mail.conf")
    smtpuser['to_addr']=sys.argv[1]
    smtpuser['subject']=sys.argv[2]
    msg = MIMEMultipart('related')
    with open("/usr/lib/zabbix/alertscripts/graph/"+graph_name,'rb') as f:
        graph=MIMEImage(f.read())  
    graph.add_header('Content-ID','imgid1')  
    text=text_to_html(sys.argv[3])
    html="""
    <html> 
      <body>
      %s  <br><img src="cid:imgid1">
      </body>
    </html>
    """ % text
    html=MIMEText(html,'html','utf8') 
    msg.attach(html)   
    msg.attach(graph) 
    msg['Subject'] = smtpuser['subject']
    msg['From'] = smtpuser['from_addr']
    try:
        server=smtplib.SMTP_SSL(smtpuser['smtp_server'],465)   
        server.login(smtpuser['from_addr'],smtpuser['password']) 
        server.sendmail(smtpuser['from_addr'],smtpuser['to_addr'].split(","),msg.as_string()) 
        server.quit()   
        print("mail send successful"+msg.as_string())
    except smtplib.SMTPException as a:
        print (a)



def run():
    itemid=get_itemid()
    print(itemid)
    graph_name=get_graph(itemid)
    print(graph_name)
    return graph_name

if __name__ =='__main__':
    os.popen("source /etc/profile")
    send_mail(run())
