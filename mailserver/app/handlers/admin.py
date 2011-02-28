from email.utils import parseaddr
from config.settings import relay, SPAM, CONFIRM
import logging
from lamson import view, queue
from lamson.routing import route, stateless, route_like, state_key_generator
from lamson.bounce import bounce_to
from app.model import mailinglist, archive
from app.handlers import bounce


INVALID_LISTS = ["noreply", "unbounce"]


@state_key_generator
def module_and_to(module_name, message):
    name, address = parseaddr(message['to'])
    if '-' in address:
        list_name = address.split('.')[0]
    else:
        list_name = address.split('@')[0]

    return module_name + ':' + list_name


@route("(address)@(host)", address='.+')
def SPAMMING(message, **options):
    spam = queue.Queue(SPAM['queue'])
    spam.push(message)
    return SPAMMING


@route('(bad_list)@(host)', bad_list='.+')
@route('(group_name)@(host)')
@route('(group_name).(topic)@(host)')
@bounce_to(soft=bounce.BOUNCED_SOFT, hard=bounce.BOUNCED_HARD)
def START(message, group_name=None, topic=None, host=None, bad_list=None):
    #group_name = group_name.lower() if group_name else None
    #bad_list = bad_list.lower() if bad_list else None
    host = host.lower() if host else None

    logging.debug("Group name: "+group_name)
    if bad_list:

        help = view.respond(locals(), "mail/bad_list_name.msg",
                            From="noreply@%(host)s",
                            To=message['from'],
                            Subject="That's not a valid list name.")
        relay.deliver(help)

        return START

    elif group_name in INVALID_LISTS or message.route_from.endswith(host):
        logging.debug("LOOP MESSAGE to %r from %r.", message['to'],
                     message.route_from)
        return START

    group = mailinglist.find_group(group_name)
    if group:
        action = "subscribe to"
        activity = group.find_topic(topic) if topic else None
        # TODO: put activity and topic in message template 
        CONFIRM.send(relay, group_name, message, 'mail/confirmation.msg',
                          locals())
        return CONFIRMING_SUBSCRIBE

    else:
        similar_groups = mailinglist.similar_named_groups(group_name)
        CONFIRM.send(relay, group_name, message, 'mail/create_confirmation.msg',
                          locals())

        return CONFIRMING_SUBSCRIBE

@route('(group_name).confirm.(id_number)@(host)')
def CONFIRMING_SUBSCRIBE(message, group_name=None, id_number=None, host=None):
    #group_name = group_name.lower() if group_name else None
    host = host.lower() if host else None

    original = CONFIRM.verify(group_name, message.route_from, id_number)

    if original:
        mailinglist.add_subscriber(message.route_from, group_name)

        msg = view.respond(locals(), "mail/subscribed.msg",
                           From="noreply@%(host)s",
                           To=message['from'],
                           Subject="Welcome to %(group_name)s group.")
        relay.deliver(msg)

        CONFIRM.cancel(group_name, message.route_from, id_number)

        return POSTING
    else:
        logging.warning("Invalid confirm from %s", message.route_from)
        return CONFIRMING_SUBSCRIBE


@route('(group_name).(topic)@(host)')
@route('(group_name)@(host)')
def POSTING(message, group_name=None, action=None, topic=None, host=None):
    #group_name = group_name.lower() if group_name else None
    #action = action.lower() if action else None
    host = host.lower() if host else None

    if topic == 'unsubscribe':
        topic = "unsubscribe from"
        CONFIRM.send(relay, group_name, message, 'mail/confirmation.msg',
                          locals())
        return CONFIRMING_UNSUBSCRIBE
    else:
        mailinglist.post_message(relay, message, group_name, host)
        # archive makes sure it gets cleaned up before archival
        final_msg = mailinglist.craft_response(message, group_name, 
                                               group_name + '@' + host)
        archive.enqueue(group_name, final_msg)
        # TODO: Save message in DB?
        # TODO: if topic: Link message to topic, attach message attachments to topic 
        return POSTING
    

@route_like(CONFIRMING_SUBSCRIBE)
def CONFIRMING_UNSUBSCRIBE(message, list_name=None, id_number=None, host=None):
    list_name = list_name.lower() if list_name else None
    host = host.lower() if host else None

    original = CONFIRM.verify(list_name, message.route_from, id_number)

    if original:
        mailinglist.remove_subscriber(message.route_from, list_name)

        msg = view.respond(locals(), 'mail/unsubscribed.msg',
                           From="noreply@%(host)s",
                           To=message['from'],
                           Subject="You are now unsubscribed from %(list_name)s.")
        relay.deliver(msg)

        CONFIRM.cancel(list_name, message.route_from, id_number)

        return START
    else:
        logging.warning("Invalid unsubscribe confirm from %s",
                        message.route_from)
        return CONFIRMING_UNSUBSCRIBE


@route("(address)@(host)", address=".+")
def BOUNCING(message, address=None, host=None):
    # don't send out a message if they are bouncing
    return BOUNCING

