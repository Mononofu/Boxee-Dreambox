from django.conf.urls.defaults import *
from furidamu.polls.models import Poll

info_dict = {
    'queryset': Poll.objects.all(),
}

urlpatterns = patterns('',
    (r'^$', 'furidamu.dreambox.views.index'),
    (r'^feed.rss$', 'furidamu.dreambox.views.index'),
    (r'^(?P<channel_id>[\dabcdef:]+)/$', 'furidamu.dreambox.views.channel'),
)
