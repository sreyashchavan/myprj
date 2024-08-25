from django.db import models
from django.core.validators import MinLengthValidator,MaxLengthValidator

# Create your models here.

class Tag(models.Model):
    caption=models.CharField(max_length=20)
    
    def __str__(self):
        return self.caption
    
class Author(models.Model):
    first_name=models.CharField(max_length=15)
    last_name=models.CharField(max_length=15)
    email=models.EmailField()
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.full_name()
    
class Post(models.Model):
    title=models.CharField(max_length=150)
    excerpt=models.CharField(max_length=250,null=True)
    image= models.ImageField(upload_to="posts",null=True)
    date=models.DateField(auto_now=True)
    slug=models.SlugField(unique=True)
    content=models.TextField(validators=[MinLengthValidator(10)],null=True)
    author=models.ForeignKey(Author,on_delete=models.SET_NULL,null=True,related_name="posts")
    tags=models.ManyToManyField(Tag)
    
    def __str__(self):
        return f"{self.title}"
    
class Comments(models.Model):
    user_name=models.CharField(max_length=100)
    text=models.TextField(max_length=400)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    
    class Meta:
        verbose_name_plural="Comments"
    
# class Register(models.Model):
#     user_name=models.CharField(max_length=20)
#     email_id=models.EmailField()
#     password_1=models.CharField(max_length=8,validators=[MaxLengthValidator(8),MinLengthValidator(8)])
#     password_2=models.CharField(max_length=8,validators=[MaxLengthValidator(8),MinLengthValidator(8)])
    
#     def __str__(self):
#         return f"{self.user_name}"

