from squadBlog import views
from django.urls import path,include

urlpatterns = [
    path('all_categories/',views.ShowAllCategories.as_view(),name='categories'),
    path('<category>/',views.ShowPostsCategory,name='category'),
    path('post/<slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('create_comment/<slug>/', views.comment_create_view,name='create-comment'),
    path('comment_list/<slug>/',views.comment_list,name='comment-list'),
]
