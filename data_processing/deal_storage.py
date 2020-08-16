import json
import random
from datetime import datetime, timedelta

now_time = datetime.now()
new_time  = now_time.strftime('%Y-%m-%d')

# data = ""
with open ("storage.json") as f:
    data = f.read()
data = json.loads(data)
data = (data["data"])
print(data)
name = {}
IP = 0
for item in data:
    name[item['name'].lower()] = IP
    IP += 1

with open('result.txt') as f:
    add_item = f.read()
if add_item in (name.keys()):
    index = name[add_item]
    data[index]['number'] = str(eval(data[index]['number']) + 1)
else:
    new_item = {}
    new_item['type'] = 'fruit'
    new_item['name'] = add_item
    new_item['number'] = '1'
    new_item['entryTime'] = new_time
    new_item['vitamins'] = str((random.randint(1,5)))
    new_item['carbohydrates'] = str((random.randint(1,5)))
    new_item['calories'] = str((random.randint(1,6)))
    data.append(new_item)
print(data)
data = {'data': data}
with open("storage.json", 'w') as f:
    f.write(json.dumps(data))