from django import forms
from app.models import ArticleModel, AuthorModel, ReleaseModel, EditorModel, FileModel

TITLE = (("нет","нет"),("научный сотрудник","научный сотрудник"),("ассистент","ассистент"),("доцент","доцент"),("профессор","профессор"))
DEGREE = (("нет","нет"),("кандидат наук","кандидат наук"),("доктор наук","доктор наук"))

class ArticleModelForm(forms.ModelForm):
	class Meta:
		model = ArticleModel
		fields = ['name', 'UDC', 'author', 'name_magazine', 'language', 'description', 'text', 'keywords']
		widgets = {"name": forms.Textarea(attrs = {"rows": 5, "cols": 45}) ,"description": forms.Textarea(attrs = {"rows": 20, "cols": 50}),
			"text": forms.Textarea(attrs = {"rows": 50, "cols": 55}), "name_magazine": forms.Textarea(attrs = {"rows": 3, "cols": 44})}
	keywords = forms.CharField(widget = forms.Textarea(attrs = {"rows": 5, "cols": 45}), label = "Ключевые слова", initial = "Пример, заполнения, ключевых слов")
	
class ArticleEditModelForm(forms.ModelForm):
	class Meta:
		model = ArticleModel
		fields = ['name', 'cost', 'release', 'UDC', 'language', 'description', 'text', 'keywords']
		widgets = {"name": forms.Textarea(attrs = {"rows": 5, "cols": 45}) ,"description": forms.Textarea(attrs = {"rows": 20, "cols": 50}),
			"text": forms.Textarea(attrs = {"rows": 50, "cols": 55}), "name_magazine": forms.Textarea(attrs = {"rows": 3, "cols": 44}), "name_publisher": forms.Textarea(attrs = {"rows": 3, "cols": 30})}
	keywords = forms.CharField(widget = forms.Textarea(attrs = {"rows": 5, "cols": 45}), label = "Ключевые слова", initial = "Пример, заполнения, ключевых слов")
	
class ReleaseModelForm(forms.ModelForm):
	class Meta:
		model = ReleaseModel
		fields = ['name_publisher']
		widgets = {"name_publisher": forms.Textarea(attrs = {"rows": 3, "cols": 30})}
	
class AuthorModelForm(forms.Form):
	class Meta:
		fields = ['login', 'password', 'name', 'birth_date', 'degree', 'title', 'work', 'position', 'email', 'education']
	login = forms.CharField(widget = forms.TextInput(attrs = {"size": 20}), label = "Логин", help_text = "Пример: Ivan")
	password = forms.CharField(widget = forms.PasswordInput(attrs = {"size": 20}), label = "Пароль", help_text = "Пример: Ivan87654321")
	name = forms.CharField(widget = forms.TextInput(attrs = {"size": 30}), label = "ФИО", help_text = "Пример: Иванов Иван Сергеевич")
	birth_date = forms.CharField(widget = forms.DateInput(attrs = {"size": 15}), label = "Дата рождения", help_text = "Пример: 1975-05-16")
	degree = forms.ChoiceField(choices=DEGREE, label = "Ученая степень")
	title = forms.ChoiceField(choices=TITLE, label = "Ученое звание")
	work = forms.CharField(widget = forms.TextInput(attrs = {"size": 20}), label = "Работа", help_text = "Пример: КНИТУ-КАИ им. Туполева")
	position = forms.CharField(widget = forms.TextInput(attrs = {"size": 20}), label = "Должность", help_text = "Пример: Доцент")
	email = forms.CharField(widget = forms.EmailInput(attrs = {"size": 20}), label = "Email", help_text = "Пример: ivan@article.com")
	education = forms.CharField(widget = forms.TextInput(attrs = {"size": 20}), label = "Образование", help_text = "Пример: КНИТУ-КАИ им. Туполева")

class EditorModelForm(forms.Form):
	class Meta:
		fields = ['login', 'password', 'name', 'birth_date', 'degree', 'title', 'work', 'position', 'email', 'education']
	login = forms.CharField(widget = forms.TextInput(attrs = {"size": 20}), label = "Логин", help_text = "Пример: Ivan")
	password = forms.CharField(widget = forms.PasswordInput(attrs = {"size": 20}), label = "Пароль", help_text = "Пример: Ivan87654321")
	name = forms.CharField(widget = forms.TextInput(attrs = {"size": 30}), label = "ФИО", help_text = "Пример: Иванов Иван Сергеевич")
	birth_date = forms.CharField(widget = forms.DateInput(attrs = {"size": 15}), label = "Дата рождения", help_text = "Пример: 1975-05-16")
	name_magazine = forms.CharField(widget = forms.Textarea(attrs = {"rows": 3, "cols": 30}), label = "Название журнала", help_text = "Пример: Информатика")
	degree = forms.ChoiceField(choices=DEGREE, label = "Ученая степень")
	title = forms.ChoiceField(choices=TITLE, label = "Ученое звание")
	work = forms.CharField(widget = forms.TextInput(attrs = {"size": 20}), label = "Работа", help_text = "Пример: КНИТУ-КАИ им. Туполева")
	position = forms.CharField(widget = forms.TextInput(attrs = {"size": 20}), label = "Должность", help_text = "Пример: Доцент")
	email = forms.CharField(widget = forms.EmailInput(attrs = {"size": 20}), label = "Email", help_text = "Пример: ivan@article.com")
	education = forms.CharField(widget = forms.TextInput(attrs = {"size": 20}), label = "Образование", help_text = "Пример: КНИТУ-КАИ им. Туполева")
	
class LoginForm(forms.Form):
	username = forms.CharField(label = "Имя")
	password = forms.CharField(widget = forms.PasswordInput, label = "Пароль")
	
class UploadFileForm(forms.Form):
	class Meta:
		model = FileModel
		fields = ['file']