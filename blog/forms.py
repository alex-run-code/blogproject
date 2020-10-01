from django import forms
from django.http import BadHeaderError, HttpResponse, HttpResponseRedirect

from .models import Comment
from django.core.mail import send_mail


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

    def send_email(self, name, email, post, comments, to):
        subject = '{} ({}) recommends you reading "{}"'.format(name, email, post.title)
        message = 'Read "{}" \n\n{}\'s comments: {}'.format(post.title, name, comments)
        from_email = 'from@mail.com'
        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email, [to])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('.')
        else:
            # In reality we'd use a form class
            # to get proper validation errors.
            return HttpResponse('Make sure all fields are entered and valid.')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')