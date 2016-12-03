import datetime

from django.contrib.auth.models import User
from django.db.models.aggregates import Count
from django.shortcuts import render_to_response
from django.template import RequestContext

from location.models import Location
from messaging.models import Message
from profile.models import UserProfile
from skills.models import UserSkill, SlugPhrase


def general(request):
    rc = RequestContext(request)
    return render_to_response('public/general.html', rc)

def developer(request):
    rc = RequestContext(request)
    return render_to_response('public/developer.html', rc)

def faq(request):
    rc = RequestContext(request)
    return render_to_response('public/faq.html', rc)

def calculate_metrics():

    total_messages = Message.objects.count()
    messages_today = Message.objects.filter(sent_time__gte=datetime.date.today()).count()
    messages_last_week = Message.objects.filter(sent_time__gte=(datetime.date.today()-datetime.timedelta(days=7))).count()

    total_user_count = User.objects.count()
    users_with_about = 100 * UserProfile.objects.exclude(about_me_text='').count() / float(total_user_count)
    users_with_picture = 100 * UserProfile.objects.exclude(avatar_link='').count() / float(total_user_count)

    available_skill_count = SlugPhrase.objects.annotate(count=Count('userskill')).exclude(count=0).count()
    average_num_skills_per_user = UserSkill.objects.count() / total_user_count



    valid_locations = Location.objects.exclude(position_updated=None).count()
    valid_locations_percent = "{0:.2f}".format(100.0 * valid_locations / total_user_count)

    return {
        'total_messages': total_messages,
        'messages_today': messages_today,
        'messages_last_week': messages_last_week,

        'total_user_count': total_user_count,
        'users_with_about': users_with_about,
        'users_with_picture': users_with_picture,

        'valid_locations': valid_locations,
        'valid_locations_percent': valid_locations_percent,

        'available_skill_count': available_skill_count,
        'average_num_skills_per_user': average_num_skills_per_user,
    }



def metrics(request):
    rc = RequestContext(request)
    rc['metrics'] = calculate_metrics()
    return render_to_response('public/metrics.html', rc)