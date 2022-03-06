from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
# Create your models here.

class User(AbstractUser):
    lecturer=models.BooleanField(default=False)
    pass

class Category(models.Model):
    category_name=models.CharField(max_length=100,default=None)

    def __str__(self):
        return f"{self.category_name}"

class Course(models.Model):
    creator=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="Course Creator")
    course_name=models.CharField(max_length=100,verbose_name="Course Name",default=None)
    course_description=models.TextField(max_length=200,verbose_name="Course Description",default=None)
    course_date=models.DateTimeField(default=datetime.datetime.now())
    course_thumbnail=models.URLField(verbose_name="Course Thumbnail URL",default=None)
    course_category=models.ForeignKey(Category,on_delete=models.SET("Miscellaneous"),verbose_name="Course Category",blank=True,null=True)
    subscribed_users=models.ManyToManyField(User,blank=True,related_name="subscribed_users")

    def __str__(self):
        return f"{self.course_name}"

class Notes(models.Model):
    creator=models.ForeignKey(User,on_delete=models.CASCADE,related_name="post_creator",verbose_name="Post Creator")
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="notes",verbose_name="Course",default=None)
    thumbnail=models.URLField(verbose_name="Thumbnail",default=None,blank=True)
    description=models.TextField(verbose_name="Notes Description",default=None,max_length=200)
    category=models.ForeignKey(Category,on_delete=models.SET("Miscellaneous"),verbose_name="Category")
    additional_category=models.CharField(max_length=200,verbose_name="Additional Tag(s)",default=None,blank=True)
    markdown_notes_content=models.TextField(verbose_name="Notes Content in Markdown", default=None)
    html_notes_content=models.TextField(verbose_name="HTML Notes Content", default=None)
    date=models.DateTimeField(default=datetime.datetime.now())
    title=models.CharField(max_length=100,verbose_name="Title",default=None)
    video_iframe=models.TextField(verbose_name="Video iframe",null=True,blank=True)
    like=models.ManyToManyField(User,blank=True,related_name="users")

    def __str__(self):
        return f"{self.id}) {self.title} | {self.course}"

class Profile(models.Model):
    person=models.ForeignKey(User,on_delete=models.CASCADE,related_name="person",default=None)
    following=models.ManyToManyField(User,blank=True,related_name="followers")
    follower=models.ManyToManyField(User,blank=True,related_name="following")

    def __str__(self):
        return f"{self.person}"

class Comment(models.Model):
    time_of_comment=models.DateTimeField(default=datetime.datetime.now())
    comment=models.TextField(default=None,verbose_name="Comment")
    commenter=models.ForeignKey(User,on_delete=models.CASCADE,related_name="commenter")
    note_commented=models.ForeignKey(Notes,on_delete=models.CASCADE,default=None)

    def __str__(self):
        return f"{self.id}) {self.commenter} commented on '{self.note_commented.title}'"


