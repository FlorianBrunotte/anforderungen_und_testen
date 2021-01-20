from django.urls import path, include, re_path
from django.views.generic import RedirectView

from . import views

#Name der App
app_name = 'aut'
urlpatterns = [
    #Basis Views
    path('', views.view_dashboard, name='view_dashboard'),
    path('requirement', views.view_requirement, name='view_requirement'),
    path('testcase', views.view_testcase, name='view_testcase'),
    path('testrun', views.view_testrun, name='view_testrun'),
    path('statistik', views.view_statistik, name='view_statistik'),

    #Requirement Views für die Forms
    path('requirement/<int:pk>/', views.edit_requirement, name='requirement_change'),
    path('requirement/create/', views.edit_requirement, name='requirement_create'),
    path('requirement/create/<int:pk>/', views.edit_requirement, name='requirement_create'),

    #TestCase Views für die Forms
    path('testcase/<int:pk>/', views.edit_testcase, name='testcase_change'),
    path('testcase/create/', views.edit_testcase, name='testcase_create'),
    path('testcase/create/<int:pk>/', views.edit_testcase, name='testcase_create'),

    #TestRun Views für die Forms
    path('testrun/<int:pk>/', views.edit_testrun, name='testrun_change'),
    path('testrun/create', views.edit_testrun, name='testrun_create'),
    path('testrun/create/<int:pk>/', views.edit_testrun, name='testrun_create'),

    path('testrun/run/<int:pk>/', views.testrun_run, name='testrun_run'),

    #Zur Beschreibung der Elemente
    path('req_desc', views.req_desc, name='req_desc'),
    path('testc_desc', views.testc_desc, name='testc_desc'),
    path('testr_desc', views.testr_desc, name='testr_desc'),

    #Views für die TestCase Schritte
    path('schritte/<int:id>', views.formset_view, name='schritte'),
    path('schritte_run/<int:id>', views.formset_view_run, name='schritte_run'),

    #Notepad für Notizen
    path('note/', views.form_note, name='notepad'),
    path('note/<int:pk>/', views.form_note, name='notepad'),

    path('test2', views.TestDocument, name='test2'),

]

