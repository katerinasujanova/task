#import elasticsearch
import json
import scraper

#es = elasticsearch()

data = scraper.get_data()

es_data = json.dumps(data)
print(es_data)
