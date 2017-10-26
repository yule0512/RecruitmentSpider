from lagouwang.settings import USER_AGENS
import random

class RandomUserAgent(object):
    def process_request(self,request,spider):
        user_agent = random.choice(USER_AGENS)
        request.headers.setdefault('Agent',user_agent)