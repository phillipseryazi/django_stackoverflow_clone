import json
from rest_framework.renderers import JSONRenderer


class UserRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        errors = data.get('erros', None)

        if errors is not None:
            return super(UserRenderer, self).render(data)

        message = data.get('message', None)
        token = data.get('token', None)
        if token is not None and isinstance(token, bytes):
            data['token'] = token.decode('utf-8')
            if message is not None:
                data['message'] = message

        return json.dumps({'user': data})
