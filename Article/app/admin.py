from django.contrib import admin
from app.models import EditorModel, ArticleModel, AuthorModel, KeywordModel, ReleaseModel, FileModel

# Register your models here.

class EditorModelAdmin(admin.ModelAdmin):
	list_display = ('name_magazine', 'name', 'birth_date', 'degree', 'title', 'work', 'position', 'email', 'education')
	search_fields = ('name_magazine', 'name', 'birth_date', 'degree', 'title', 'work', 'position', 'email', 'education')

class ArticleModelAdmin(admin.ModelAdmin):
	list_display = ('DOI', 'name', 'cost', 'release_date', 'number_release', 'UDC', 'name_magazine', 'name_publisher', 'ISSN', 'language', 'description', 'text', 'release')
	search_fields = ('name', 'cost', 'release_date', 'UDC', 'name_magazine', 'name_publisher', 'language', 'release')

class AuthorModelAdmin(admin.ModelAdmin):
	list_display = ('index', 'name', 'birth_date', 'degree', 'title', 'work', 'position', 'email', 'education')
	search_fields = ('name', 'birth_date', 'degree', 'title', 'work', 'position', 'email', 'education')

class KeywordModelAdmin(admin.ModelAdmin):
	list_display = ('name', 'article')
	search_fields = ('name', 'article')
	
class ReleaseModelAdmin(admin.ModelAdmin):
	list_display = ('ISSN', 'name_magazine', 'name_editor', 'name_publisher', 'number_release')
	search_fields = ('name_magazine', 'name_editor', 'name_publisher', 'number_release')
	
class FileModelAdmin(admin.ModelAdmin):
	list_display = ('file',)

admin.site.register(EditorModel, EditorModelAdmin)	
admin.site.register(ArticleModel, ArticleModelAdmin)
admin.site.register(AuthorModel, AuthorModelAdmin)
admin.site.register(KeywordModel, KeywordModelAdmin)
admin.site.register(ReleaseModel, ReleaseModelAdmin)
admin.site.register(FileModel, FileModelAdmin)