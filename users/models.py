from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models import Q
# Create your models here.


class ProfileManager(models.Manager):
    def get_all_profile_to_invites(self,sender):
        profiles=Profile.objects.all().exclude(user=sender)
        profile=Profile.objects.get(user=sender)
        qs=Relationship.objects.filter(Q(sender=profile)|Q(receiver=profile))

        accepted=set([])
        for rel in qs:
            if rel.status == 'accepted':
                accepted.add(rel.receiver)
                accepted.add(rel.sender)
        avaliable=[profile for profile in profiles if profile not in accepted]
        return avaliable


    def get_all_profile(self,me):
        profiles=Profile.objects.all().exclude(user=me)
        return profiles



class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    bio=models.TextField(max_length=500,default='This user has no bio..')
    email=models.EmailField(max_length=254,blank=True)
    country=models.CharField(max_length=50,blank=True)
    image=models.ImageField(upload_to='profile_pic',default='default.png')
    friends=models.ManyToManyField(User,blank=True,related_name='friends')
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)


    objects=ProfileManager()

    def __str__(self):
        return f"{self.user.username}"

    def get_friends(self):
        return self.friends.all()

    def get_posts_number(self):
        return self.posts.all().count()

    def get_all_auth_post(self):
        return self.posts.all()

    def likes_given(self):
        like=self.like_set.all()
        total_likes=0
        for item in like:
            if item.value=="Like":
                total_likes+=1
        return total_likes
    

    def likes_received(self):
        posts=self.posts.all()
        total_likes=0
        for item in posts:
            total_likes+=item.liked.all().count()
        return total_likes



    def get_friends_number(self):
        return self.friends.all().count()


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

        img=Image.open(self.image.path)
        if img.height>300 or img.width>300:
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)



class ManagerRelationship(models.Manager):
    def invite_receiver(self,receiver):
        invite=Relationship.objects.filter(receiver=receiver,status='send')
        return invite




class Relationship(models.Model):
    STATUS_CHOICES=(
        ('send','send'),
        ('accepted','accepted')
    )
    sender=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver=models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='receiver')
    status=models.CharField(max_length=10,choices=STATUS_CHOICES)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    objects=ManagerRelationship()

    def __str__(self):
        return f"{self.sender}-->{self.receiver}-->{self.status}."
