from squadBlog import views
from django.urls import path

try:
    urlpatterns = [
        path('all_categories',views.ShowAllCategories.as_view(),name='categories'),
        path('<category>',views.ShowPostsCategory,name='category'),
        path('post/<slug>', views.PostDetailView.as_view(), name='post-detail'),
        path('create_comment/<slug>', views.comment_create_view,name='create-comment'),
        path('comment_list/<slug>',views.comment_list,name='comment-list'),
        path('show_post_random/<category>',views.showPost_instance,name='show-post-random'),#phase2.6
        path('disengage_post/<int:id>/<category>',views.disengage_post,name='disengage-post'),#phase3.3 #add category to url
        path('disengage_post_validate/<int:id>',views.disengage_post_validate,name='disengage-post-validate'),#phase2.6
        path('post_has_answer_by_random/',views.post_has_answer_random,name='post-has-answer-random'),#phase2.6
        path('validate_comments_of_specific_post/<int:id>',views.validate_comments_of_specific_post,name='validate-comments-of-specific-post'),#phase2.6
        path('comment_list_validated/<slug>',views.comment_list_validated,name='comment-list'),#phase2.6
        path('disengage_post_finish/<int:id>',views.disengage_post_finish,name='disengage-post-finish'),#phase3.4
        path('unblocker_post/',views.unblocker_post,name='unblocker-post'),#phase3.4
    ] 
except:
    urlpatterns=[] 