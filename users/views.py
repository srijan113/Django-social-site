from django.shortcuts import render,redirect,get_object_or_404
from .forms import UserRegisterForm,ProfileUpdateForm
from django.contrib import messages
from .models import Profile,Relationship
from django.contrib.auth.models import User
from django.views.generic import ListView,DetailView
from django.db.models import Q
# Create your views here.


def register(request):
    if request.method=="POST":
        r_form=UserRegisterForm(request.POST)
        if r_form.is_valid():
            r_form.save()
            username=r_form.cleaned_data.get('username')
            messages.success(request,f'You can now login {username}.')
            return redirect('/')
        else:
            messages.error(request,f'Please enter the fields properly')
            return redirect('register')
    else:
        r_form=UserRegisterForm()

    return render(request,'users/register.html',{'r_form':r_form})



def profile(request):
    pro=Profile.objects.get(user=request.user)
    if request.method=="POST":
        p_form=ProfileUpdateForm(request.POST or None,request.FILES or None,instance=pro)
        if p_form.is_valid():
            p_form.save()
            messages.success(request,f'You have updated your profile.')
            return redirect('profile')
        else:
            messages.error(request,f'Please enter all fields propely.')
            return redirect('profile')
    else:
        p_form=ProfileUpdateForm(instance=pro)
    context={
        'pro':pro,
        'p_form':p_form
    }
    return render(request,'users/profile.html',context)




def invitesReceivedViews(request):
    pro=Profile.objects.get(user=request.user)
    invites=Relationship.objects.invite_receiver(pro)
    results=list(map(lambda x: x.sender,invites))
    is_empty=False
    if len(results)==0:
        is_empty=True
    context={
        'invites':results,
        'is_empty':is_empty
    }
    return render(request,'users/invites.html',context)


def accept_invite(request):
    if request.method=="POST":
        pk=request.POST.get('profile_id')
        sender=Profile.objects.get(pk=pk)
        receiver=Profile.objects.get(user=request.user)
        rel=get_object_or_404(Relationship,sender=sender,receiver=receiver)
        if rel.status=='send':
            rel.status='accepted'
            rel.save()

    return redirect(request.META.get('HTTP_REFERER'))


def reject_invite(request):
    if request.method=="POST":
        pk=request.POST.get('profile_id')
        sender=Profile.objects.get(pk=pk)
        receiver=Profile.objects.get(user=request.user)
        rel=get_object_or_404(Relationship,sender=sender,receiver=receiver)
        rel.delete()

    return redirect(request.META.get('HTTP_REFERER'))




class ProfileListView(ListView):
    model=Profile
    template_name='users/profile_list.html'
    context_object_name='qs'

    def get_queryset(self):
        qs=Profile.objects.get_all_profile(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=User.objects.get(username__iexact=self.request.user)
        profile=Profile.objects.get(user=user)
        # context['profile']=profile
        rel_r=Relationship.objects.filter(sender=profile)
        rel_s=Relationship.objects.filter(receiver=profile)
        rel_receiver=[]
        rel_sender=[]
        for i in rel_r:
            rel_receiver.append(i.receiver.user)
        for i in rel_s:
            rel_sender.append(i.sender.user)

        context['rel_receiver']=rel_receiver
        context['rel_sender']=rel_sender

        context['is_empty']=False
        if len(self.get_queryset())==0:
            context['is_empty']=True
        return context
    

class profileDetailView(DetailView):
    model=Profile
    template_name='users/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=User.objects.get(username__iexact=self.request.user)
        profile=Profile.objects.get(user=user)
        # context['profile']=profile
        rel_r=Relationship.objects.filter(sender=profile)
        rel_s=Relationship.objects.filter(receiver=profile)
        rel_receiver=[]
        rel_sender=[]
        for i in rel_r:
            rel_receiver.append(i.receiver.user)
        for i in rel_s:
            rel_sender.append(i.sender.user)

        context['rel_receiver']=rel_receiver
        context['rel_sender']=rel_sender
        context['posts']=self.get_object().get_all_auth_post()
        context['len_post']=True if self.get_object().get_posts_number() > 0 else False
        return context



def send_invitation(request):
    if request.method =="POST":
        pk=request.POST.get('profile_id')
        user=request.user
        sender=Profile.objects.get(user=user)
        receiver=Profile.objects.get(pk=pk)
        rel=Relationship.objects.create(sender=sender,receiver=receiver,status='send')

        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('profile')



def remove_from_friends(request):
    if request.method=="POST":
        pk=request.POST.get('profile_id')
        user=request.user
        sender=Profile.objects.get(user=user) #this is us we want  to remove a profile
        receiver=Profile.objects.get(pk=pk)  #this is the other profile which profile we want to remove

        rel=Relationship.objects.get((Q(sender=sender)&Q(receiver=receiver))|(Q(sender=receiver)&Q(receiver=sender)))
        rel.delete()

        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('profile')

         


def search(request):
    query=request.GET.get('q')
    result=User.objects.filter(
        Q(username__icontains=query) | 
        Q(first_name__icontains=query) | 
        Q(last_name__icontains=query)
        )

    context={
        'result':result,
        'query':query
    }
    return render(request,'users/search.html',context)
