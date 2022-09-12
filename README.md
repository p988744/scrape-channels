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
