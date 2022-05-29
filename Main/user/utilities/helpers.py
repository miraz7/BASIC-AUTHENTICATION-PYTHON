from datetime import datetime
from secrets import token_urlsafe
from user.models import login_sessions


def get_login_session(access_token=None, refresh_token=None, user_email=None):
    if user_email:
        try:
            sessions=login_sessions.objects.filter(email=user_email, is_invalidated=False)
        except login_sessions.DoesNotExist:
            return None
        return sessions
    if refresh_token:
        try:
            sessions=login_sessions.objects.filter(access_token=access_token, refresh_token= refresh_token, is_invalidated=False)
        except login_sessions.DoesNotExist:
            return None
        return sessions    
    else:
        try:
            sessions=login_sessions.objects.filter(access_token=access_token, is_invalidated=False)
        except login_sessions.DoesNotExist:
            return None

        return sessions


def invalidate_session(login_session):
    get_login_session=login_sessions.objects.get(access_token=login_session.access_token)
    get_login_session.is_invalidated=True
    get_login_session.save()
    return True



def get_tokens(user):
    access_token = token_urlsafe(128)
    refresh_token = token_urlsafe(64)
    login_sessions.objects.create(email=user.email, access_token=access_token, refresh_token=refresh_token, logged_in_at=datetime.utcnow(), is_invalidated=False)
    return access_token, refresh_token