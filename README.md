# scrape-channels

## requirements
- python 3.9 or higher

## installation
First, use virtualenv to create a python environment.
Then install packages:
```shell
pip install -r requirements.txt
```

## quick start
After running following script, you can find export result in project directory. 

### show available spiders
```shell
scrapy list
```

### Meteor
```shell
scrapy crawl meteor -O "%(spider_name)s-%(run_date)s.csv"
```

### PTT
```shell
scrapy crawl ptt -O "%(spider_name)s-%(run_date)s.csv"
```

### mobile01
```shell   
scrapy crawl mobile01 -O "%(spider_name)s-%(run_date)s.csv"
```

### youtube
Create a api key from [Google Developers Console](https://console.developers.google.com/) then export it to environment variable `YT_API_KEY`.
```shell
export YT_API_KEY=your_api_key
scrapy crawl youtube -O "%(spider_name)s-%(run_date)s.csv"
```
