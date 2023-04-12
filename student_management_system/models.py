from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
	user_type_data = (
		(1,"HOD"),
		(2,"Staff"),
		(3,"Student"))
	user_type 			= models.CharField(default=1,choices=user_type_data,max_length=10)

class AdminHot(models.Model):
	admin 				= models.OneToOneField(CustomUser,on_delete=models.CASCADE) 
	created_at	 		= models.DateTimeField(auto_now_add=True)
	updated_at 			= models.DateTimeField(auto_now_add=True)
	objects 			= models.Manager()

class Staffs(models.Model):
	admin 				= models.OneToOneField(CustomUser,on_delete=models.CASCADE) 
	address 			= models.TextField()
	created_at 			= models.DateTimeField(auto_now_add=True)
	updated_at 			= models.DateTimeField(auto_now_add=True)
	objects 			= models.Manager()

class Courses(models.Model):
	course_name 		= models.CharField(max_length=255)
	created_at 			= models.DateTimeField(auto_now_add=True)
	updated_at 			= models.DateTimeField(auto_now_add=True)
	objects 			= models.Manager()

class Subjects(models.Model):
	subject_name 		= models.CharField(max_length=255)
	course_id 			= models.ForeignKey(Courses,on_delete=models.CASCADE,default=1)
	staff_id 			= models.ForeignKey(CustomUser,on_delete=models.CASCADE)
	created_at 			= models.DateTimeField(auto_now_add=True)
	updated_at 			= models.DateTimeField(auto_now_add=True)
	objects 			= models.Manager()


class Students(models.Model):
	admin 				= models.OneToOneField(CustomUser,on_delete=models.CASCADE) 
	gender 				= models.CharField(max_length=255)
	profile_pic 		= models.FileField()
	address 			= models.TextField()
	course_id 			= models.ForeignKey(Courses,on_delete=models.DO_NOTHING)
	session_start_year  = models.DateField()
	session_end_year 	= models.DateField()
	created_at 			= models.DateTimeField(auto_now_add=True)
	updated_at 			= models.DateTimeField(auto_now_add=True)
	objects 			= models.Manager()


class Attendance(models.Model):
	subject 			= models.ForeignKey(Subjects,on_delete=models.DO_NOTHING)
	attendance_date 	= models.DateTimeField(auto_now_add=True)
	created_at 			= models.DateTimeField(auto_now_add=True)
	updated_at 			= models.DateTimeField(auto_now_add=True)
	objects 			= models.Manager()


class AttendanceReport(models.Model):
	student 			= models.ForeignKey(Students,on_delete=models.DO_NOTHING)
	attendance 			= models.ForeignKey(Attendance,on_delete=models.CASCADE)
	status 				= models.BooleanField(default=False)
	created_at 			= models.DateTimeField(auto_now_add=True)
	updated_at 			= models.DateTimeField(auto_now_add=True)
	objects 			= models.Manager()


class LeaveReportStaff(models.Model):
	staff 				= models.ForeignKey(Staffs,on_delete=models.CASCADE)
	leave_date 			= models.CharField(max_length=255)
	leave_message 		= models.TextField()
	leave_status 		= models.BooleanField(default=False)
	created_at 			= models.DateTimeField(auto_now_add=True)
	updated_at 			= models.DateTimeField(auto_now_add=True)
	objects 			= models.Manager()



class FeedBackStudent(models.Model):
	student 			= models.ForeignKey(Students,on_delete=models.DO_NOTHING)
	feedback 			= models.TextField()
	feedback_reply 		= models.TextField()
	created_at 			= models.DateTimeField(auto_now_add=True)
	updated_at 			= models.DateTimeField(auto_now_add=True)
	objects 			= models.Manager()


class FeedBackStaffs(models.Model):
	staff 				= models.ForeignKey(Staffs,on_delete=models.CASCADE) 
	feedback 			= models.TextField()
	feedback_reply 		= models.TextField()
	created_at 			= models.DateTimeField(auto_now_add=True)
	updated_at 			= models.DateTimeField(auto_now_add=True)
	objects 			= models.Manager()



class NotificationStudent(models.Model):
	student 			= models.ForeignKey(Students,on_delete=models.DO_NOTHING)
	message 			= models.TextField()
	created_at 			= models.DateTimeField(auto_now_add=True)
	updated_at 			= models.DateTimeField(auto_now_add=True)
	objects 			= models.Manager()


class NotificationStaffs(models.Model):
	staff 				= models.ForeignKey(Staffs,on_delete=models.CASCADE) 
	message 			= models.TextField()
	created_at 			= models.DateTimeField(auto_now_add=True)
	updated_at 			= models.DateTimeField(auto_now_add=True)
	objects 			= models.Manager()



@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
	if created:
		if instance.user_type == 1:
			AdminHot.objects.create(admin=instance)
		if instance.user_type == 2:
			Staffs.objects.create(admin=instance,address='')
		if instance.user_type == 3:
			Students.objects.create(admin=instance,course_id=Courses.objects.get(id=1),session_start_year='2022-01-01',session_end_year='2023-01-01',address='',profile_pic='',gender='')


@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
	if instance.user_type == 1:
		instance.adminhot.save()
	if instance.user_type == 2:
		instance.staffs.save()
	if instance.user_type == 3:
		instance.students.save()