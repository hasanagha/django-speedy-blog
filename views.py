from django.shortcuts import redirect
from django.views.generic.dates import DateDetailView
from el_pagination.views import AjaxListView

from speedyblog.forms import CommentForm, UserCommentForm
from speedyblog.models import Comment, Post

from speedyblog.settings import COMMENT_STATUS_APPROVED, POST_STATUS_PUBLISHED


class BlogListView(AjaxListView):
    context_object_name = "posts"
    queryset = Post.objects.filter(status=POST_STATUS_PUBLISHED).select_related()


class BlogDetailView(DateDetailView):
    model = Post
    date_field = 'created_on'
    month_format = '%m'
    page_template = "speedyblog/post_detail_page.html"

    def get_queryset(self):
        queryset = super(BlogDetailView, self).get_queryset()

        return queryset.select_related()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        post = self.object

        if request.user.is_authenticated:
            form = UserCommentForm(request.POST)
        else:
            form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post

            if request.user.is_authenticated:
                comment.user = request.user
                comment.user_name = request.user
                comment.user_email = request.user.email

            comment.ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
            comment.save()

            return redirect(post.get_absolute_url())

        context = self.get_context_data(object=post)
        context['comment_form'] = form

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            form = UserCommentForm()
        else:
            form = CommentForm()

        context = {
            'page_template': self.page_template,
            'comment_form': form,
            'comments': Comment.objects.filter(
                post=self.object.id, status=COMMENT_STATUS_APPROVED
            ).select_related()
        }

        return super(BlogDetailView, self).get_context_data(**context)

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response with a template depending if the request is ajax
        or not and it renders with the given context.
        """
        if self.request.is_ajax():
            template = self.page_template
        else:
            template = self.get_template_names()

        return self.response_class(
            request=self.request,
            template=template,
            context=context,
            **response_kwargs
        )
