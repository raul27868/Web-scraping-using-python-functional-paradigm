#Web Scrap https://www.danmurphys.com.au/red-wine/rose
# json: https://gist.github.com/raul27868/a5010f230b7621950f23acb7ca87b249

import json       # for manage json values: parsed_json = json.loads (json_string)
import requests   # for http requests
import requests   # for http requests
import shutil     # for High Level File Operations
import re         # for Regular Expressions
import io         # for write files

#Set the fields that we want to scrape
FIELDS = ["webdescriptionshort" , "countryoforigin", "webbrandname", "liquorstyle", "webregionoforigin", "vintage"]

#Set the headers for the http call
headers = { 'user-agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/66.0.3359.139 Chrome/66.0.3359.139 Safari/537.36', 
            'content-type': 'application/json'}

#Set the parameters of the http call to the url: https://api.danmurphys.com.au/apis/ui/Browse
data = {'pageNumber': 1,'sortType':'Relevance','pageSize': 20,'subDepartment':'rose','filters': [],'department':'red wine','Location':'ListerFacet'}



def f(n):
        #Returns the values obtained for each array (20 per page):
        #   First, the value is returned in the key ["Name"]. Then it returns the values with keys of the FIELDS array that are in the structure ["Products"] [0] ["AdditionalDetails"]
        #   re.sub(r'^\s+'... we eliminated with Regular Expression the spaces at the beginning
        return [n["Name"]] + map(  lambda x : re.sub(r'^\s+', "",extract(x,n) ),FIELDS)
 
    
def extract(r,n):
    #We obtain the values of the key passed by parameter.        
    try:
        return  filter(lambda x : x["Name"]==r  ,  n["Products"][0]["AdditionalDetails"])[0]["Value"]   
    except IndexError as error: return ""



def scrap_danmurphys(page_from , page_to):
    #Principal function
    data["pageNumber"] =  page_from
    
    print "page:"  ,page_from
    print "******************************************************"
    print ""

    json_data = map(f,  json.loads(requests.post('https://api.danmurphys.com.au/apis/ui/Browse', headers=headers, data=json.dumps(data) ).text)["Bundles"]   )
    
    #To detect the last call to web server
    if(page_from == page_to or  json_data == []   ):
        return json_data
    else:
        # Recursion: call this function again if there are pages for scrap
        return scrap_danmurphys(page_from+1,page_to) + json_data




#Write the result in the file danmurphys.csv
with io.open('danmurphys.csv', 'w',closefd=True) as file:
    #Write the headers in quotes and separated by;   
    file.write(
                    unicode(";".join(map(lambda campo: '"'+ re.sub(r'^\s+', "",campo ) +'"' ,["Name"] + CAMPOS)+["\n"]))
              )   
               
    #Write the data in quotes and separated by;
    map(lambda fila:   file.write(
                    unicode(";".join(map(lambda campo: '"'+ re.sub(r'^\s+', "",campo ) +'"' ,fila)+["\n"]))
                               ),      
     scrap_danmurphys(1,""))
    
 
