# Web-scraping-using-python-functional-paradigm-
Code to illustrate the use of functional programming in python to make web scraping in http calls that return json

<p>This script works for Python 2 (or higher).</p>
<p>It is an example to obtain the values ​​of the wine store https://www.danmurphys.com.au/red-wine/rose</p>
<p>The data can not be found on the html page. The data are in json format and it is necessary to obtain them by making HTTP calls with the POST method and passing as parameters a text string with json structure. We do this with the Python requests module and the requests.post function</p> 

<p>We convert the json document to a Python object with the json.loads function of the Python json module We apply functional programming to extract the data and simulate the paging with several http calls until we extract all the data.</p> 

<p>In reality it is not 100% functional programming because we use some variables for comfort and a better compression of the code, but it could be 100% functional. </p>

<p>To do the pagination we use the recursion calling the main function, scrap_danmurphys as many times as there are pages</p>

<p>To execute the function we call
<b>scrap_danmurphys (1, "")</b> to get all the pages in an array.</p>
<p>The first parameter of this function is the initial pagna that we want to scrape and the second parameter is the last page. If the second parameter is left blank, the function navigates through all the pages.</p>

<p>In this example we generate a csv file from the array obtained also with functional programming</p>
