# Author: Vincent.chan
# Blog: http://blog.alys114.com

import os

##获取当前根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 数据库相关
db_path = BASE_DIR+os.sep+"db"+os.sep
teacher_db = db_path + "teacher.pkl"
course_db =  db_path + "course.pkl"
classes_db =  db_path + "classes.pkl"
student_db = db_path + "student.pkl"
score_db = db_path + "score.pkl"
school_db = db_path + "school.pkl"
student_classes_db = db_path + "student_classes.pkl"
classes_record_db = db_path + "classes_record.pkl"
student_record_db = db_path + "student_record.pkl"

#
info_width = 40
menu_width = 20
center_width = 90