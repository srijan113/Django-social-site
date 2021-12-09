from django.db import models
from users.models import Profile
from PIL import Image
from django.core.validators import FileExtensionValidator
# Create your models here.


class Post(models.Model):
    content=models.TextField()
    image=models.ImageField(upload_to='post_pics', validators=[FileExtensionValidator(['png','jpg','jpeg'])],blank=True)
    liked=models.ManyToManyField(Profile, blank=True,related_name='likes')
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    author=models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='posts')


    def __str__(self):
        return str(self.content[:20])
    

    def number_likes(self):
        return self.liked.all().count()


    def number_comment(self):
        return self.comment.all().count()  #if related_name is not provided in the field like in comment model then we can user 'modelname_set' to grab the data for the singular data.


    class Meta:
        ordering=['-created']


    #this below method will make your posts image into 300*300 (You can change its size as necessary), use this method to reduce the size of the picture uploaded.
    """def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

        img=Image.open(self.image.path)
        if img.height>300 or img.width>300:
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)"""
    

class Comment(models.Model):
    user=models.ForeignKey(Profile, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comment')
    body=models.TextField(max_length=500)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.pk)



LIKE_CHOICES=(
        ('Like','Like'),
        ('Unlike','Unlike')
    )

class Like(models.Model):
    user=models.ForeignKey(Profile, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    value=models.CharField(max_length=50,choices=LIKE_CHOICES)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}-->{self.post}-->{self.value}"
    
