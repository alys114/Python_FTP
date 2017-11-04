# Author: Vincent.chan
# Blog: http://blog.alys114.com

import common
import model
from constConfig import *

# 学校记录
school1 = model.School('8001','北京前程似锦','西单xxxx')
school2 = model.School('8002','上海前程似锦','浦东xxxx')
data = {}
data[school1.schoolID] = school1
data[school2.schoolID] = school2
common.pickleDump(data,school_db)
# 课程记录
course1 = model.Course('1','Linux',6500.00,'8001')
course2 = model.Course('2','Python',5500.00,'8001')
course3 = model.Course('3','Go',4500.00,'8002')
data = {}
data[course1.courseID] = course1
data[course2.courseID] = course2
data[course3.courseID] = course3
common.pickleDump(data,course_db)
# 老师
teacher1 = model.Teacher('1','oldboy','oldboy',common.md5Encode('123456'),'8001')
teacher2 = model.Teacher('2','alex','alex',common.md5Encode('123456'),'8001')
teacher3 = model.Teacher('3','jack','jack',common.md5Encode('123456'),'8002')
data = {}
data[teacher1.id] = teacher1
data[teacher2.id] = teacher2
data[teacher3.id] = teacher3
common.pickleDump(data,teacher_db)
# 班级信息
classes1 = model.Classes('1','1','1','20周','2017-09-01','8001')
classes2 = model.Classes('2','2','2','20周','2017-09-27','8001')
classes3 = model.Classes('3','3','3','18周','2017-10-18','8002')
data = {}
data[classes1.classesID] = classes1
data[classes2.classesID] = classes2
data[classes3.classesID] = classes3
common.pickleDump(data,classes_db)
# 学生
stu = model.Student('1','test1','test1','e10adc3949ba59abbe56e057f20f883e','8001')
data  = {}
data[stu.id]=stu
common.pickleDump(data,student_db)

