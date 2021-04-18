from django.shortcuts import render
from .forms import CommentForm

#My views
from blog.models import Post, Comment, Category

def blog_index(request):
	posts = Post.objects.all().order_by('-created_on')
	categories = Category.objects.all().order_by('name')
	context = {
		"posts": posts,
		"categories": categories,
	}

	return render(request, "blog_index.html", context)

def blog_category(request, category):
	posts = Post.objects.filter(
			categories__name__contains = category
		).order_by(
			'-created_on'
		)
	categories = Category.objects.all().order_by('name')
	context = {
		"category": category,
		"categories": categories,
		"posts": posts,
	}

	return render(request, "blog_category.html", context)

def blog_detail(request, pk):
	post = Post.objects.get(pk = pk)

	form = CommentForm()
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = Comment(
					author = form.cleaned_data['author'],
					body = form.cleaned_data['body'],
					post = post
				)
			comment.save()

	comments = Comment.objects.filter(post = post)
	context = {
		"post": post,
		"comments": comments,
		"form": form,
	}

	return render(request, "blog_detail.html", context)