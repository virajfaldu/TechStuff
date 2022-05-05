from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from blog.models import *
from django.contrib.auth import logout, login, authenticate
from django.views.decorators.csrf import csrf_exempt
import requests
import json

#Main (Home) Page Content
def index(request):
	try:
		allCate = Cate.objects.all() #Fetching Categories
		allPost = Post.objects.all().order_by("id").reverse()[:4] #Fetching Posts
		popularPost = Post.objects.all().order_by("views").reverse()[:5] #Fetching Popular Posts By Views

		context = {
			"allCate": allCate,
			"allPost": allPost,
			"popularPost": popularPost
		}
		return render(request, 'blog/index.html', context)
	except Exception as e:
		print(e)
		return redirect('Home')

#Adding Post
def add_post(request):
	allCate = Cate.objects.all()
	verify = ""
	msg = ""
	if request.method == "POST":
		title = request.POST['form_title']
		desc = request.POST['form_desc']
		category = request.POST['category_val']
		user = request.user
		img = request.FILES.get('thumbnail')
		cate = Cate.objects.filter(id=category).first()
		
		if desc == "":
			verify = False
			msg = "Please Enter Description"
			return render(request, 'blog/add-post.html',{"allCate":allCate, "verify":verify, "errorMsg":msg})
			
		if category == 'none':
			verify = False
			msg = "Please Select Category"
			return render(request, 'blog/add-post.html',{"allCate":allCate, "verify":verify, "errorMsg":msg})
			
		if img == None:
			verify = False
			msg = "Please Select Image"
			return render(request, 'blog/add-post.html',{"allCate":allCate, "verify":verify, "errorMsg":msg})

        # Captcha
		clientKey = request.POST['g-recaptcha-response']
		secretKey = '6LeEj-gZAAAAAKIPCPPdATO4vCnOfYqC_viPIRU_'
		
		captchaData = {
            'secret': secretKey,
            'response': clientKey
        }
		r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=captchaData)
		response = json.loads(r.text)
		verifyRes = response['success']
		
		if verifyRes:
			postObj = Post()
			postObj.title = title
			postObj.desc = desc
			postObj.img = img
			postObj.categoty = cate
			postObj.post_by = user
			postObj.save()
			verify = True
			msg = "Post Added Successfully"
			return render(request, 'blog/add-post.html', {"allCate": allCate, "verify": verify, "errorMsg": msg})
		else:
			verify = False
			msg = "reCaptcha Validation Failed"
			return render(request, 'blog/add-post.html', {"allCate": allCate, "verify": verify, "errorMsg": msg})
	else:
		return render(request, 'blog/add-post.html', {"allCate":allCate})
	
#Displaying Post
def show_post(request, title=""):
	try:
		post = Post.objects.filter(title=title).first(); #Fetching Post By Title
		popularPost = Post.objects.all().order_by("views").reverse()[:5] #Fetching Popular Posts By Views
		total_likes = Like.objects.filter(liked_to=post).count() #Calculating Total Likes On Post
		total_comments = Comment.objects.filter(comment_to=post).count() #Calculating Total Comments On Post
		comments = Comment.objects.filter(comment_to=post).order_by("id").reverse()[:10] #Fetching Comments

		if request.user.is_authenticated:
			user = request.user
			isLike = Like.objects.filter(liked_by=user, liked_to=post).count()

			if(isLike > 0):
				isLike = True
			else:
				isLike = False
		else:
			isLike = False

		#Increasing Views
		post.views = post.views + 1;
		post.save()

		context = {
		"post":post,
		"popularPost":popularPost,
		"total_likes":total_likes,
		"total_comments":total_comments,
		"isLike":isLike,
		"comments":comments
		}
		return render(request, 'blog/show_post.html', context)
	except Exception as e:
		print(e)
		return redirect('Home')

#Showing Categories
def show_cate(request, title):
	try:
		cat = Cate.objects.filter(name=title).first()
		posts = Post.objects.filter(categoty=cat)

		context = {
			"posts":posts,
			"cateName":title
		}
		return render(request, 'blog/show_category.html', context)
	except Exception as e:
		print(e)
		return redirect('Home')

#Adding Contact Details
def contact(request):
	if request.user.is_authenticated:
		try:
			details = request.POST['desc'] #Fetching Desc
			con = Contact()
			con.contact_by = request.user
			con.contact_detail = details
			con.save()

			context = {
				'status':True
			}

			return JsonResponse(context)
		except Exception as e:
			context = {
				'status':False
			}
			print(e)
			return JsonResponse(context)
	else:
		return JsonResponse({'redirect':True})

#Adding Likes To Posts
def add_like(request):
	if request.user.is_authenticated:
		try:
			user = request.user #Get User
			title = request.POST['title'] #Get Title
			post = Post.objects.filter(title=title).first() #Fetching Post
			lk = Like()
			lk.liked_by = user
			lk.liked_to = post
			lk.save() #Like Saved
			totalLikes = Like.objects.filter(liked_to=post).count() #Counting Likes
			context = {
				'status':True,
				'totalLikes':totalLikes
			}
		except:
			context = {
				'status':False
			}
		return JsonResponse(context)
	else:
		return JsonResponse({'redirect':True})

#Removing Likes
def remove_like(request):
	if request.user.is_authenticated:
		try:
			user = request.user #Get User
			title = request.POST['title'] #Get title
			post = Post.objects.filter(title=title).first() #Fetching post
			lk = Like.objects.filter(liked_by=user, liked_to=post)
			lk.delete() #deleting like
			totalLikes = Like.objects.filter(liked_to=post).count() #Counting Likes
			context = {
				'status':True,
				'totalLikes':totalLikes
			}
		except:
			context = {
				'status':False
			}
		return JsonResponse(context)
	else:
		return JsonResponse({'redirect':True})

#Adding Comments
@login_required(login_url='Login')
def add_comment(request):
	if request.user.is_authenticated:
		try:
			title = request.POST['title']
			desc = request.POST['desc']
			user = request.user #Fetching User
			post = Post.objects.filter(title=title).first() #Fetching Post

			comm = Comment()
			comm.comment_by = user
			comm.comment_to = post
			comm.desc = desc
			comm.save()

			cmt = Comment.objects.filter(comment_to=post, comment_by=user).order_by('id').reverse().values()
			cmtCount = Comment.objects.filter(comment_to=post).count()
			username = user.username
			allComment = list(cmt)

			context = {
				'status':True,
				'allComment':allComment,
				'username':username,
				'cmtCount':cmtCount
			}

			return JsonResponse(context)
		except Exception as e:
			context = {
				'status':False
			}
			return JsonResponse(context)
	else:
		return JsonResponse({'redirect':True})

#Creating User
def auth_register(request):
	if request.method == "POST":
		username = request.POST['username']
		pwd = request.POST['pwd']
		email = request.POST['email']
		clientKey = request.POST['clientKey']

		secretKey = '6LeEj-gZAAAAAKIPCPPdATO4vCnOfYqC_viPIRU_'
		captchaData = {
            'secret': secretKey,
            'response': clientKey
        }
		
		r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=captchaData)
		response = json.loads(r.text)
		verifyRes = response['success']
		
		repeatUsername = User.objects.filter(username=username)
		repeatEmail = User.objects.filter(email=email)
		
		if len(repeatUsername) > 0:
			context = {
				'status':False,
				'errorMsg':"Username Already In Use"
			}
			return JsonResponse(context)
		elif len(repeatEmail) > 0:
			context = {
				'status':False,
				'errorMsg':"Email Address Already In Use"
			}
			return JsonResponse(context)

		if verifyRes:
			obj = User.objects.create_user(username=username, email=email, password=pwd)
			obj.save()
			context = {
				'status':True
			}
			return JsonResponse(context)
		else:
			context = {
				'status':False,
				'errorMsg':"reCaptcha Validation Failed"
			}
			return JsonResponse(context)
	else:
		return render(request, 'blog/signin.html')

#Login User
def auth_login(request):
	if request.method == "POST":
		username = request.POST['username']
		pwd = request.POST['pwd']
		clientKey = request.POST['clientKey']
		
		secretKey = '6LeEj-gZAAAAAKIPCPPdATO4vCnOfYqC_viPIRU_'
		captchaData = {
            'secret': secretKey,
            'response': clientKey
        }
		
		r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=captchaData)
		response = json.loads(r.text)
		verifyRes = response['success']

		if verifyRes:
			user = authenticate(request, username=username, password=pwd)
			if user is not None:
				login(request, user)
				context = {
					'status':True
				}
				return JsonResponse(context)
			else:
				context = {
					'status':False,
					'msg':'Invalid Username Or Password'
				}
			return JsonResponse(context)
		else:
			context = {
				'status':False,
				'msg':'reCaptcha Validation Failed'
			}
			return JsonResponse(context)
	else:
		context = {

		}
		return render(request, 'blog/login.html', context)

#Logout User
def auth_logout(request):
	try:
		logout(request) #Loggingout
		return redirect('Home')
	except Exception as e:
		print(e)
		return redirect('Home')

def user_account(request):
	if request.user.is_authenticated:
		userPosts = Post.objects.filter(post_by=request.user).order_by("id").reverse()
		totalPosts = userPosts.count()
		totalLikes = countLikes(request, userPosts)
		totalComments = countComments(request, userPosts)
		totalViews = countViews(request, userPosts)
		context = {
			"userPosts":userPosts,
			"totalPosts":totalPosts,
			"totalLikes":totalLikes,
			"totalComments":totalComments,
			"totalViews":totalViews,
		}
		return render(request, 'blog/dashbord.html', context)
	else:
		return redirect('Login')

def countLikes(request, userPosts):
	likes = 0
	for post in userPosts:
		likes += Like.objects.filter(liked_to=post).count()
	return likes

def countComments(request, userPosts):
	comments = 0
	for post in userPosts:
		comments += Comment.objects.filter(comment_to=post).count()
	return comments

def countViews(request, userPosts):
	views = 0
	for post in userPosts:
		views += post.views
	return views

def post_approve(request):
	if request.user.is_superuser:
		posts = Post.objects.filter(approve=False).order_by("id").reverse()
		context = {
			"posts":posts
		}
		return render(request, 'blog/approve.html', context)
	else:
		return HttpResponse("You Are Not Allowed")

def action(request, act, pid):
	post = Post.objects.filter(id=pid).first()
	if act == "del":
		try:
			post.delete()
		except:
			pass
	elif act == "apr":
		try:
			post.approve = True
			post.save()
		except:
			pass
	else:
		pass

	return post_approve(request)
	
def search(request):
	query = request.GET['query']
	results = Post.objects.filter(title__icontains=query ,approve=True)
	return render(request, 'blog/search.html',{"results":results})