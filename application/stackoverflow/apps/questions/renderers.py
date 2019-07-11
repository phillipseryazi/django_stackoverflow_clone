import json
from rest_framework.renderers import JSONRenderer


class QuestionRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return json.dumps({'question': data})


class QuestionListRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return json.dumps({'questions': data})
