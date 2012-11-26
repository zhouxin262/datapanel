from django.contrib.sessions.backends.base import SessionBase, CreateError
from django.core.exceptions import SuspiciousOperation
# from django.db import IntegrityError, transaction, router
# from django.utils.encoding import force_unicode
# from django.utils import timezone


class SessionStore(SessionBase):
    """
    Implements database session store.
    """
    def __init__(self, session_key=None):
        super(SessionStore, self).__init__(session_key)

    def load(self):
        try:
            s = Session.objects.get(
                session_key=self.session_key
            )
        except (Session.DoesNotExist, SuspiciousOperation):
            s = Session()
            s.session_key = self.session_key
            s.save()

        return s

    def create(self):
        while True:
            self._session_key = self._get_new_session_key()
            try:
                # Save immediately to ensure we have a unique entry in the
                # database.
                self.save(must_create=True)
            except CreateError:
                # Key wasn't unique. Try again.
                continue
            self.modified = True
            self._session_cache = {}
            return

    def save(self):
        s = self.load()
        if s:
            s.save()


# At bottom to avoid circular import
from session.models import Session
