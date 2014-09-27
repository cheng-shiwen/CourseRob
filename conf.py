# -*- coding: utf-8 -*-

# Account info, academic year and semester
USERNAME    = ''
PASSWORD    = ''
STUDENTID   = ''
XNXQ        = ''       # e.g. '2013-2014-2'

# Courses to rob
# courses list:
#   (course_type, course_number, serial_number) or
#   (new_course_type, new_course_number, new_serial_number, old_course_type, old_course_number, old_serial_number)
#   if new course and old course have a conflict
# course_type:
#   'bx', 'xx', 'rx', 'xwk'
COURSES = [
    ('bx', '60240013', '0'),
    ('xx', '00510392', '2', 'xx', '00510392', '7'),
    ('rx', '70240183', '0'),
    ('xwk', '60640012', '5')
]

# Interval to rob (seconds)
INTERVAL = 1
