from django.conf.urls import url

from asignacionHistorias import views

urlpatterns = [
 
    url(r'^uniquecostassign/', views.AssignmentUniqueCostView.as_view(),  name='uniquecostassign'),
    url(r'^attributeassign/', views.AssignmentWithAttributesView.as_view(), name='attributeassign'),
    url(r'^groupassign/', views.AssignmentWithGroupsView.as_view(), name='groupassign'),
    url(r'^pairassign/', views.AssignmentByPairs.as_view(), name='pairassign')

]
