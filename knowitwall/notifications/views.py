from django.shortcuts import render, redirect
from django.template import loader
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from .emails import send_email
from .slack import send_feedback_to_slack

@require_http_methods(["POST"])
def get_feedback(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    feedback_overall = request.POST.get('feedback_overall')
    context_email = {'name': name, 'email': email, 'content': feedback_overall}
    email_message_html = loader.render_to_string(template_name='notifications/email_user_feedback.html', context=context_email)
    email_message_txt = loader.render_to_string(template_name='notifications/email_user_feedback.txt', context=context_email)
    send_email(message=email_message_html)
    # send_feedback_to_slack(message=email_message_txt)
    return redirect('content:index')
