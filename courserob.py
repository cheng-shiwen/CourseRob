#! /usr/bin/env python
#coding=utf-8

import urllib2
import urllib
import cookielib
import re
import time
from pytesser import *

cookies = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
opener = urllib2.build_opener(cookies)
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.202 Safari/535.1')]
urllib2.install_opener(opener)

# account info, academic year and semester
username = ''
password = ''
xnxq = ''       # e.g. '2013-2014-2'

def login():
    pic_url = 'http://zhjwxk.cic.tsinghua.edu.cn/login-jcaptcah.jpg?captchaflag=login1'
    post_url = 'https://zhjwxk.cic.tsinghua.edu.cn/j_acegi_formlogin_xsxk.do'
    login_success = re.compile('hitTree')

    while True:
        pic_verify = urllib2.urlopen(pic_url).read();
        pic_out = open('verify.jpg', 'wb')
        pic_out.write(pic_verify)
        pic_out.close()

        verify_image = Image.open('verify.jpg')
        login_code = image_to_string(verify_image)
        login_code = login_code[0:-2]
        login_code = login_code.replace(' ', '')
        login_code = login_code.replace(']', 'J')
        print login_code, len(login_code)

        body = (('j_username', username), ('j_password', password), ('captchaflag', 'login1'), ('_login_image_', login_code))
        req = urllib2.Request(post_url, urllib.urlencode(body))
        login_html = urllib2.urlopen(req).read()

        # f_out = open('login.html', 'w')
        # f_out.write(login_html)
        # f_out.close()

        if login_success.search(login_html):
            break

def course_rob(course_type, course_number, serial_number):
    if course_type not in ['bx', 'xx', 'rx', 'xwk']:
        raise Exception('course_type error')

    base_url = 'http://zhjwxk.cic.tsinghua.edu.cn/xkBks.vxkBksXkbBs.do' if course_type in ['bx', 'xx', 'rx'] else \
               'http://zhjwxk.cic.tsinghua.edu.cn/xkYjs.vxkYjsXkbBs.do'

    course_url = base_url + '?m=' + course_type + 'Search&p_xnxq=' + xnxq + '&tokenPriFlag=' + course_type
    course_html = urllib2.urlopen(course_url).read()
    # f_out = open(course_type + '_course.html', 'w')
    # f_out.write(course_html)
    # f_out.close()

    token_regex = re.compile('<input type="hidden" name="token" value="(.*?)">')
    token_match = token_regex.search(course_html)
    token_string = token_match.group(1)
    print course_type, course_number, serial_number, token_string

    course_body = {
        'bx': (('m', 'saveBxKc'), ('token', token_string), ('p_xnxq', xnxq), ('tokenPriFlag', 'bx'), ('p_bxk_id', '%s;%s;%s;' % (xnxq, course_number, serial_number))),
        'xx': (('m', 'saveXxKc'), ('token', token_string), ('p_xnxq', xnxq), ('tokenPriFlag', 'xx'), ('p_xxk_id', '%s;%s;%s;' % (xnxq, course_number, serial_number))),
        'rx': (('m', 'saveRxKc'), ('token', token_string), ('p_xnxq', xnxq), ('tokenPriFlag', 'rx'), ('p_rx_id', '%s;%s;%s;' % (xnxq, course_number, serial_number)), ('p_sort.asc1', 'true'), ('p_sort.asc2', 'true')),
        'xwk': (('m', 'saveXwKc'), ('token', token_string), ('p_xnxq', xnxq), ('tokenPriFlag', 'xwk'), ('p_xwk_id', '%s;%s;%s;' % (xnxq, course_number, serial_number)))
    }
    course_req = urllib2.Request(base_url, urllib.urlencode(course_body[course_type]))
    course_req _html = urllib2.urlopen(course_req).read()
    # f_out = open(course_type + '_req.html', 'w')
    # f_out.write(course_req _html)
    # f_out.close()

while True:
    login()
    while True:
        try:
            # call function course_rob() to rob courses

            course_rob('rx', '00510392', '91')
            time.sleep(1)

        except:
            break
    # time.sleep(30)
