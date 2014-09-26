#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
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
studentid = ''
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

def get_base_url(course_type):
    if course_type not in ['bx', 'xx', 'rx', 'xwk']:
        raise Exception('course_type error')
    return 'http://zhjwxk.cic.tsinghua.edu.cn/xkBks.vxkBksXkbBs.do' if course_type in ['bx', 'xx', 'rx'] else \
           'http://zhjwxk.cic.tsinghua.edu.cn/xkYjs.vxkYjsXkbBs.do'

def is_rob_success(base_url, course_number, serial_number):
    yx_url = base_url + '?m=yxSearchTab&p_xnxq=' + xnxq + '&tokenPriFlag=yx'
    yx_html = urllib2.urlopen(yx_url).read()
    # f_out = open('yx_course.html', 'w')
    # f_out.write(yx_html)
    # f_out.close()

    success_regex = re.compile('<span>' + course_number + '</span>[\s\S]*?<span >' + serial_number + '</span>')
    success_match = success_regex.search(yx_html)
    return True if success_match else False

def del_course(course_type, course_number, serial_number):
    base_url = get_base_url(course_type)

    yx_url = base_url + '?m=yxSearchTab&p_xnxq=' + xnxq + '&tokenPriFlag=yx'
    yx_html = urllib2.urlopen(yx_url).read()
    # f_out = open('yx_course.html', 'w')
    # f_out.write(yx_html)
    # f_out.close()

    token_regex = re.compile('<input\s+?type="hidden"\s+?name="token"\s+?value="(.*?)">')
    token_match = token_regex.search(yx_html)
    token_string = token_match.group(1)
    print course_type, course_number, serial_number, token_string

    body = (('m', 'deleteYxk'), ('token', token_string), ('p_xnxq', xnxq), ('tokenPriFlag', 'yx'), ('p_del_id', '%s;%s;%s;%s' % (xnxq, course_number, serial_number, studentid)))
    course_req = urllib2.Request(base_url, urllib.urlencode(body))
    course_req_html = urllib2.urlopen(course_req).read()
    # f_out = open(course_type + '_req.html', 'w')
    # f_out.write(course_req _html)
    # f_out.close()

def rob_course(*course_info):
    if len(course_info) == 3:
        course_type = course_info[0]
        course_number = course_info[1]
        serial_number = course_info[2]
        swap = False
    elif len(course_info) == 6:
        course_type = course_info[0]
        course_number = course_info[1]
        serial_number = course_info[2]
        old_course_type = course_info[3]
        old_course_number = course_info[4]
        old_serial_number = course_info[5]
        swap = True
    else:
        raise Exception('course_info error')

    base_url = get_base_url(course_type)

    course_url = base_url + '?m=' + course_type + 'Search&p_xnxq=' + xnxq + '&tokenPriFlag=' + course_type
    course_html = urllib2.urlopen(course_url).read()
    # f_out = open(course_type + '_course.html', 'w')
    # f_out.write(course_html)
    # f_out.close()

    remain_regex = re.compile('>\s*?' + course_number + '</td>\s*?.*?>' + serial_number + '</td>[\s\S]*?</td>\s*?.*?>(\d+)</td>')
    remain_match = remain_regex.search(course_html)
    remain_num = int(remain_match.group(1))
    print 'course remain: ', course_type, course_number, serial_number, remain_num

    if remain_num:
        if swap:
            del_course(old_course_type, old_course_number, old_serial_number)

        token_regex = re.compile('<input\s+?type="hidden"\s+?name="token"\s+?value="(.*?)">')
        token_match = token_regex.search(course_html)
        token_string = token_match.group(1)
        print 'course token: ', course_type, course_number, serial_number, token_string

        course_body = {
            'bx': (('m', 'saveBxKc'), ('token', token_string), ('p_xnxq', xnxq), ('tokenPriFlag', 'bx'), ('p_bxk_id', '%s;%s;%s;' % (xnxq, course_number, serial_number))),
            'xx': (('m', 'saveXxKc'), ('token', token_string), ('p_xnxq', xnxq), ('tokenPriFlag', 'xx'), ('p_xxk_id', '%s;%s;%s;' % (xnxq, course_number, serial_number))),
            'rx': (('m', 'saveRxKc'), ('token', token_string), ('p_xnxq', xnxq), ('tokenPriFlag', 'rx'), ('p_rx_id', '%s;%s;%s;' % (xnxq, course_number, serial_number)), ('p_sort.asc1', 'true'), ('p_sort.asc2', 'true')),
            'xwk': (('m', 'saveXwKc'), ('token', token_string), ('p_xnxq', xnxq), ('tokenPriFlag', 'xwk'), ('p_xwk_id', '%s;%s;%s;' % (xnxq, course_number, serial_number)))
        }
        course_req = urllib2.Request(base_url, urllib.urlencode(course_body[course_type]))
        course_req_html = urllib2.urlopen(course_req).read()
        # f_out = open(course_type + '_req.html', 'w')
        # f_out.write(course_req _html)
        # f_out.close()

        return is_rob_success(base_url, course_number, serial_number)

    return False

def rob_courses(courses, interval=1):
    result = [False for course in courses]

    while True:
        login()
        while True:
            try:
                if result.count(False) == 0:
                    return

                for idx, course in enumerate(courses):
                    if not result[idx]:
                        result[idx] = rob_course(*course)
                        time.sleep(interval)
            except:
                break
        time.sleep(interval * len(courses))


if __name__ == '__main__':
    # courses list: (course_type, course_number, serial_number) or
    # (new_course_type, new_course_number, new_serial_number, old_course_type, old_course_number, old_serial_number)
    courses = [
        ('xx', '60240013', '0'),
        ('rx', '00510392', '91'),
        ('bx', '70240183', '2', 'bx', '70240183', '7')
    ]
    interval = 1
    rob_courses(courses, interval)
