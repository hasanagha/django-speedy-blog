from django.conf.urls import url

from speedyblog.views import BlogDetailView
from speedyblog.views import BlogListView


app_name = "speedyblog"

urlpatterns = [
    url(
        r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-_\w]+)/$',
        BlogDetailView.as_view(),
        name='blog_detail'
    ),
    url(
        r'^archive/$',
        BlogListView.as_view(template_name="blog/post_archive.html", page_template="blog/post_archive_page.html"),
        name="blog_archive"
    ),
    url(r'^$', BlogListView.as_view(), name='blog_index'),
]
