from lamson.routing import StateStorage, ROUTE_FIRST_STATE
from mailinglists.models import UserState

class UserStateStorage(StateStorage):

    def clear(self):
        UserState.objects.all().delete()

    def _find_state(self, key, sender):
        sender = sender.lower()
        key = key.lower()
        states = UserState.objects.filter(state_key = key,
                                          from_address = sender)
        if states:
            return states[0]
        else:
            return None

    def get(self, key, sender):
        sender = sender.lower()
        key = key.lower()
        try:
            stored_state = UserState.objects.get(state_key = key,
                                                 from_address = sender)
            return stored_state.state
        except UserState.DoesNotExist:
            return ROUTE_FIRST_STATE

    def key(self, key, sender):
        raise Exception("THIS METHOD MEANS NOTHING TO DJANGO!")

    def set(self, key, sender, to_state):
        """
        Store an appropriate user-state object in the database,
        except if the state to store is "START", because that's
        just the default state when nothing is found anyway.
        """        
        sender = sender.lower()
        key = key.lower()
        if to_state == "START":
            UserState.objects.filter(state_key = key,
                                     from_address = sender) \
                             .delete()
        else:
            stored_state,created = \
                UserState.objects.get_or_create(state_key = key,
                                                from_address = sender,
                                                defaults={'state': to_state})
            if not created:
                stored_state.state = to_state
                stored_state.save()

    def set_all(self, sender, to_state):
        """
        This isn't part of normal lamson code, it's used to 
        control the states for all of the app.handlers.admin
        lists during a bounce.
        """
        sender = sender.lower()
        UserState.objects.filter(from_address = sender).update(state=to_state)


