from django.conf.urls import url

from asignacionHistorias import views

urlpatterns = [
 
    url(r'^uniquecostassign/', views.AssignmentUniqueCostView.as_view(),  name='uniquecostassign'),
    url(r'^attributeassign/', views.AssignmentWithAttributesView.as_view(), name='attributeassign'),
    url(r'^groupassign/', views.AssignmentWithGroupsView.as_view(), name='groupassign'),
    url(r'^pairassign/', views.AssignmentByPairs.as_view(), name='pairassign'),
    url(r'^makepairs/', views.GeneratePairs.as_view(), name='makepairs'),
    url(r'^agent/default_id', views.DefaultAgentId.as_view(), name='agent_default_id')

]
