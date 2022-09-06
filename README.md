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
### Meteor
After runing following script, you can find export result in project directory. 
```shell
scrapy crawl Meteor -o "%(spider_name)s-%(run_date)s.csv"
```
