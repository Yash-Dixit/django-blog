from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post,Category
from .forms import PostForm, EditForm, SignUpForm, EditProfileForm, PasswordsChangesForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView

def LikeView(request, pk):
	'''
		The Function View "LikeView" takes the web request of the "Like" button
		and updates the Post Model. 
	'''
	post = get_object_or_404(Post, id=request.POST.get('post_id'))
	#Setting the like to False on the creation of a post
	liked=False
	# This if else condition updates the 'theblog_post_likes` table when the user clicks the like or the unlike button. 
	if post.likes.filter(id=request.user.id).exists():
		post.likes.remove(request.user)
		liked=False
	else:
		post.likes.add(request.user)
		liked=True
	
	#Whenever the user likes or unlikes the blog it will rediect to the same page 'article_detail.html'
	return HttpResponseRedirect(reverse('article-detail',args=[str(pk)]))


class HomeView(ListView):
	'''
	The Class View "HomeView" inherits the ListView.
	ListView is used to view all the blogs on the homepage.
	A custom ordering is used which orders the blogs with respect to the recent post first scheme.
	'''

	model = Post
	template_name = 'home.html'

	ordering=['-post_date_time']

	#Ordering posts by negative id
	#ordering=['-id']

	def get_context_data(self, *args, **kwargs):
		'''
			This function is responsible to show categories corresponding to the specific blogpost.
		'''
		cat_menu = Category.objects.all()
		context=super(HomeView, self).get_context_data(*args, **kwargs)
		context['cat_menu'] = cat_menu
		return context


def CategoryView(request, cats):
	'''
		The Function View "CategoryView" shows the different posts corresponding to the relevant category to the category.html page.
	'''
	category_posts = Post.objects.filter(category_title=cats.replace('-', ' '))
	return render(request, 'categories.html', {'cats':cats.title().replace('-', ' '), 'category_posts':category_posts})

def CategoryListView(request):
	'''
		The Function View "CategoryListView" shows the different categories present in the "theblog_category table" to the category_list.html page
	'''
	cat_menu_list = Category.objects.all()
	#print("HELLO WORLD==============", cat_menu_list)
	return render(request, 'category_list.html', {'cat_menu_list':cat_menu_list})

class ArticleDetailView(DetailView):
	'''
		The Class View "ArticleDetailView" shows the details about the post 
		when the title of the corresponding post is clicked on the home page.
		It inherits the DetailView as part of the Django package for the same purpose.
	'''
	model = Post
	template_name = 'article_details.html'

	def get_context_data(self, *args, **kwargs):
		'''
			This function returns details about the categories related to the Post.
		'''
		cat_menu = Category.objects.all()
		context=super(ArticleDetailView, self).get_context_data(*args, **kwargs)
		temp = get_object_or_404(Post,id=self.kwargs['pk'])		
		total_likes = temp.total_likes()

		liked=False
		if temp.likes.filter(id=self.request.user.id).exists():
			liked=True

		context['cat_menu'] = cat_menu
		context['total_likes'] = total_likes
		context['liked'] = liked
		return context

class AddPostView(CreateView):
	'''
		The Class View "ArticleDetailView" shows the form (uses the PostForm from forms.py) to add a new post.
		It inherits the CreateView as part of the Django package for the same purpose.
	'''
	model = Post
	form_class = PostForm
	template_name= 'add_post.html'
	#fields = '__all__'
	#fields = ('title', 'body')

class AddCategoryView(CreateView):
	'''
		The Class View "AddCategoryView" shows the form to add a new category.
		It inherits the CreateView as part of the Django package for the same purpose.
	'''
	model = Category
	template_name= 'add_category.html'
	fields = '__all__'

class UpdatePostView(UpdateView):
	'''
		The Class View "UpdatePostView" shows the form (uses the EditForm from forms.py) to edit the details of the post.
		It inherits the UpdateView as part of the Django package for the same purpose.
	'''
	model = Post
	form_class = EditForm
	template_name = 'update_post.html'
	#fields = ['title','title_tag','body']

class DeletePostView(DeleteView):
	'''
		The Class View "DeletePostView" is used to delete the post.
		It inherits the DeleteView as part of the Django package for the same purpose.
	'''
	model = Post
	template_name = 'delete_post.html'
	success_url = reverse_lazy('home')

class UserRegisterView(generic.CreateView):
	'''
		The Class View "UserRegisterView" shows the form (uses the SignUpForm from forms.py) to register to the webapp.
		It inherits the CreateView as part of the Django package for the same purpose.
	'''
	form_class = SignUpForm
	template_name = 'registration/register.html'
	success_url = reverse_lazy('login')

class UserEditView(generic.UpdateView):
	'''
		The Class View "UserEditView" shows the form (uses the EditProfileForm from forms.py) to edit the details of the user profile.
		It inherits the UpdateView as part of the Django package for the same purpose.
	'''
	form_class = EditProfileForm
	template_name = 'registration/edit_profile.html'
	success_url = reverse_lazy('home')

	def get_object(self):
		return self.request.user

class PasswordsChangeView(PasswordChangeView):
	'''
		The Class View "PasswordsChangeView" shows the form (uses the PasswordChangesForm from forms.py) to change the password of the user profile.
		It inherits the PasswordChangeView as part of the Django package for the same purpose.
	'''
	form_class=PasswordsChangesForm
	template_name = 'registration/change_password.html'
	success_url = reverse_lazy('edit_profile')