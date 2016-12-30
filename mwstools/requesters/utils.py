import os

from mws.mws import DictWrapper

requesters_dir = os.path.dirname(os.path.abspath(__file__))
responses_dir = os.path.join(requesters_dir, 'responses')


def write_response(response, fname):
    return
    with open(os.path.join(responses_dir, fname), 'wb') as f:
        if isinstance(response, DictWrapper):
            f.write(response.original)
        else:
            f.write(response.content)
