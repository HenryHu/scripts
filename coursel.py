#!/usr/local/bin/python
# vim: set fileencoding=utf8 :
import urllib2
import urllib
import cookielib
import lxml.html
import subprocess
import getpass
import time
import random
from lxml import etree

hosturl = "http://zhjwxk.cic.tsinghua.edu.cn";
username = "";
password = getpass.getpass("Password: ");
loginfrm = "https://zhjwxk.cic.tsinghua.edu.cn:443/j_acegi_formlogin_xsxk.do";
ocrcmd_pre = "convert captcha.jpg captcha.bmp ; cuneiform captcha.bmp > /dev/null";
#gocr -a 80 -s 100 -C \"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ\"";
ocrcmd_res = "cat cuneiform-out.txt";
urllogin = hosturl + "/xsxk_index.jsp";

jar = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(jar)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)

h=urllib2.HTTPHandler(debuglevel=1)
opener = urllib2.build_opener(h) 

coursemajor = "30240422"
courseminor = "0"
term = "2010-2011-1"
coursetype = "xx" # rx
searchtype = "xxSearch" # rxSearch
type_id = "p_xxk_id" # p_rx_id
savetype = "saveXxKc" # saveRxKc

arg2 = "?m=" + searchtype + "&p_xnxq=" + term + "&tokenPriFlag=" + coursetype + "&p_kch=" + coursemajor

success = False
trytime = 0

while not success:
    while True:
        data = urllib2.urlopen(urllogin).read()
        # print data;
        img = lxml.html.fromstring(data).get_element_by_id("captcha");
        captcha = urllib2.urlopen(hosturl + img.get("src")).read();
        imgfile = open("captcha.jpg", "w");
        imgfile.write(captcha);
        imgfile.close();
        subprocess.Popen(args=ocrcmd_pre, shell=True).wait();
        ocrproc = subprocess.Popen(args=ocrcmd_res, stdout=subprocess.PIPE, shell=True);
        ocrret = ocrproc.stdout.read().replace(" ","").replace("\n","").replace("/","J").replace("1","J").replace("I","J").replace("S","8");
        loginfrm_arg = urllib.urlencode({'j_username': username,
                                         'j_password': password,
                                         'captchaflag': "login1",
                                         '_login_image_': ocrret})
        loginres = ""
        try:
            loginres = urllib2.urlopen(loginfrm, loginfrm_arg).read();
        except:
            loginres = ""
        if loginres.find("<div align=\"center\"") == -1 :
            break
    print "Logged in!"
#    print urllib2.urlopen(hosturl + "/xkBks.vxkBksXkbBs.do?m=rxSearch&p_xnxq=2010-2011-1&tokenPriFlag=rx&p_kch=00430093").read()
    mainpage = lxml.html.fromstring(urllib2.urlopen(hosturl + "/xkBks.vxkBksXkbBs.do" + arg2).read())
    selurl = hosturl + "/" + mainpage.forms[0].action
    while True:
        trytime = trytime + 1
        print "Round ", trytime
        seldict = {}
        try:
            for input in mainpage.forms[0].inputs:
                if input.name != None and input.value != None:
                    if input.name != 'submit1' and input.name != 'bt':
                        print input.name.encode("utf-8"),":", input.value.encode("utf-8")
                if input.name == 'm':
                    input.value = savetype
                if (input.name == None):
                    continue
                if (input.value == None and input.name != 'j_captcha_bks_xk'):
                    seldict[input.name] = ''
                    continue
                if (input.type != 'button') & (input.type != 'reset') :
                    seldict[input.name] = input.value
                if input.name == 'j_captcha_bks_xk':
                    img = mainpage.get_element_by_id("captcha");
                    captcha = urllib2.urlopen(hosturl + img.get("src")).read();
                    imgfile = open("captcha.jpg", "w");
                    imgfile.write(captcha);
                    imgfile.close();
                    subprocess.Popen(args=ocrcmd_pre, shell=True).wait();
                    ocrproc = subprocess.Popen(args=ocrcmd_res, stdout=subprocess.PIPE, shell=True);
                    ocrret = ocrproc.stdout.read().replace(" ","").replace("\n","").replace("/","J").replace("1","J").replace("I","J").replace("S","8");
                    seldict[input.name] = ocrret
                    print "Img Capt: ",ocrret
        except:
            break
        seldict[type_id] = term + ";"+ coursemajor + ";" + courseminor + ";"
        selparam = urllib.urlencode(seldict)
        print selparam
        time.sleep(0.5+0.01*random.randint(0, 100))
        selres = urllib2.urlopen(selurl, selparam).read().decode('gbk')
        selpage = open("selpage" + str(trytime % 2) + ".htm", "w");
        selpage.write(selres.encode("utf-8"));
        selpage.close();
        if selres.encode("utf-8").find("成功") != -1:
            success = True;
            break
        if selres.encode("utf-8").find("Forbidden") != -1:
            timeout = True;
            break;
        mainpage = lxml.html.fromstring(selres)
        alertStart = selres.find('showMsg("') + 9;
        alertEnd = selres.find('");', alertStart);
        print "Result: ", selres[alertStart:alertEnd]
#        print selres.encode("utf-8")

print "FINISHED!"
