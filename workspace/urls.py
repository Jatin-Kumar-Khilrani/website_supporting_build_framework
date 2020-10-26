from django.conf.urls import url
import views

urlpatterns = [
    url(r'^index/$', views.Workspace.as_view(), name='ws_index'),
    
    url(r'^add_release/$', views.ManageRelease.as_view(), name='ManageRelease'),
    
    url(r'^add_release/(?P<op>\w+)/$', views.ManageRelease.as_view(), name='ManageRelease'),

    url(r'^add_pid/$', views.add_pid, name='add_pid'),

    url(r'^add_common_tool/$', views.add_common_tool, name='add_common_tool'),
    
    url(r'^add_ws/$', views.add_workspace, name='add_workspace'), 
    
    url(r'^create_iso/$', views.create_iso, name='create_iso'),
    
    url(r'^get_log/$', views.get_log, name='get_log'),
    
    url(r'^get_iso_status/$', views.get_iso_status, name='get_iso_status'),
    
    url(r'^r_c/(?P<ws_name>\w+)/(?P<release>\w+)/$', views.redirect_to_components, name='redirect_to_components'),
    
    url(r'^delete_ws/$', views.delete_ws, name='delete_ws'),

    url(r'^move_ws/$', views.move_ws, name='move_ws'),
    
    url(r'^download_iso/$', views.download_iso, name='download_iso'),

    #url(r'^sanityqueue_iso/$', views.sanityqueue_iso, name='sanityqueue'),

    url(r'^download_catalog/$',views.downloadjson, name='download_catalog'),
]
