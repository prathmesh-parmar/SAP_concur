import requests
from urllib.parse import urlparse
import redis
import time

start_time = time.time()
orignal_urls={}
mapping = {}
final_url_dict={}
index = 1
data =[]
file_list=['safari.txt','firefox.txt','chrome.txt']
redis = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

#Read the files
for files in file_list:
    with open(files) as file:
        temp = file.readlines()
        data = data + temp
#print(data)

#Making a dictionary out of the list of bookmarks received
for i in data:
    i.rstrip() #for stripping the extraspaces before and after the url
    if i.endswith('\n'):
        orignal_urls[index] = i[:-1]
    else:
        orignal_urls[index] = i
    index = index + 1
#print(orignal_urls)

for key, values in orignal_urls.items():
    try:
        r = requests.get(values, allow_redirects=False) # Curl like request
        if (int(r.status_code) == 301 or int(r.status_code) == 302): # if true means redirect url
            location = str(r.headers['Location']) #if redirecting then get the location attribute
            if("http" not in location): # in case of location attribute in not then append
                url = orignal_urls.get(key) + str(r.headers['Location'])[1:]
                r = requests.get(url, allow_redirects=False)
                while(int(r.status_code)!=200):
                    location = str(r.headers['Location'])
                    if("http" not in location):
                        location = orignal_urls.get(key) + str(r.headers['Location'])[1:]
                    if(bool(redis.get(location))):
                        location = str(redis.get(location))
                        location = location[2:-1]
                        break
                    r = requests.get(location, allow_redirects=False)
                redis.set(values,location)
                mapping[values] = location
                
            else:
                while(int(r.status_code)!=200):
                    location = str(r.headers['Location'])
                    if(bool(redis.get(location))):
                        location = str(redis.get(location))
                        location = location[2:-1]
                        break
                    r = requests.get(location, allow_redirects=False)
                redis.set(values,location)
                mapping[values] = location
                #print(mapping)
        elif(int(r.status_code)==404):
            print("Error Status code 404 for URL:" + values)
        else: #first time 200 status
            redis.set(values,values)
            mapping[values] = values
            #print(mapping)
    except requests.exceptions.InvalidURL:
        print("The link provided is not valid "+ values +" Invalid")
    #except:
        #print("Please check the URL "+ values +" and try again")

for key, value in sorted(mapping.items()): #Make a dictionary where key would be the orignal url and values will be list of redirecting urls
    final_url_dict.setdefault(value, []).append(key)
#print(final)


for key, urls in final_url_dict.items():
    temp1=[]
    temp=[]
    temp2=[]
    count =0
    if key in urls:
        temp.insert(0,key)
        x = final_url_dict.get(key)
        x.remove(key)
        temp =temp + x
    else:
        temp = urls
    temp.sort(key = len)

    for urls in temp:      
        if str(urlparse(temp[count]).scheme) == "https":
            temp2.append(urls)
        else:
            temp1.append(urls)
        count = count + 1
    print(temp2+temp1)
print("--- %s seconds with cache ---" % (time.time() - start_time))
