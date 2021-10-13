from mohavereh import views
from django.urls import path

try:
    urlpatterns = [
        path('informal_text', views.showInformalText, name='informal-text-list'),
        path('informal_text/<slug>', views.InformalTextDetailView.as_view(), name='informal-text-detail'),
        path('create_formal_text/<slug>', views.formal_text_create_view,name='create-formal-text'),
        path('formal_text/<slug>',views.formal_text,name='formal-text-show'),
        path('informal_text_has_answer_list', views.InformalTextHasAnswerList.as_view(), name='informal-text-has-answer-list'),
        path('validate_formal_text/<slug>',views.validate_formal_text,name='validate-formal-text'),
        path('show_informal_text_random',views.showInformalText_instance,name='show-informal-text-random'),#phase2.6
        path('disengage_informaltext/<int:id>',views.disengage_informaltext,name='disengage-informal-text'),#phase2.6
        path('informal_text_has_answer_random', views.informal_text_has_answer, name='informal-text-has-answer-random'),#phase2.6
        path('disengage_informaltext_validate/<int:id>',views.disengage_informaltext_validate,name='disengage-informal-text-validate'),#phase2.6
        path('disengage_informaltext_finish/<int:id>',views.disengage_informal_text_finish,name='disengage-informal-text-finish'),#phase3.4
        path('unblocker_informaltext/',views.unblocker_informaltext,name='unblocker-informaltext'),#phase3.4
    ]
except:
    urlpatterns=[]     