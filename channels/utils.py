import random
from datetime import datetime


def uri_params(params, spider):
    return {
        **params,
        'spider_name': spider.name,
        'run_date': datetime.now().strftime('%Y-%m-%d')
    }


user_agent_list = [
    # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
]


def get_user_agent():
    return random.choice(user_agent_list)
