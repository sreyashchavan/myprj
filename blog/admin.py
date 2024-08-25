from django.contrib import admin
from .models import Post,Tag,Author,Comments


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_filter=("title","author","tags",)
    list_display=("title","date","author",)
    prepopulated_fields={"slug":("title",)}
    
class CommentsAdmin(admin.ModelAdmin):
    list_display=("user_name","post")
    

admin.site.register(Post,PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comments,CommentsAdmin)



