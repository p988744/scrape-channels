from datetime import datetime


def uri_params(params, spider):
    return {
        **params,
        'spider_name': spider.name,
        'run_date': datetime.now().strftime('%Y-%m-%d')
    }
