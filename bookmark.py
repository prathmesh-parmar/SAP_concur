import requests
from urllib.parse import urlparse
orignal_urls={}
mapping = {}
final_url_dict={}
index = 1
data =[]
file_list=['safari.txt','chrome.txt','firefox.txt']

for files in file_list:
    with open(files) as file:
        temp = file.readlines()
        data = data + temp
#print(data)
for i in data:
    i.rstrip()
    if i.endswith('\n'):
        orignal_urls[index] = i[:-1]
    else:
        orignal_urls[index] = i
    index = index + 1
#print(orignal_urls)

for key, values in orignal_urls.items():
    try:
        r = requests.get(values, allow_redirects=False)
        if (int(r.status_code) == 301 or int(r.status_code) == 302):
            location = str(r.headers['Location'])
            if("http" not in location):
                url = orignal_urls.get(key) + str(r.headers['Location'])[1:]
                r = requests.get(url, allow_redirects=False)
                #print(str(r.status_code), location)
                mapping[values] = str(r.headers['Location'])
            else:
                #print(str(r.status_code), location)
                while(int(r.status_code)!=200):
                    location = str(r.headers['Location'])
                    r = requests.get(location, allow_redirects=False)
                mapping[values] = location
                #print(mapping)
        elif(int(r.status_code)==404):
            print("Error Status code 404 for URL:" + values)
        else:
            mapping[values] = values
            #print(mapping)
    except requests.exceptions.InvalidURL:
        print("The link provided is not valid "+ values +" Invalid")
    except:
        print("Please check the URL "+ values +" and try again")

for key, value in sorted(mapping.items()):
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
