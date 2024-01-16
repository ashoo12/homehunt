import unicodedata
import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd

price_list=[]
bed_list=[]
bath_list=[]
area_list=[]
location_list=[]

dubizzle_url="https://abudhabi.dubizzle.com/property-for-rent/residential/?price__gte=20000&price__lte=50000&bedrooms=1&bedrooms=2"
headers={
    "Accept-Language":"en-US,en;q=0.9",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}
# reuesting for the url of webpage we want to extract data from
response=requests.get(dubizzle_url,headers=headers)
webpage=response.text

soup=BeautifulSoup(webpage,"html.parser")

prices=soup.find_all(class_="sc-fBWQRz sc-jGKxIK fEbvgi cKudTj")
for price in prices:
    price_list.append(price.get_text())

beds=soup.find_all(class_="sc-bizigk fZTTxQ")
for bed in beds:
    cleaned_list=unicodedata.normalize("NFKD",bed.get_text()).replace('\xa0','')
    bed_list.append(cleaned_list[0:5])
    bath_list.append(cleaned_list[5:11])
    area_list.append(cleaned_list[11:])

locations=soup.find_all(class_="MuiTypography-root MuiTypography-body1 MuiTypography-noWrap css-ncavm4")
for location in locations:
    location_list.append(location.get_text())

# now we are writing all are data in our csv file
data=[price_list,bed_list,bath_list,area_list,location_list]
csv_file_path="rentals.csv"
with open(csv_file_path,mode="w",newline="") as f:
     writer=csv.writer(f)
     # this line is for adding a header coulumn
     writer.writerow(["price","bed","bath","area","location"])
     # i have zipped the data so it will come in column format
     transposed_data = zip(*data)
     writer.writerows(transposed_data)

# if u want to save this data in excel format
data={
    "price":price_list,
    "bedrooms":bed_list,
    "bathrooms":bath_list,
    "area":area_list,
    "location":location_list
}
df=pd.DataFrame(data)
excel_file_path="rentals.xlsx"
df.to_excel(excel_file_path,index=True)