#Importing libraries and models
from django import forms
from .models import Post, Category
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User

#choices = [('Coding', 'Coding'), ('Sports','Sports'), ('Entertainment','Entertainment'),]
#Getting all the tags of the posts created by the admin together
tags = Category.objects.all().values_list('name','name')

#Creating a temporary list to append all the tags
choice_list = []
for item in tags:
	choice_list.append(item)


class PostForm(forms.ModelForm):
	'''
		This is the PostForm where the user can post a new blog on the webapp.
		The fields required to create the post are - 
		1) title - This is the title of the post which will be showcased on the webpage.
		2) title_tag - This is the main title(HTML title tag) which will be shown on the main tab.
		3) author - This is a default option present in django forms to change the author of the blogpost.
		(but we don't need to change the author and so I have passed the default value of the user's name)
		(Note that I have also commented out the author field in the widgets so that it won't be shown on the add_post.html page)
		4) category_title - This is the "Post's Tag" which defines the post's category.
		5) body - The main context of the post.
		6) snippet - The snippet or some part of the body which is to be shown on the main home page(home.html)
				instead of showing the entire blog on the homepage.
	'''
	class Meta:
		'''
			This is the Meta Class correponding to PostForm
			The class decides which "fields" are needed to be stored in the database.
			Also, the "widgets" which are to be shown on the add_post.html page
		'''
		model = Post

		fields = ('title','title_tag','author','category_title','body','snippet')

		widgets = {
			'title':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Title'}),
			'title_tag':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Title Tag'}),
			'author':forms.TextInput(attrs={'class':'form-control', 'value':'', 'id':'user', 'type':'hidden'}),
			#'author':forms.Select(attrs={'class':'form-control'}),
			'category_title':forms.Select(choices=choice_list, attrs={'class':'form-control'}),
			'body':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Enter Content'}),			
			'snippet':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Enter Snippet'}),			
		}


class EditForm(forms.ModelForm):
	'''
		This is the EditForm where the user can edit the blog on the webapp.
		The fields required to adit the post are - 
		1) title - This is the title of the post which will be showcased on the webpage.
		2) title_tag - This is the main title(HTML title tag) which will be shown on the main tab.
		5) body - The main context of the post.
		6) snippet - The snippet or some part of the body which is to be shown on the main home page(home.html)
				instead of showing the entire blog on the homepage .
	'''
	class Meta:
		'''
			This is the Meta Class correponding to EditForm.
			This class decides which "fields" are needed to be stored in the database.
			Also, the "widgets" which are to be shown on the update_post.html page.
		'''
		model = Post
		fields = ('title','title_tag','body','snippet')

		widgets = {
			'title':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Edit Title'}),
			'title_tag':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Edit Title Tag'}),
			'body':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Edit Content'}),			
			'snippet':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Edit Snippet'}),			
		}

class SignUpForm(UserCreationForm):
	'''
		This is the SignUpForm where the user can register on the webapp.
		The fields required to create an account are - 
		1) username(as part of the django UserCreationForm) - Username of the user.
		2) password1(as part of the django UserCreationForm) - Password entered by the user.
		3) password2(as part of the django UserCreationForm) - Re-entering the password for confirmation.
		4) email(custom field) - Email of the user.
		5) first_name(custom field) - First name of the user.
		6) last_name(custom field) - Last name of the user.
	'''

	# Stating the custom fields other than username, password1 and password2
	email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter Email'}))
	first_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter First Name'}))
	last=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Last Name'}))

	class Meta:
		'''
			This is the Meta Class correponding to SignUpForm.
			This class decides which "fields" are needed to be stored in the database.
		'''
		model=User
		fields=('username','first_name','last','email','password1','password2')

	def __init__(self, *args, **kwargs):
		'''
			Stating the class = form_control for all the default fields since I have used Django form instead of a form other than inbuilt django forms.
			Stating the default placeholders to be shown in the widgets on the html page
		'''
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class']='form-control'
		self.fields['username'].widget.attrs['placeholder']='Enter Username'
		self.fields['password1'].widget.attrs['class']='form-control'
		self.fields['password1'].widget.attrs['placeholder']='Enter Password'
		self.fields['password2'].widget.attrs['class']='form-control'
		self.fields['password2'].widget.attrs['placeholder']='Re-enter Password'

class EditProfileForm(UserChangeForm):
	'''
		This is the EditProfileForm where the user can edit the profile on the webapp.
		The fields required to edit the user profile are - 
		1) username - Username of the user.
		2) email - Email of the user.
		3) first_name - First name of the user.
		4) last_name - Last name of the user.
		(Note: You can even change the password on the registration/edit_profile.html webpage.
		There will be a link which will redirect to the PasswordChangesForm)
	'''

	#You can add many parameters for the user to edit. You can uncomment those statements for the same.
	email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Edit Email'}))
	first_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Edit First Name'}))
	last_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Edit Last Name'}))
	username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Edit Username'}))
	#last_login=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
	#is_superuser=forms.CharField(max_length=100,widget=forms.CheckboxInput(attrs={'class':'form-check'}))
	#is_staff=forms.CharField(max_length=100,widget=forms.CheckboxInput(attrs={'class':'form-check'}))
	#is_active=forms.CharField(max_length=100,widget=forms.CheckboxInput(attrs={'class':'form-check'}))
	#date_joined=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))

	class Meta:
		'''
			This is the Meta Class correponding to EditProfileForm.
			This class decides which "fields" are needed to be updated in the database.
		'''
		model=User
		fields=('username','first_name','last_name','email','password')

class PasswordsChangesForm(PasswordChangeForm):
	'''
		Please refer the Note given in docstring of EditProfileForm first to refer this docstring
		This is the PasswordsChangesForm where the user can change the password on the webapp.
		The fields required to edit the user profile are - 
		1) old_password - Old password of the user.
		2) new_password - New password of the user.
		3) new_password - Reconfirmation of the new password of the user.
	'''
	old_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'placeholder':'Enter Old Password'}))
	new_password1=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'placeholder':'Enter New Password'}))
	new_password2=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'placeholder':'Re-Enter New Password'}))

	class Meta:
		'''
			This is the Meta Class correponding to PasswordsChangesForm.
			This class decides which "fields" are needed to be updated in the database.
		'''
		model=User
		fields=('old_password','new_password1','new_password2')