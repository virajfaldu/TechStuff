from django.db import models
from django.contrib.auth.models import User

class Cate(models.Model):
	cate_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	name = models.CharField(max_length=50, default="")
	img = models.ImageField(upload_to="category", default="")

	def __str__(self):
		return self.name

	def delete(self, *args, **kwargs):
		self.img.delete()
		super().delete(*args, **kwargs)

class Post(models.Model):
	title = models.CharField(max_length=300, default="")
	img = models.ImageField(upload_to="post")
	desc = models.CharField(max_length=15000,default="")
	categoty = models.ForeignKey(Cate, on_delete=models.CASCADE, null=True)
	views = models.IntegerField(default=0)
	approve = models.BooleanField(default=False)
	date = models.DateField(auto_now_add=True)
	post_by = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	def delete(self, *args, **kwargs):
		self.img.delete()
		super().delete(*args, **kwargs)

class Contact(models.Model):
	contact_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	contact_detail = models.CharField(max_length=500, default="")

	def __str__(self):
		return "Contact By " + self.contact_by.username

class Comment(models.Model):
	comment_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	desc = models.CharField(max_length=500, default="")
	comment_to = models.ForeignKey(Post, on_delete=models.CASCADE)
	time = models.DateField(auto_now_add=True)

	def __str__(self):
		return "Commented By " + self.comment_by.username + " On " + self.comment_to.title

class Like(models.Model):
	liked_by = models.ForeignKey(User, on_delete=models.CASCADE)
	liked_to = models.ForeignKey(Post, on_delete=models.CASCADE)

	def __str__(self):
		return f"Liked By {self.liked_by.username} On {self.liked_to.title}"