from django.shortcuts import render_to_response, render, redirect
from app.models import EditorModel, ArticleModel, AuthorModel, KeywordModel, ReleaseModel, FileModel
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.base import TemplateView
from app.forms import ArticleModelForm, LoginForm, AuthorModelForm, ReleaseModelForm, EditorModelForm, ArticleEditModelForm, UploadFileForm
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required,  login_required
from django.contrib.auth.models import User, Group, Permission
from time import gmtime, strftime
import xlrd
from django.views.decorators.csrf import csrf_exempt

def get_usergroup(request):
	try:
		user = User.objects.get(username=request.user)
		group1 = Group.objects.get(name='Authors').user_set.all()
		group2 = Group.objects.get(name='Editors').user_set.all()
		if user.username=='Admin':
			usergroup = 'Admins'
		if user in group1:
			usergroup = 'Authors'
		if user in group2:
			usergroup = 'Editors'
	except:
		usergroup = 'Guests'
	return usergroup

@csrf_exempt
def upload_file(request):
	data_name = 'Загрузка информации в БД'
	if Group.objects.filter(name='Authors').count() == 0:
		Group.objects.create(name='Admins')
		Group.objects.create(name='Editors')
		Group.objects.create(name='Authors')
		Group.objects.create(name='Guests')
		return redirect('articles')
	else:
		usergroup = get_usergroup(request)
		if usergroup == 'Admins':
			if request.method == 'POST':
				form = UploadFileForm(request.POST, request.FILES)
				if form.is_valid():
					# так производится создание объектов модели FileModel и запись их в базу данных
					p1 = FileModel.objects.create(file = request.FILES['file'])
					data_way1 = 'app/static/'
					data_way2 = str(request.FILES['file'])
					data_way = data_way1 + data_way2
					excel_data_file = xlrd.open_workbook(data_way)
					sheet_3 = excel_data_file.sheet_by_index(3) #Users, Авторы
					sheet_4 = excel_data_file.sheet_by_index(4) #Usrrs, Редакторы
					row_number = sheet_3.nrows  # количество строк
					if row_number > 0:  # Проверка на пустоту файла
						for row in range(1, row_number):
							if User.objects.filter(username=str(sheet_3.row(row)[0]).replace("text:","").replace("'","")).count() == 0:
								user = User.objects.create_user(username=str(sheet_3.row(row)[0]).replace("text:","").replace("'",""),
									email=str(sheet_3.row(row)[7]).replace("text:","").replace("'",""), password=str(sheet_3.row(row)[0]).replace("text:","").replace("'",""))
								group = Group.objects.get(name='Authors')
								group.user_set.add(user)
								permission = Permission.objects.get(name='Can add Article')
								user.user_permissions.add(permission)
								permission = Permission.objects.get(name='Can change Article')
								user.user_permissions.add(permission)
								permission = Permission.objects.get(name='Can delete Article')
								user.user_permissions.add(permission)
								AuthorModel.objects.create(login = user, index = "", name = str(sheet_3.row(row)[1]).replace("text:","").replace("'",""),
									birth_date = str(sheet_3.row(row)[2]).replace("text:","").replace("'","").replace(".",""), degree = str(sheet_3.row(row)[3]).replace("text:","").replace("'",""),
										title = str(sheet_3.row(row)[4]).replace("text:","").replace("'",""), work = str(sheet_3.row(row)[5]).replace("text:","").replace("'",""),
											position = str(sheet_3.row(row)[6]).replace("text:","").replace("'",""), email = str(sheet_3.row(row)[7]).replace("text:","").replace("'",""),
												education = str(sheet_3.row(row)[8]).replace("text:","").replace("'",""))
								author = AuthorModel.objects.get(index="")
								author.index = str(author.id)
								author.save()
					row_number = sheet_4.nrows  # количество строк
					if row_number > 0:  # Проверка на пустоту файла
						for row in range(1, row_number):
							if User.objects.filter(username=str(sheet_4.row(row)[0]).replace("text:","").replace("'","")).count() == 0:
								user = User.objects.create_user(username=str(sheet_4.row(row)[0]).replace("text:","").replace("'",""),
									email=str(sheet_4.row(row)[8]).replace("text:","").replace("'",""), password=str(sheet_4.row(row)[0]).replace("text:","").replace("'",""))
								group = Group.objects.get(name='Editors')
								group.user_set.add(user)
								editor = EditorModel.objects.create(login = user, name_magazine = str(sheet_4.row(row)[3]).replace("text:","").replace("'",""),
									name = str(sheet_4.row(row)[1]).replace("text:","").replace("'",""),
										birth_date = str(sheet_4.row(row)[2]).replace("text:","").replace("'","").replace(".",""), degree = str(sheet_4.row(row)[4]).replace("text:","").replace("'",""),
											title = str(sheet_4.row(row)[5]).replace("text:","").replace("'",""), work = str(sheet_4.row(row)[6]).replace("text:","").replace("'",""),
												position = str(sheet_4.row(row)[7]).replace("text:","").replace("'",""), email = str(sheet_4.row(row)[8]).replace("text:","").replace("'",""),
													education = str(sheet_4.row(row)[9]).replace("text:","").replace("'",""))
					p1.delete()
					data_name = "Загрузка завершена"
					return render_to_response('upload.html', {'data_name': data_name})
				else:
					return render_to_response('upload.html', {'form': form, 'data_name': "Ошибка ввода данных"})
			else:
				form = UploadFileForm()
			return render_to_response('upload.html', {'form': form, 'data_name': data_name})
		else:
			return redirect('articles')
	
def give_keywords(keywords, article):
	keyword = ""
	for symbol in keywords:
		if symbol == ",":
			KeywordModel.objects.create(name = keyword, article = article)
			keyword = ""
		else:
			keyword = keyword + symbol
	KeywordModel.objects.create(name = keyword, article = article)
	
def get_keywords(id):	
	first = True
	keywords = ""
	for keyword in KeywordModel.objects.filter(article = ArticleModel.objects.get(id = id)):
		if first:
			keywords = keyword.name
			first = False
		else:
			keywords = keywords + "," + keyword.name
	return keywords

class LoginView(TemplateView):
	form = None
	message = ""
	template_name = "login.html"
	def get(self, request, *args, **kwargs):
		self.form = LoginForm()
		return super(LoginView, self).get(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(LoginView, self).get_context_data(**kwargs)
		context["message"] = self.message
		context["form"] = self.form
		return context
	def post(self,request,*args,**kwargs):
		self.form = LoginForm(request.POST)
		if self.form.is_valid():
			user = authenticate(username = self.form.cleaned_data["username"], password = self.form.cleaned_data["password"])
			if user is not None:
				if user.is_active:
					login(request, user)
					usergroup = get_usergroup(request)
					if usergroup=='Authors':
						return redirect("articles")
					if usergroup=='Editors':
						return redirect("releases")
					else:
						return redirect("articles")
				else:
					return super(LoginView, self).get(request, *args, **kwargs)
			else:
				self.message = "Неверное имя пользователя или пароль"
				return super(LoginView, self).get(request, *args, **kwargs)
		else:
			return super(LoginView, self).get(request, *args, **kwargs)
			
class LogoutView(TemplateView):
	template_name = "logout.html"
	def get(self, request, *args, **kwargs):
		logout(request)
		return super(LogoutView, self).get(request, *args, **kwargs)

def registration(request):
	if request.method == "POST":
		form = AuthorModelForm(request.POST)
		if form.is_valid():
			try:
				user = User.objects.create_user(username=form.cleaned_data["login"], email=form.cleaned_data["email"], password=form.cleaned_data["password"])
				group = Group.objects.get(name='Authors')
				group.user_set.add(user)
				permission = Permission.objects.get(name='Can add Article')
				user.user_permissions.add(permission)
				permission = Permission.objects.get(name='Can change Article')
				user.user_permissions.add(permission)
				permission = Permission.objects.get(name='Can delete Article')
				user.user_permissions.add(permission)
				AuthorModel.objects.create(login = user, index = "", name = form.cleaned_data["name"], birth_date = form.cleaned_data["birth_date"], degree = form.cleaned_data["degree"], title = form.cleaned_data["title"], work = form.cleaned_data["work"], position = form.cleaned_data["position"], email = form.cleaned_data["email"], education = form.cleaned_data["education"])
				author = AuthorModel.objects.get(index="")
				author.index = str(author.id)
				author.save()
				return redirect("login")
			except:
				return render(request, "registration.html", {"form": form, "message": "Ошибка"})
		else:
			return render(request, "registration.html", {"form": form, "message": ""})
	else:
		form = AuthorModelForm()
		return render(request, "registration.html", {"form": form, "message": ""})

def registration_editors(request):
	if request.method == "POST":
		form = EditorModelForm(request.POST)
		if form.is_valid():
			try:
				user = User.objects.create_user(username=form.cleaned_data["login"], email=form.cleaned_data["email"], password=form.cleaned_data["password"])
				group = Group.objects.get(name='Editors')
				group.user_set.add(user)
				EditorModel.objects.create(login = user, name_magazine = form.cleaned_data["name_magazine"], name = form.cleaned_data["name"], birth_date = form.cleaned_data["birth_date"], degree = form.cleaned_data["degree"], title = form.cleaned_data["title"], work = form.cleaned_data["work"], position = form.cleaned_data["position"], email = form.cleaned_data["email"], education = form.cleaned_data["education"])
				return redirect("login")
			except:
				return render(request, "registration_editors.html", {"form": form, "message": "Такое имя пользователя уже существует"})
		else:
			return render(request, "registration_editors.html", {"form": form, "message": ""})
	else:
		form = EditorModelForm()
		return render(request, "registration_editors.html", {"form": form, "message": ""})

class ArticleListView(ListView):
	template_name = "articles.html"
	queryset = ArticleModel.objects.order_by("name")
	articles = ArticleModel.objects.exclude(release_date=None)
	keywords = KeywordModel.objects.all()
	def get(self, request, *args, **kwargs):
		self.usergroup = get_usergroup(request)
		if self.usergroup=='Authors':
			user=User.objects.get(username=request.user)
			author=AuthorModel.objects.get(login=user)
			self.articles = ArticleModel.objects.filter(author=author)	
		return super(ArticleListView,self).get(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(ArticleListView,self).get_context_data(**kwargs)
		context["Articles"] = self.articles
		context["Keywords"] = self.keywords
		context["usergroup"] = self.usergroup
		return context
	def get_queryset(self):
		return ArticleModel.objects.order_by("name")

class ReleaseListView(ListView):
	template_name = "releases.html"
	queryset = ReleaseModel.objects.order_by("number_release")
	usergroup = 'Guests'
	releases = ReleaseModel.objects.exclude(release_date=None)
	articles = ArticleModel.objects.exclude(release_date=None)
	def get(self, request, *args, **kwargs): 
		self.usergroup = get_usergroup(request)
		if self.usergroup=='Editors':
			user=User.objects.get(username=request.user)
			editor=EditorModel.objects.get(login=user)
			self.releases = ReleaseModel.objects.filter(editor=editor)
			self.articles = ArticleModel.objects.filter(name_magazine=editor.name_magazine).filter(release_date=None)
		return super(ReleaseListView,self).get(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(ReleaseListView,self).get_context_data(**kwargs)
		context["Releases"] = self.releases
		context["usergroup"] = self.usergroup
		context["Articles"] = self.articles
		context["Keywords"] = KeywordModel.objects.all()
		return context
	def get_queryset(self):
		return ReleaseModel.objects.order_by("number_release")

def article_create(request):
	usergroup = get_usergroup(request)
	if usergroup=='Authors':
		if request.method == "POST":
			form = ArticleModelForm(request.POST)
			if form.is_valid():
				form.save()
				article = ArticleModel.objects.get(DOI="")
				article.DOI = article.id
				article.save()
				keywords = form.cleaned_data["keywords"]
				give_keywords(keywords, article)
				return redirect("articles")
			else:
				return render(request, "article_add.html", {"form": form})
		else:
			form = ArticleModelForm()
			return render(request, "article_add.html", {"form": form})
	else:
		return redirect("articles")

def release_create(request):
	usergroup = get_usergroup(request)
	if usergroup=='Editors':
		user = User.objects.get(username=request.user)
		editor = EditorModel.objects.get(login=user)
		if ReleaseModel.objects.filter(editor=editor).filter(release_date=None).count() < 1:
			if request.method == "POST":
				form = ReleaseModelForm(request.POST)
				if form.is_valid():
					form.save()
					user = User.objects.get(username=request.user)
					editor = EditorModel.objects.get(login=user)
					release = ReleaseModel.objects.get(ISSN="")
					release.ISSN = release.id
					release.save()
					release.name_magazine = editor.name_magazine
					release.number_release = ReleaseModel.objects.filter(editor=editor).count() + 1
					release.name_editor = editor.name
					release.editor = editor
					release.save()
					return redirect("releases")
				else:
					return render(request, "release_add.html", {"form": form})
			else:
				form = ReleaseModelForm()
				return render(request, "release_add.html", {"form": form})
		else:
			return redirect("releases")
	else:
		return redirect("releases")		

def article_update(request, id):
	usergroup = get_usergroup(request)
	if usergroup == 'Authors':
		user=User.objects.get(username=request.user)
		author=AuthorModel.objects.get(login=user)
		try:
			article = ArticleModel.objects.get(id=id)
			if article in ArticleModel.objects.filter(author=author) and article.release == None:
				if request.method == "POST":
					form = ArticleModelForm(request.POST, instance=ArticleModel.objects.get(id=id))
					if form.is_valid():
						form.save()
						article = ArticleModel.objects.get(id=id)
						KeywordModel.objects.filter(article = article).delete()
						keywords = form.cleaned_data["keywords"]
						give_keywords(keywords, article)
						return redirect("articles")
					else:
						return render(request, "edit_article.html", {"form": form})
				else:
					form = ArticleModelForm(instance=ArticleModel.objects.get(id=id))
					keywords = get_keywords(id)
					form.fields['keywords'].initial = keywords
					return render(request, "edit_article.html", {"form": form})
			else:
				return redirect("articles")
		except:
			return redirect("articles")
	else:
		return redirect("articles")	

def article_edit(request, index):
	usergroup = get_usergroup(request)
	if usergroup=='Editors':
		user=User.objects.get(username=request.user)
		editor=EditorModel.objects.get(login=user)
		try:
			article = ArticleModel.objects.get(id=index)
			if article.name_magazine==editor.name_magazine and ReleaseModel.objects.filter(editor=editor).filter(release_date=None).count()!=0 and article.release_date == None:
				releases = ReleaseModel.objects.filter(release_date=None).filter(editor=editor)
				if request.method == "POST":
					form = ArticleEditModelForm(request.POST, instance=ArticleModel.objects.get(id=index))
					if form.is_valid():
						form.save()
						KeywordModel.objects.filter(article=article).delete()
						keywords = form.cleaned_data["keywords"]
						give_keywords(keywords, article)
						article.cost = form.cleaned_data["cost"]
						article.release = form.cleaned_data["release"]
						article.name_publisher = article.release.name_publisher
						article.number_release = article.release.number_release
						article.save()
						return redirect("releases")
					else:
						return render(request, "edit_article.html", {"form": form})
				else:
					form = ArticleEditModelForm(instance=ArticleModel.objects.get(id=index))
					keywords = get_keywords(id=index)
					form.fields['keywords'].initial = keywords
					form.fields['release'].queryset = releases
					return render(request, "edit_article.html", {"form": form})
			else:
				return redirect("releases")
		except:
			return redirect("releases")
	else:
		return redirect("releases")

def article_delete(request, id):
	usergroup = get_usergroup(request)
	if usergroup=='Authors':
		user=User.objects.get(username=request.user)
		author=AuthorModel.objects.get(login=user)
		try:
			article = ArticleModel.objects.get(id=id)
			if author in article.author.all() and article.release_date == None and article != None:
				if request.method == "POST":
					ArticleModel.objects.get(id=id).delete()
					return redirect("articles")
				else:
					return render(request, "delete_article.html", {'article': article.number_release})
			else:
				return redirect("articles")
		except:
			return redirect("articles")
	else:
		return redirect("articles")		

def article_add(request, id):
	usergroup = get_usergroup(request)
	try:
		release = ReleaseModel.objects.get(id=id)
		Articles = ArticleModel.objects.filter(release=release)
		if release.release_date == None:
			if usergroup == 'Editors':
				user = User.objects.get(username=request.user)
				if release.editor == EditorModel.objects.get(login=user):
					release.release_date = strftime("%Y-%m-%d", gmtime())
					release.ISSN = str(release.id) + "." + str(release.editor.id) + "/" + release.release_date
					release.save()
					for article in Articles:
						Authors = article.author.all()
						article.release_date = release.release_date
						article.ISSN = release.ISSN
						article.name_publisher = release.name_publisher
						AuthorsArrayId = ""
						first = True
						for author in Authors:
							if first:
								AuthorsArrayId = str(author.id)
								first = False
							else:
								AuthorsArrayId = AuthorsArrayId + "-" + str(author.id)
						article.DOI = str(article.id) + "." + AuthorsArrayId + "/" + article.release_date
						article.save()
					return redirect("releases")
				else:
					return redirect("releases")
			else:
				return redirect("releases")
		else:
			return redirect("releases")
	except:
		return redirect("releases")

def articlerelease(request, id, index):
	usergroup = get_usergroup(request)
	try:
		article = ArticleModel.objects.get(id=id)
		Keywords = KeywordModel.objects.all()
		Authors = article.author.all()
		if article.release_date == None:
			if usergroup=='Editors':
				user = User.objects.get(username=request.user)
				if article.release.editor == EditorModel.objects.get(login=user):
					return render_to_response('article.html', {'article': article, 'Keywords': Keywords, 'Authors': Authors, 'usergroup': usergroup})
				else:
					return redirect("releases")
			else:
				return redirect("releases")
		else:
			return render_to_response('article.html', {'article': article, 'Keywords': Keywords, 'Authors': Authors, 'usergroup': usergroup})
	except:
		return redirect("releases")
	
def article(request, id):
	usergroup = get_usergroup(request)
	try:
		article = ArticleModel.objects.get(id=id)
		Keywords = KeywordModel.objects.all()
		Authors = article.author.all()
		if article.release_date == None:
			if usergroup=='Authors':
				user = User.objects.get(username=request.user)
				AuthorsArray = []
				for author in Authors:
					AuthorsArray.append(author)
				if AuthorModel.objects.get(login=user) in AuthorsArray:
					return render_to_response('article.html', {'article': article, 'Keywords': Keywords, 'Authors': Authors, 'usergroup': usergroup})
				else:
					return redirect("articles")
			else:
				return redirect("articles")
		else:
			return render_to_response('article.html', {'article': article, 'Keywords': Keywords, 'Authors': Authors, 'usergroup': usergroup})
	except:
		return redirect("articles")

def release(request, index):
	usergroup = get_usergroup(request)
	permission = False
	try:
		release = ReleaseModel.objects.get(id=index)
		Articles = ArticleModel.objects.filter(release=release)
		Keywords = KeywordModel.objects.all()
		if release.release_date == None:
			if usergroup == 'Editors':
				user = User.objects.get(username=request.user)
				if release.editor == EditorModel.objects.get(login=user):
					if  ArticleModel.objects.filter(release=release).count() > 0:
						permission = True
					return render_to_response('release.html', {'release': release, 'usergroup': usergroup, 'Articles': Articles, 'Keywords': Keywords, 'index': index, 'permission': permission})
				else:
					return redirect("releases")
			else:
				return redirect("releases")
		else:
			return render_to_response('release.html', {'release': release, 'usergroup': usergroup, 'Articles': Articles, 'Keywords': Keywords, 'index': index, 'permission': permission})
	except:
		return redirect("releases")