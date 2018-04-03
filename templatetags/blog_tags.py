from django import template

from speedyblog.models import Post
from speedyblog.settings import POST_STATUS_PUBLISHED

register = template.Library()


def latest_blog_posts(context, num):
    latest_blog_posts = Post.objects.filter(status=POST_STATUS_PUBLISHED)[:num].select_related()

    return {
        'latest_blog_posts': latest_blog_posts
    }


register.inclusion_tag('tags/latest_blog_posts.html',
                       takes_context=True)(latest_blog_posts)
