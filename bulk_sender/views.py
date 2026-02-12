from django.shortcuts import render, redirect
from celery import group
from .forms import EmailForm
from .utils import get_valid_emails
from .tasks import send_email

def index(request):
    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            emails = get_valid_emails(file)

            if not emails:
                return render(request, 'bulk_sender/index.html', {
                    'form': form,
                    'error': 'No valid email addresses found in CSV'
                })

            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            group(
                send_email.s(email, subject, message)
                for email in emails
            ).apply_async()

            request.session['success'] = f'{len(emails)} emails queued'
            return redirect('bulk_sender:index')

    else:
        form = EmailForm()

    return render(request, 'bulk_sender/index.html', {
        'form': form,
        'success': request.session.pop('success', None)
    })