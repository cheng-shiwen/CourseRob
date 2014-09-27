# -*- coding: utf-8 -*-

# Account info, academic year and semester
USERNAME    = ''
PASSWORD    = ''
STUDENTID   = ''
XNXQ        = ''       # e.g. '2013-2014-2'

# Courses to rob
# courses list: (course_type, course_number, serial_number) or
# (new_course_type, new_course_number, new_serial_number, old_course_type, old_course_number, old_serial_number)
# if new course and old course have a conflict
COURSES = [
    ('xx', '60240013', '0'),
    ('rx', '00510392', '91'),
    ('bx', '70240183', '2', 'bx', '70240183', '7')
]

# Interval to rob (seconds)
INTERVAL = 1
