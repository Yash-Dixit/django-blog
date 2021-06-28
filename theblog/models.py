from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from ckeditor.fields import RichTextField

from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver


#===========LoginUpdate Model - To store the Count number of logins of a specific user===========
class LoginUpdate(models.Model):
	'''
		This model has a one to one relation with the User Model(django default)
		When a new user is created the table is updated with the user id of that user
		and the count of login is set to 0
	'''
	action_user = models.OneToOneField(User, on_delete=models.CASCADE)
	login_count = models.IntegerField()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	'''
		The method create_user_profile is triggered by using a 'receiver' and signal called 'post_save' 
		such that when the user is registered on the webapp after that the table `theblog_loginupdate` is updated 
	'''
	if created:
		# Set action_user=user id and login_count=0
		LoginUpdate.objects.create(action_user=instance,login_count=0)

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
	'''
		The method log_user_login is triggered by using a 'receiver' and signal called 'user_logged_in' 
		such that whenever the user logs into the webapp after that the table `theblog_loginupdate` is updated 
	'''

	# The if condition is created only for the superuser of the app
	# Whenever the superuser is created then the theblog_loginupdate doesn't update so whenever the 
	# superuser logs into the webapp for the first time then the login_count is set to 1
	if not LoginUpdate.objects.filter(action_user=user.id).exists():
		LoginUpdate.objects.create(action_user=user,login_count=1)
	else:
		count=LoginUpdate.objects.get(action_user=user.id)
		count.login_count+=1
		count.save()



#===========Post Model - To store the Post details===========
class Post(models.Model):
	'''
		This model uses a foreign key of id from the User Model(django default)
		When a new post is created by the user is created the table is updated with 
		the post's details which are - 
		1) title - This is the title of the post which will be showcased on the webpage.
		2) title_tag - This is the main title(HTML title tag) which will be shown on the main tab.
		3) author - User id of the user.
		4) body - The main context of the post.
		5) post_date_time - The time and date of whenever the blog was posted.
		4) category_title - This is the "Post's Tag" which defines the post's category.
		6) snippet - The snippet or some part of the body which is to be shown on the main home page(home.html)
				instead of showing the entire blog on the homepage.
		7) Number of likes on the blogpost.

	'''
	title = models.CharField(max_length=255)
	title_tag = models.CharField(max_length=255)
	#CASCADE Deletes the blogs of the user once the user is deleted
	author = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
	#I have used RichTextField as an option for the user to make changes to the text without using html tags and also to add images.
	body = RichTextField(blank=True,null=True)
	post_date_time = models.DateTimeField(auto_now=True)
	category_title = models.CharField(max_length=255, default='Other')
	snippet = models.CharField(max_length=255)
	# The likes is a separate table consisting of a graph like structure to depict who as liked which post
	likes = models.ManyToManyField(User, related_name='blog_posts')

	def total_likes(self):
		'''
			This function returns the number of likes on a specific post.
		'''
		return self.likes.count()

	def __str__(self):
		'''
			This function returns the string "Title | User_id".
		'''
		return self.title + ' | ' + str(self.author)

	def get_absolute_url(self):
		'''
			This function redirects the user to the 'home.html' page
		'''
		#return reverse('article-detail', args=(str(self.id)))
		return reverse('home')



#===========Category Model To store the category type (post's tag name)===========
class Category(models.Model):
	'''
		The model "Category" stores the categories(tags) of the posts similar to something like a dictionary
	'''
	name = models.CharField(max_length=255)

	def __str__(self):
		'''
			This function returns the category.
		'''
		return self.name

	def get_absolute_url(self):
		'''
			This function redirects the user to the 'home.html' page
		'''
		#return reverse('article-detail', args=(str(self.id)))
		return reverse('home')