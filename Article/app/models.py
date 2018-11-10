from django.db import models
from django.contrib.auth.models import User

# Create your models here.
LANGUAGE = (("Русский","Русский"),("English","English"))
TITLE = (("нет","нет"),("научный сотрудник","научный сотрудник"),("ассистент","ассистент"),("доцент","доцент"),("профессор","профессор"))
DEGREE = (("нет","нет"),("кандидат наук","кандидат наук"),("доктор наук","доктор наук"))

class EditorModel (models.Model):
	class Meta:
		verbose_name = "Editor" #название таблицы в ед.ч
		verbose_name_plural = "Editors" #название таблицы в мн.ч
	name_magazine = models.CharField(max_length = 150, verbose_name = "Название журнала", unique = True)
	login = models.OneToOneField(User)
	name = models.CharField(max_length = 150, verbose_name = "ФИО редактора")
	birth_date = models.DateField(verbose_name = "Дата рождения")
	degree = models.CharField(max_length = 35, verbose_name = "Ученая степень", choices=DEGREE)
	title = models.CharField(max_length = 35, verbose_name = "Ученое звание", choices=TITLE)
	work = models.CharField(max_length = 70, verbose_name = "Место работы", null=True)
	position = models.CharField(max_length = 70, verbose_name = "Должность", null=True)
	email = models.EmailField(verbose_name = "Email", unique=True)
	education = models.CharField(max_length = 70, verbose_name = "Образование")
	def __str__(self):
		return "(%s) %s" % (self.name, self.name_magazine)

class AuthorModel(models.Model):
	class Meta:
		verbose_name = "Author" #название таблицы в ед.ч
		verbose_name_plural = "Authors" #название таблицы в мн.ч
	index =  models.CharField(max_length = 10, verbose_name = "index", unique = True)
	login = models.OneToOneField(User)
	name = models.CharField(max_length = 150, verbose_name = "ФИО автора")
	birth_date = models.DateField(verbose_name = "Дата рождения")
	degree = models.CharField(max_length = 35, verbose_name = "Ученая степень", choices=DEGREE, null = True)
	title = models.CharField(max_length = 35, verbose_name = "Ученое звание", choices=TITLE, null = True)
	work = models.CharField(max_length = 70, verbose_name = "Место работы", null = True)
	position = models.CharField(max_length = 70, verbose_name = "Должность", null = True)
	email = models.EmailField(verbose_name = "Email")
	education = models.CharField(max_length = 70, verbose_name = "Образование", null = True)
	def __str__(self):
		return "(%s) %s" % (self.name, self.work)	

class ReleaseModel(models.Model):
	class Meta:
		ordering = ["name_magazine","number_release"] #поля, по которым будет производиться сортировка
		verbose_name = "Release" #название таблицы в ед.ч
		verbose_name_plural = "Releases" #название таблицы в мн.ч
	ISSN = models.CharField(max_length = 35, verbose_name = "ISSN", unique = True)
	release_date = models.DateField(verbose_name = "Дата выхода", null = True)
	name_magazine = models.CharField(max_length = 150, verbose_name = "Название журнала", null = True)
	name_editor = models.CharField(max_length = 150, verbose_name = "ФИО редактора", null = True)
	name_publisher = models.CharField(max_length = 150, verbose_name = "Название издательства")
	number_release = models.PositiveSmallIntegerField(verbose_name = "Номер выпуска", null = True)
	editor = models.ForeignKey(EditorModel, null = True)
	def __str__(self):
		return "(%s) %s" % (self.name_magazine, self.number_release)
		
class ArticleModel(models.Model):
	class Meta:
		ordering = ["release_date", "name"] #поля, по которым будет производиться сортировка
		verbose_name = "Article" #название таблицы в ед.ч
		verbose_name_plural = "Articles" #название таблицы в мн.ч
	DOI = models.CharField(max_length = 35, verbose_name = "DOI", unique = True)
	name = models.CharField(max_length = 150, verbose_name = "Название статьи")
	cost = models.PositiveSmallIntegerField(verbose_name = "Стоимость статьи", null=True)
	release_date = models.DateField(verbose_name = "Дата выхода", null = True)
	number_release = models.PositiveSmallIntegerField(verbose_name = "Номер выпуска", null=True)
	UDC = models.CharField(max_length = 35, verbose_name = "УДК")
	name_magazine = models.CharField(max_length = 150, verbose_name = "Название журнала", null = True)
	name_publisher = models.CharField(max_length = 150, verbose_name = "Название издательства", null = True)
	ISSN = models.CharField(max_length = 35, verbose_name = "ISSN", null = True)
	language = models.CharField(max_length = 35, verbose_name = "Язык", choices = LANGUAGE)
	description = models.TextField(verbose_name = "Аннотация")
	text = models.TextField(verbose_name = "Текст")
	author = models.ManyToManyField(AuthorModel, verbose_name = "Авторы")
	release = models.ForeignKey(ReleaseModel, verbose_name = "Выпуск", null = True)
	def __str__(self):
		return "(%s) %s" % (self.name, self.name_magazine)
	
class KeywordModel(models.Model):
	class Meta:
		verbose_name = "Keyword" #название таблицы в ед.ч
		verbose_name_plural = "Keywords" #название таблицы в мн.ч
	name = models.CharField(max_length = 35, verbose_name = "Ключевое слово", help_text = "Заполнить ключевое слово")
	article = models.ForeignKey(ArticleModel)
	
class FileModel(models.Model):
	file = models.FileField(upload_to="app/static/")