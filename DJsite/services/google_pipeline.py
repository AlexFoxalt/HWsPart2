from django.http import HttpResponseNotAllowed

USER_FIELDS = ['username', 'email']


def create_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    fields = dict((name, kwargs.get(name, details.get(name)))
                  for name in backend.setting('USER_FIELDS', USER_FIELDS))

    if not fields['email'] or not fields['username']:
        return HttpResponseNotAllowed('Can not find email. Check your privacy settings!')

    fields['nickname'] = fields.get('username')

    return {
        'is_new': True,
        'user': strategy.create_user(**fields)
    }
