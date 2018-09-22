#Web Scrap con Recursividad en las llamadas http para simular la paginación
import json      #Libreria para tratar valores json: parsed_json = json.loads(json_string)
import requests  #Libreria para las peticiones http
import requests  #Libreria para las peticiones http
import shutil    #Libreria para Operaciones de archivos de alto nivel
import re        #Libreria para Expresiones regulares
import io        #Libreria para escribir ficheros

#Establece los campos que queremos obtener
CAMPOS = ["webdescriptionshort" , "countryoforigin", "webbrandname", "liquorstyle", "webregionoforigin", "vintage"]

#Establece las cabeceras para la llamada http 
headers = { 'user-agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/66.0.3359.139 Chrome/66.0.3359.139 Safari/537.36', 
            'content-type': 'application/json'}

#Define los parametros de la llamada http a la url https://api.danmurphys.com.au/apis/ui/Browse
data = {'pageNumber': 1,'sortType':'Relevance','pageSize': 20,'subDepartment':'rose','filters': [],'department':'red wine','Location':'ListerFacet'}



def f(n):
        #Devuel el nombre unido a un array con los otros datos de la extructuda["Products"][0]["AdditionalDetails"])[0]["Value"]
        #   con re.sub(r'^\s+' eliminamos con Exppresion Regular los espacios al priciopio
        return [n["Name"]] + map(  lambda x : re.sub(r'^\s+', "",extract(x,n) ),CAMPOS)
 
    
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
    
 