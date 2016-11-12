from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.db.models.aggregates import Count
from django.http.response import JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, render
from django.template import RequestContext

from library.log import rbe_logger
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


@login_required()
def messages(request):
    x = Message.objects.filter(recipient=request.user, status=MessageStatus.UNREAD).annotate(count=Count('status')).order_by('count').first()
    return conversation(request, x.sender.id)


def get_ordered_latest_contact_list(user):
    # TODO add distinct once switching to Postgresql
    sent_message = list(Message.objects.filter(sender=user).order_by('-sent_time').values_list('recipient', 'sent_time'))
    received_messages = list(Message.objects.filter(recipient=user).order_by('-sent_time').values_list('sender', 'sent_time'))

    result_dict = {}
    # Dummy algorithm to order by latest message
    for element in sent_message + received_messages:
        uid, dt = element

        if uid not in result_dict:
            result_dict[uid] = []
        result_dict[uid].append(dt)

    for key in result_dict.keys():
        result_dict[key] = max(result_dict[key])

    as_real_user_object = [(User.objects.get(id=e[0]), e[1]) for e in result_dict.items()]
    as_real_user_object = [{
        'user': e[0],
        'unread_messages': Message.objects.filter(sender=e[0], recipient=user, status=MessageStatus.UNREAD).count(),
        'last_contact': e[1]
    } for e in as_real_user_object]

    sorted_list = sorted(as_real_user_object, key=lambda x: (x['unread_messages'], x['last_contact']))
    sorted_list.reverse()
    return sorted_list


@login_required()
def conversation(request, user_id, error_message=''):
    try:
        rc = RequestContext(request)
        conversation_partner = User.objects.get(id=user_id)
        messages = Message.objects.filter(Q(sender=request.user) | Q(recipient=request.user)).filter(
            Q(sender=conversation_partner) | Q(recipient=conversation_partner)).order_by('-sent_time')[0:10]

        ordered_latest_conversations = get_ordered_latest_contact_list(request.user)

        rc['latest_conversations'] = ordered_latest_conversations
        rc['messages'] = messages.reverse()
        rc['error_message'] = error_message
        rc['conversation_partner'] = conversation_partner
        return render_to_response('messaging/conversation.html', rc)
    except User.DoesNotExist:
        raise Http404


@login_required()
def send(request):
    recipient_id = request.POST.get('recipient_id')
    message_text = request.POST.get('message_text')
    error_message = ''

    try:
        if not message_text:
            error_message = 'Empty message cannot be sent!'
        elif len(message_text) > 1200:
            error_message = 'A message cannot be longer than 1200 characters!'
        else:
            recipient = User.objects.get(id=recipient_id)
            Message.create_message(request.user, recipient, '', message_text)
    except User.DoesNotExist as e:
        rbe_logger.warning("Had problems")
        error_message = "User to write to doesn't exists"
    except Exception as e:
        error_message = "Unknown error occurred - please try again later"
        rbe_logger.exception(e)

    return conversation(request, recipient_id, error_message)


@login_required()
def messaging_confirm_read(request):
    message_ids = request.POST.getlist('message_ids[]', None)

    if not message_ids:
        return JsonResponse({'success': False, 'reason': 'No message_ids list present'})

    try:
        message_ids = [int(e) for e in message_ids]
    except:
        return JsonResponse({'success': False, 'reason': 'Error in parsing message_ids'})

    Message.objects.filter(id__in=message_ids, recipient=request.user).update(status=MessageStatus.READ)

    return JsonResponse({'success': True})