from django.urls import path
from .import views as reg_views
from django.contrib.auth import views as auth_views
from .views import ProfileListView,profileDetailView

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name='users/login.html'), name="login"), #login page
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),  #logout -->redirect to login page
    path('result/',reg_views.search,name='search'), #search Q 

    path("register/", reg_views.register, name="register"), #register page
    path("profile/", reg_views.profile, name="profile"), #my profile
    path("invites/", reg_views.invitesReceivedViews, name="invites"), #request sent by others

    path("profile/list/", ProfileListView.as_view() , name="profileList"),#All of the profiles list we can see
    path("profile/<int:pk>/detail/", profileDetailView.as_view(), name="profileDetail"), #individual profile of choice

    path("profile/invites/sent/", reg_views.send_invitation, name="sendInvite"), #sending friend request no template
    path("profile/invites/remove/", reg_views.remove_from_friends, name="removeFriends"), #Removing form friends no template
    path("profile/invites/accept/", reg_views.accept_invite, name="acceptInvites"), #Accepting the request no template
    path("profile/invites/reject/", reg_views.reject_invite, name="rejectInvites"), #deleting the request no template

]
