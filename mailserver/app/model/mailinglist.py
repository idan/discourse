from django.db.models import Q
from django.contrib.auth.models import User
from email.utils import parseaddr
from lamson.mail import MailResponse
from config import settings
from app.model.archive import build_index
from groups.models import *


def find_group(slug):
    assert slug == slug.lower()
    try:
        return InterestGroup.objects.get(slug = slug)
    except InterestGroup.DoesNotExist:
        return None

def similar_named_groups(group_name):
    #TODO: Do something intelligent (like original Librelist, copied at end?
    return InterestGroup.objects.all()

def add_subscriber(address, group_name):
    #assert group_name == group_name.lower()
    group = find_group(group_name)
    sub_name, sub_addr = parseaddr(address)
    username = sub_addr.lower() # normalize
    try:
        user = User.objects.get(Q(username=username) | Q(email=sub_addr))
    except User.DoesNotExist:
        user = User.objects.create_user(username, sub_addr)
        set_user_full_name(user, sub_name)
    
    return Membership.objects.get_or_create(user=user, group=group,
                                            defaults={'level':0})    

def set_user_full_name(user, sub_name):
    #TODO: Try to set user.first_name, user.last_name
    pass

def remove_subscriber(address, group_name):
    #assert group_name == group_name.lower()
    find_memberships(address, group_name).delete()

def remove_all_subscriptions(address):
    find_memberships(address).delete()

def find_memberships(address, group_name=None):
    #if group_name: assert group_name == group_name.lower()
    _, sub_addr = parseaddr(address)

    by_user = Q(user__username=sub_addr.lower()) | Q(user__email=sub_addr)
    mems = Membership.objects.filter(by_user)
    if group_name:
        return mems.filter(group__slug=group_name)
    else:
        return mems

def post_message(relay, message, group_name, host):
    #assert group_name == group_name.lower()
    group = find_group(group_name)
    assert group, "User is somehow able to post to non-existent list %s" % group_name

    list_addr = "%s@%s" % (group_name, host)
    delivery = craft_response(message, group_name, list_addr)

    subject_mod = "[%s]" % group_name
    if subject_mod not in delivery['subject']:
        delivery['subject'] = subject_mod + " " + delivery['subject']

    for user_email in group.members.all().values('email'):

        relay.deliver(delivery, To=user_email, From=list_addr)


def craft_response(message, list_name, list_addr):
    assert list_name == list_name.lower()
    response = MailResponse(To=list_addr, 
                            From=message['from'],
                            Subject=message['subject'])

    msg_id = message['message-id']

    response.update({
        "Sender": list_addr, 
        "Reply-To": list_addr,
        "List-Id": list_addr,
        "List-Unsubscribe": "<mailto:%s-unsubscribe@librelist.com>" % list_name,
        "List-Archive": "<http://librelist.com/archives/%s/>" % list_name,
        "List-Post": "<mailto:%s>" % list_addr,
        "List-Help": "<http://librelist.com/help.html>",
        "List-Subscribe": "<mailto:%s-subscribe@librelist.com>" % list_name,
        "Return-Path": list_addr, 
        "Precedence": 'list',
    })

    if 'date' in message:
        response['Date'] = message['date']

    if 'references' in message:
        response['References'] = message['References']
    elif msg_id:
        response['References'] = msg_id

    if msg_id:
        response['message-id'] = msg_id

        if 'in-reply-to' not in message:
            response["In-Reply-To"] = message['Message-Id']

    if message.all_parts():
        response.attach_all_parts(message)
    else:
        response.Body = message.body()

    return response

"""
# These were in the original librelist, not sure what of this we want.

from lib import metaphone
import Stemmer


def stem_and_meta(list_name):
    s = Stemmer.Stemmer('english')
    name = " ".join(s.stemWords(list_name.split('.')))
    return metaphone.dm(name)

def create_list(list_name):
    list_name = list_name.lower()
    mlist = find_list(list_name)
    sim_pri, sim_sec = stem_and_meta(list_name)

    if not mlist:
        mlist = MailingList(archive_url = "/archives/" + list_name,
                            archive_queue = "/queues/" + list_name,
                            name=list_name,
                            similarity_pri = sim_pri,
                            similarity_sec = sim_sec)
        mlist.save()
        build_index()

    return mlist

def delete_list(list_name):
    assert list_name == list_name.lower()
    MailingList.objects.filter(name = list_name).delete()

def similar_named_lists(list_name):
    
    sim_pri, sim_sec = stem_and_meta(list_name)
    sim_sec = sim_sec or sim_pri

    return MailingList.objects.filter(Q(similarity_pri = sim_pri) | 
                                       Q(similarity_sec =
                                         sim_sec))

def disable_all_subscriptions(address):
    Subscription.objects.filter(subscriber_address=address).update(enabled=False)

def enable_all_subscriptions(address):
    Subscription.objects.filter(subscriber_address=address).update(enabled=True)


"""