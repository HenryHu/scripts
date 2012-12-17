#!/usr/local/bin/python
# vim: set fileencoding=utf8 :

# Copyright (c) 2009, Henry Hu
# All rights reserved.

# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#     * Neither the name of the software nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import urllib2
import urllib
import cookielib
import lxml.html
import subprocess
import getpass
import time
import random
from lxml import etree

ocrcmd_pre = "";
loginfrm = "http://portal.pku.edu.cn:80/infoPortal/login.do";
hosturl = "http://elective.pku.edu.cn";
ocrcmd_res = "./pointrmv captcha.jpg";
loginhost = "http://portal.pku.edu.cn";
urllogin = "http://portal.pku.edu.cn/infoPortal/";
imgurl = loginhost + "/infoPortal/DrawServlet?Rand=9613.807267094351";
course_url = loginhost + "/infoPortal/portlets/schoolwork/choosecourse/uniChooseCourse.jsp"
course_login = hosturl + "/elective2008/LoginServlet?addr=162.105.131.23&maskAddr=0113917136086270f671568b194e3eee"
val_url = hosturl + "/elective2008/edu/pku/stu/elective/controller/supplement/validate.do?validCode="
sel_url = hosturl + "/elective2008/edu/pku/stu/elective/controller/supplement/electSupplement.do?index=" + courseminor + "&seq=" + coursemajor
sel2_url = hosturl + "/elective2008/edu/pku/stu/elective/controller/supplement/SupplementController.jpf"
course_img = hosturl + "/elective2008/DrawServlet?Rand=5463.484995765994"

jar = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(jar)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)

h=urllib2.HTTPHandler(debuglevel=1)
opener = urllib2.build_opener(h) 


while True:


	data = urllib2.urlopen(urllogin).read()

# print data;

#	img = lxml.html.fromstring(data).get_element_by_id("loginForm")[0];

#	simple validation code
	captcha = urllib2.urlopen(imgurl).read();

	imgfile = open("captcha.jpg", "w");
	imgfile.write(captcha);
	imgfile.close();

	subprocess.Popen(args=ocrcmd_pre, shell=True).wait();
	ocrproc = subprocess.Popen(args=ocrcmd_res, stdout=subprocess.PIPE, shell=True);
	ocrret = ocrproc.stdout.read();
	print ocrret

	loginfrm_arg = urllib.urlencode({'{actionForm.userid}': username,
		'{actionForm.password}': password,
		'{actionForm.validCode}': ocrret })
	loginres = ""
	try:
		loginres = urllib2.urlopen(loginfrm, loginfrm_arg).read();
	except:
		loginres = ""

	if loginres.find("IAAA") != -1 :
		break;

print "Logged in!"

pageone = urllib2.urlopen(course_url).read()
# print pageone

course_login_args = urllib.urlencode({'userid' : username,
		'passwd' : password2,
		'encrypted' : 1})
pagetwo = urllib2.urlopen(course_login, course_login_args).read()
# print pagetwo

# selurl = hosturl + "/" + mainpage.forms[0].action

while True:
	pagethree = urllib2.urlopen(sel2_url).read()
#	print pagethree
	while True:
		captcha = urllib2.urlopen(course_img).read()
		imgfile = open("captcha.jpg", "w");
		imgfile.write(captcha);
		imgfile.close();
		subprocess.Popen(args=ocrcmd_pre, shell=True).wait();
		ocrproc = subprocess.Popen(args=ocrcmd_res, stdout=subprocess.PIPE, shell=True);
		ocrret = ocrproc.stdout.read();
		print ocrret
		val_res = urllib2.urlopen(val_url + ocrret).read()
#		print val_res
		if val_res.find("<valid>2</valid>") != -1 :
			break;

	selres = urllib2.urlopen(sel_url).read()
	selfile = open("result.html", "w");
	selfile.write(selres)
	selfile.close()
	subprocess.Popen(args="cat result.html | grep message", shell=True).wait()
#	print selres
	if selres.find("message_error") == -1 :
		break;

	if selres.find("message_success") != -1 :
		break;

	time.sleep(10+0.01*random.randint(0, 500));

print "FINISHED!"

