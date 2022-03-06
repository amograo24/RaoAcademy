from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("upload_notes",views.upload_notes,name="upload_notes"),
    path("notes/<int:id>",views.note_view,name="note_view"),
    path("<str:lecturer>/<str:course>",views.course_view,name="course_view"), 
    path("lecturer/<str:username>/courses",views.profile_view,name="profile"),
    path("apis/follow_unfollow/<str:username>",views.follow_unfollow,name="follow_unfollow"),
    path("apis/subscribe_unsubscribe/<int:id>",views.subscribe_unsubscribe,name="subscribe_unsubscribe"),
    path("apis/like_unlike/<int:id>",views.like_unlike,name="like_unlike"),
    path("apis/edit_note/<int:id>",views.edit_note,name="edit_note"),
    path("apis/delete_note/<int:id>",views.delete_note,name="delete_note"),
    path("apis/edit_course/<str:lecturer>/<str:course>",views.edit_course,name="edit_course"),
    path("apis/delete_course/<str:lecturer>/<str:course>",views.delete_course,name="delete_course"),    
    path("apis/post_comment/<int:id>",views.post_comment,name="post_comment"),
    path("apis/notes/comments/<int:id>",views.comments,name="comments"),
    path("create_course",views.create_course,name="create_course"),
    path("subscribed",views.subscribed_courses,name="subscribed_courses"),
    path("following",views.following_lecturer_courses,name="f_l_c"),
    path("search",views.search,name="search"),
    path("categories",views.category_list,name="categories"),
    path("category/<str:category_name>/courses",views.category_view,name="category"),
]