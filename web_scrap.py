#Web Scrap https://www.danmurphys.com.au/red-wine/rose

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
        #Devuelve el nombre unido a un array con los otros datos de la extructura : ["Products"][0]["AdditionalDetails"])[0]["Value"]
        #   con re.sub(r'^\s+' eliminamos con Exppresion Regular los espacios al priciopio
        return [n["Name"]] + map(  lambda x : re.sub(r'^\s+', "",extract(x,n) ),FIELDS)
 
    
def extract(r,n):
    try:
        return  filter(lambda x : x["Name"]==r  ,  n["Products"][0]["AdditionalDetails"])[0]["Value"]   
    
    except IndexError as error: return ""



def scrap_danmurphys(page_from , page_to):

    data["pageNumber"] =  page_from
    
    print "page:"  ,page_from
    print "******************************************************"
    print ""
   
    
    json_data = map(f,  json.loads(requests.post('https://api.danmurphys.com.au/apis/ui/Browse', headers=headers, data=json.dumps(data) ).text)["Bundles"]   )
    
    #print json_data
    #print ""
    
    if(page_from == page_to or  json_data == []   ):
        return json_data
    else:
        return scrap_danmurphys(page_from+1,page_to) + json_data
    

#Escribe el resultado de la variable DATA en el fichero danmurphys.csv
with io.open('danmurphys.csv', 'w',closefd=True) as file:
    #Escibre las cabeceras entre comillas y separados por ;   
    file.write(
                    unicode(";".join(map(lambda campo: '"'+ re.sub(r'^\s+', "",campo ) +'"' ,["Name"] + CAMPOS)+["\n"]))
              )   
               
    #Escibre los datos entre comillas y separados por ;    
    map(lambda fila:   file.write(
                    unicode(";".join(map(lambda campo: '"'+ re.sub(r'^\s+', "",campo ) +'"' ,fila)+["\n"]))
                               ),      
     scrap_danmurphys(1,""))
    
 
