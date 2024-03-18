from rest_framework import renderers
import json


# This to customize the response
class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        # import pdb
        # pdb.set_trace()
        if 'ErrorDetail' in str(data):
            response = json.dumps({'error': data})
        else:
            response = json.dumps({'data': data})
        return response
        # return super().render(response, accepted_media_type, renderer_context)
