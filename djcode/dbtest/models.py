__author__ = 'skar'

from IMS.models import *

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
