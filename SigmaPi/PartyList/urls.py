from django.conf.urls import url
from django.views.generic import RedirectView

from . import views, api

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='partylist-index'), name='partylist-index-old'),
    url(r'^all/$', views.index, name='partylist-index'),
    url(r'^add/$', views.add_party, name='partylist-add_party'),
    url(r'^blacklist/$', views.view_blacklist, name='partylist-view_blacklist'),
    url(r'^blacklist/manage/$', views.manage_blacklist, name='partylist-manage_blacklist'),
    url(r'^blacklist/manage/remove/(?P<bl_id>[\d]+)/$', views.remove_blacklisting, name='partylist-remove_blacklisting'),
    url(r'^manage/$', views.manage_parties, name='partylist-manage_parties'),
    url(r'^edit/(?P<party>[\d]+)/$', views.edit_party, name='partylist-edit_party'),
    url(r'^delete/(?P<party>[\d]+)/$', views.delete_party, name='partylist-delete_party'),
    url(r'^view/(?P<party>[\d]+)/guests/$', views.guests, name='partylist-guests'),
    url(r'^view/(?P<party>[\d]+)/guests/create/$', api.create, name='partylist-api-create'),
    url(r'^view/(?P<party>[\d]+)/guests/destroy/(?P<guestID>[\d]+)/$', api.destroy, name='partlist-api-destroy'),
    url(r'^view/(?P<party>[\d]+)/guests/signIn/(?P<guestID>[\d]+)/$', api.signin, name='partylist-api-signin'),
    url(r'^view/(?P<party>[\d]+)/guests/signOut/(?P<guestID>[\d]+)/$', api.signout, name='partylist-api-signout'),
    url(r'^view/(?P<party>[\d]+)/guests/poll/$', api.poll, name='partylist-api-poll'),
    url(r'^view/(?P<party>[\d]+)/guests/export/$', api.export_list, name='partylist-api-export_list'),
    url(r'^view/(?P<party>[\d]+)/guests/count/$', api.updateCount, name='partylist-api-updateCount'),
    url(r'^view/(?P<party>[\d]+)/guests/count/delta/$', api.updateManualDelta, name='partylist-api-updateManualDelta'),
    url(r'^view/(?P<party>[\d]+)/guests/count/poll/$', api.pollCount, name='partylist-api-pollCount'),
    url(r'^view/(?P<party>[\d]+)/guests/init/$', api.initPulse, name='partylist-api-initPulse'),
]
