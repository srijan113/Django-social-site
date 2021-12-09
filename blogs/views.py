from django.shortcuts import render,redirect
from .models import Post,Like
from users.models import Profile
from .forms import PostCreationForm,CommentModelForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView,DeleteView
# Create your views here.
@login_required
def home(request):
    user=request.user
    posts=Post.objects.all()
    profile=Profile.objects.get(user=request.user)

    p_form=PostCreationForm()
    c_form=CommentModelForm()



    if 'post_button' in request.POST:
        p_form=PostCreationForm(request.POST,request.FILES)
        if p_form.is_valid():
            instance=p_form.save(commit=False)
            instance.author=profile
            instance.save()
            messages.success(request,f'New post has been added')
            p_form=PostCreationForm()


    if 'comment_button' in request.POST:
        c_form=CommentModelForm(request.POST or None)
        if c_form.is_valid():
            instance=c_form.save(commit=False)
            instance.user=profile
            instance.post=Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form=CommentModelForm()

    context={
        'posts':posts,
        'profile':profile,
        'p_form':p_form,
        'c_form':c_form

    }
    return render(request,'blogs/home.html',context)


def likeUnlikePost(request):
    now_users=request.user
    if request.method=="POST":
        post_id=request.POST.get('post_id')
        post_obj=Post.objects.get(id=post_id)
        profile=Profile.objects.get(user=now_users)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like,created=Like.objects.get_or_create(user=profile,post_id=post_id)

        if not created:
            if like.value=='Like':
                like.value='Unlike'
            else:
                like.value='Like'
        else:
            like.value='Like'

            post_obj.save()
            like.save()

    return redirect(request.META.get('HTTP_REFERER'))



class PostDeleteView(DeleteView):
    model=Post
    template_name='blogs/delete.html'
    success_url='/'

    def get_object(self, *args,**kwargs):
        pk=self.kwargs.get('pk')
        post=Post.objects.get(pk=pk)
        if not post.author.user==self.request.user:
            messages.warning(self.request,f'You need to be the post author to update the post.')
        return post


class PostUpdateView(UpdateView):
    form_class=PostCreationForm
    model=Post
    template_name='blogs/update.html'
    success_url='/'

    def form_valid(self, form):
        profile=Profile.objects.get(user=self.request.user)
        if form.instance.author==profile:
            return super().form_valid(form)
        else:
            form.add_error(None,'You need to be the post author to delete the post.')
            return super().form_invalid(form)


