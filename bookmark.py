import requests
from urllib.parse import urlparse
orignal_urls={}
mapping = {}
final_url_dict={}
index = 1
data =[]
file_list=['safari.txt','chrome.txt','firefox.txt']

#Read the files
for files in file_list:
    with open(files) as file:
        temp = file.readlines()
        data = data + temp

#Making a dictionary out of the list of bookmarks received
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
        r = requests.get(values, allow_redirects=False) # Making a curl like request
        if (int(r.status_code) == 301 or int(r.status_code) == 302): #if status is 302 or 301 get the location attribute from header
            location = str(r.headers['Location'])
            if("http" not in location):
                url = orignal_urls.get(key) + str(r.headers['Location'])[1:]
                r = requests.get(url, allow_redirects=False)
                mapping[values] = str(r.headers['Location'])
            else:
                while(int(r.status_code)!=200): #Loop until you find the orignal url
                    location = str(r.headers['Location'])
                    r = requests.get(location, allow_redirects=False)
                mapping[values] = location
        elif(int(r.status_code)==404): #if page not found 
            print("Error Status code 404 for URL:" + values)
        else:
            mapping[values] = values
    except requests.exceptions.InvalidURL: # incase of invalidurl exception
        print("The link provided is not valid "+ values +" Invalid")
    except:
        print("Please check the URL "+ values +" and try again")

for key, value in sorted(mapping.items()): #Make a dictionary where key would be the orignal url and values will be list of redirecting urls
    final_url_dict.setdefault(value, []).append(key)


for key, urls in final_url_dict.items():
    temp1=[]
    temp=[]
    temp2=[]
    count =0
    if key in urls: # sort on basis of redirection
        temp.insert(0,key)
        x = final_url_dict.get(key)
        x.remove(key)
        temp =temp + x
    else:
        temp = urls
    temp.sort(key = len) # sort on basis of length

    for urls in temp:      # sort on basis of https and http
        if str(urlparse(temp[count]).scheme) == "https":
            temp2.append(urls)
        else:
            temp1.append(urls)
        count = count + 1
    print(temp2+temp1)
