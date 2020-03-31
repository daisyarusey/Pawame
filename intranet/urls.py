from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('',views.updates,name='updates'),
    path('login/',views.logins, name='login'),
    path('notifications/',views.notifications, name='notifications'),
    path('employees/',views.employees, name='employees'),
    path('inventory/',views.inventory, name='inventory'),
    path('finance/',views.finance, name='finance'),
    path('marketing/',views.marketing, name='marketing'),
    path('information/',views.information_technology, name='information'),
    path('employeeProfile/',views.employeeProfile, name='employeeProfile'),
    path('editProfile/',views.editProfile, name='editProfile'),
    path('updateProfilePic/',views.updateProfilePic, name='updateProfilePic'),    
    path('human_resource/',views.human_resource,name='human_resource'),
    path('postUpdate/',views.postUpdate,name='postUpdate'),
    path('searchResults/',views.searchResults,name='searchResults'),
    path('comments/<int:update_id>',views.comments,name='comments'),
    path('commenting/<int:update_id>',views.commenting,name='commenting'),
    path('approve/<int:id>', views.approved, name='approve'),
    path('disapprove/<int:id>', views.disapproved, name='disapprove'),
    path('delete_employee/<int:id>',views.delete_employee, name='delete_employee')


]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
