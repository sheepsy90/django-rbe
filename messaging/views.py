from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http.response import JsonResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext

from messaging.forms import ComposeForm
from messaging.models import Message, MessageStatus


@login_required
def inbox(request):
    rc = RequestContext(request)
    rc['messages_received'] = Message.objects.filter(recipient=request.user).exclude(status=MessageStatus.DELETED)
    return render_to_response('messaging/inbox.html', rc)


@login_required
def message(request, message_id):
    rc = RequestContext(request)

    try:
        # Existence check
        mqs = Message.objects.filter(id=message_id)
        if mqs.exists():
            m = mqs.first()

            if request.user not in [m.sender, m.recipient]:
                rc['denied'] = True
            elif m.status != MessageStatus.DELETED:
                # Mark the message as read
                if m.recipient == request.user:
                    m.status = MessageStatus.READ
                    m.save()
                rc['message'] = m
            else:
                rc['deleted'] = True
    except:
        pass

    return render_to_response('messaging/message.html', rc)


@login_required
def outbox(request):
    rc = RequestContext(request)
    rc['messages_sent'] = Message.objects.filter(sender=request.user).exclude(status=MessageStatus.DELETED)
    return render_to_response('messaging/outbox.html', rc)


@login_required
def compose(request, recipient_user_id):
    rc = RequestContext(request)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ComposeForm(request.POST)
        rc['form'] = form

        # check whether it's valid:
        if form.is_valid():
            try:
                subject = form.cleaned_data['subject']
                body = form.cleaned_data['body']
                user_id = form.cleaned_data['recipient_id']
                recipient = User.objects.get(id=int(user_id))

                m = Message.create_message(request.user, recipient, subject, body)
                return HttpResponseRedirect(reverse('message', kwargs={'message_id': m.id}))
            except User.DoesNotExist:
                form.add_error(None, "Recipient doesn't exists")
            except Exception:
                form.add_error(None, "Server error. Could not send message!")

        rc['form'] = form
    else:

        try:
            user = User.objects.get(id=int(recipient_user_id))
            form = ComposeForm(initial={
                'recipient_id': recipient_user_id,
                'recipient_name': user.username
            })
            rc['form'] = form
        except User.DoesNotExist:
            pass

    return render(request, 'messaging/compose.html', rc)


@login_required
def delete_message(request):
    message_id = request.POST.get('message_id')

    if not message_id:
        return JsonResponse({'success': False, 'error': 'Message id not set'})

    try:
        m = Message.objects.get(id=message_id)

        if m.recipient != request.user:
            return JsonResponse({'success': False, 'error': 'Not allowed to delete the message!'})
        else:
            m.status = MessageStatus.DELETED
            m.save()
            return JsonResponse({'success': True})

    except Message.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'No such message'})
    except Exception:
        return JsonResponse({'success': False, 'error': 'Internal server error'})
