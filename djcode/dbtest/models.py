__author__ = 'skar'

from django.db import models


class Student_user(models.Model):
    """
    | id | contact | name | gender | college | major | grade | gpa | credits |
    |---|---|---|---|---|---|---|---|---|
    | CHARACTER(10) | VARCHAR(11) | VARCHAR(20) | BOOLEAN | VARCHAR(50) | VARCHAR(50) | INTEGER | FLOAT | FLOAT |
    """
    id = models.CharField(max_length=10, primary_key=True)
    contact = models.CharField(max_length=11)
    name = models.CharField(max_length=20)
    gender = models.BooleanField()
    college = models.CharField(max_length=50)
    major = models.CharField(max_length=50)
    grade = models.IntegerField()
    gpa = models.FloatField()
    credits = models.FloatField()


class Faculty_user(models.Model):
    """
    | id | contact | name | gender | college | major | degree | title |
    |---|---|---|---|---|---|---|---|
    | CHARACTER(6) | VARCHAR(11) | VARCHAR(20) | BOOLEAN | VARCHAR(50) | VARCHAR(50) | VARCHAR(20) | VARCHAR(20) |
    """
    id = models.CharField(max_length=6, primary_key=True)
    contact = models.CharField(max_length=11)
    name = models.CharField(max_length=20)
    gender = models.BooleanField()
    college = models.CharField(max_length=50)
    major = models.CharField(max_length=50)
    degree = models.CharField(max_length=20)
    title = models.CharField(max_length=20)


# class Admin_user: disabled temporarily


class Course_info(models.Model):
    """
    | course_id | name | credits | semester | textbook | college |
    |---|---|---|---|---|---|
    | CHARACTER(8) | VARCHAR(110) | FLOAT | INTEGER | VARCHAR(110) | VARCHAR(50) |
    """
    course_id = models.CharField(max_length=8, primary_key=True)
    chief_faculty = models.ForeignKey(Faculty_user)
    name = models.CharField(max_length=110)
    credits = models.FloatField()
    semester = models.IntegerField()
    textbook = models.CharField(max_length=110)
    college = models.CharField(max_length=50)


class Class_info(models.Model):
    """
    | class_id | course_id | teacher | time | room | examdate | examtime | examroom | capacity | semester
    |---|---|---|---|---|---|---|---|---|
    | CHARACTER(10) | CHARACTER(8) | VARCHAR(20) | INTEGER | VARCHAR(20) | DATETIME(TEXT) | INTEGER | VARCHAR(20) | INTEGER | INTEGER
    """
    class_id = models.CharField(max_length=10)
    course_id = models.ForeignKey(Course_info)
    teacher = models.CharField(max_length=20)
    time = models.IntegerField()
    room = models.CharField(max_length=20)
    examdate = models.CharField(max_length=20)
    examtime = models.IntegerField()
    examroom = models.CharField(max_length=20)
    capacity = models.IntegerField()
    semester = models.IntegerField()


class class_table(models.Model):
    """
    | student_id | class_id |
    |---|---|
    | CHARACTER(10) | CHARACTER(10) |
    """
    student_id = models.ForeignKey(Student_user)
    class_id = models.ForeignKey(Class_info)


class TempTable(models.Model):
    # faculty_id = models.ForeignKey(Faculty_user)
    student_id = models.ForeignKey(Student_user)
    class_id = models.ForeignKey(Class_info)
    """ the above three should be modified to ForeignKey
        not sure if class_id is a primary of class_info
         in IMS
    """
    score = models.FloatField()

    class Meta:
        ordering = ["class_id"]

    def __str__(self):
        return 'score of student %s in class %s' \
               % (self.student_id, self.class_id)


class MessageTable(models.Model):
    message_id = models.CharField(max_length=50)
    from_faculty_id = models.ForeignKey(Faculty_user, related_name='%(class)s_from')
    to_faculty_id = models.ForeignKey(Faculty_user, related_name='%(class)s_to')
    student_id = models.ForeignKey(Student_user)
    class_id = models.ForeignKey(Class_info)
    old_score = models.FloatField()
    new_score = models.FloatField()
    reason = models.CharField(max_length=200)
    status = models.IntegerField(default=0)

    class Meta:
        ordering = ["message_id"]

    def __str__(self):
        return 'message on student %s, from faculty %s to %s' \
               % (self.student_id, self.from_faculty_id, self.to_faculty_id)


class ScoreTable(models.Model):
    class_id = models.ForeignKey(Class_info)
    student_id = models.ForeignKey(Student_user)

    score = models.FloatField()

    class Meta:
        ordering = ["class_id"]

    def __str__(self):
        return 'score of student %s in class %s' \
               % (self.student_id, self.class_id)


class User(models.Model):
    xlsx_file = models.FileField(upload_to='./upload/')

#This class should be get from group of "Choose course"
class Scheme_info(models.Model):
    """
    | class_id | course_id | state |
    |---|---|---|
    | CHARACTER(10) | CHARACTER(8) |  {-2,-1,0,1,2} |
    """
    student_id = models.ForeignKey(Student_user)
    course_id = models.ForeignKey(Course_info,related_name='scheme_course')
    state = models.IntegerField(default=0)
    class Meta:
        ordering = ["student_id"]
    def __str__(self):
        return (self.id)
