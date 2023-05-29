import requests
import random
from bs4 import BeautifulSoup


class scpClass:
  dict_scp={}
  def __init__(self):
    self.mannager()
  
  def set_objclass_scp(self):
    dict_object_class=self.get_scp_object_class()
    for key_object_class,values in dict_object_class.items():
      for v in values:
        for key_scp in self.dict_scp.keys():
          if v==key_scp:
            self.dict_scp[key_scp]['object_class']=key_object_class



  def get_scp_object_class(self):
    safe=[]
    euclid=[]
    keter=[]
    thaumiel=[]
    neutralized=[]
    apollyon=[]
    archon=[]
    list_links=['safe','euclid','keter','thaumiel','neutralized','apollyon','archon']
    dict_object_class={}
    for object_class in list_links:
      link=requests.get(f"https://scp-wiki.wikidot.com/system:page-tags/tag/{object_class}")
      soup=BeautifulSoup(link.content,'html.parser')
      for i in soup.find_all('div',class_='pages-list',id='tagged-pages-list'):
        for x in i.find_all('a',href=True):
          if object_class=='safe':
            safe.append(x.text)
          elif object_class=='euclid':
            euclid.append(x.text)
          elif object_class=='keter':
            keter.append(x.text)
          elif object_class=='thaumiel':
            thaumiel.append(x.text)
          elif object_class=='neutralized':
            neutralized.append(x.text)
          elif object_class=='apollyon':
            apollyon.append(x.text)
          elif object_class=='archon':
            archon.append(x.text)
         
      dict_object_class.update({'Safe':safe,'Euclid':euclid,'Keter':keter,'Thaumiel':thaumiel,'Neutralized':neutralized,'Apollyon':apollyon,'Archon':archon})

    return dict_object_class
   

  
  
  def get_name_seriesI(self):
    lista=[]
    link=requests.get("https://scp-wiki.wikidot.com/scp-series")
    soup=BeautifulSoup(link.content,'html.parser')
    a=soup.find_all('li')
    for num in range(1,1000):
      if num<10:
        scp_num=f'00{num}'
      elif num<100:
        scp_num=f'0{num}'
      else:
        scp_num=num
      for i in a:
        for b in i.find_all('a',string=f'SCP-{scp_num}'):
          lista.append(i.text.split(' ',2))  
      for values in lista:
        self.dict_scp.update({values[0]:{'item':values[0],'name':values[-1],'object_class':'Unknown','scpoints':'','image':'','claims': 0}})



  def set_image(self):
    for key in self.dict_scp.keys():
        link=f"https://the-scp.foundation/temp/{key.lower()}.jpg"
        response=requests.get(link)
        if response.status_code==404:
          self.dict_scp[key]['image']=''
          #with open('have_no_image.txt','a') as file:
          #file.writelines(f'{self.dict_scp[key]}\n')
        else:
          self.dict_scp[key]['image']=link

  def set_scpoints(self):
    for key in self.dict_scp.keys():
      if self.dict_scp[key]['object_class']=="Safe":
        self.dict_scp[key]['scpoints']=random.randrange(500,1000,10)
      elif self.dict_scp[key]['object_class']=="Euclid":
        self.dict_scp[key]['scpoints']=random.randrange(3000,5000,10)
      elif self.dict_scp[key]['object_class']=="Keter":
        self.dict_scp[key]['scpoints']=random.randrange(10000,20000,10)
      elif self.dict_scp[key]['object_class']=="Thaumiel":
        self.dict_scp[key]['scpoints']=random.randrange(30000,40000,10)
      elif self.dict_scp[key]['object_class']=="Apollyon":
        self.dict_scp[key]['scpoints']=random.randrange(50000,59999,10)
      elif self.dict_scp[key]['object_class']=="Archon":
        self.dict_scp[key]['scpoints']=random.randrange(60000,65000,10)
      elif self.dict_scp[key]['object_class']=="Neutralized":
        self.dict_scp[key]['scpoints']=random.randrange(100,499,10)
      else:
        self.dict_scp[key]['scpoints']=random.randrange(40000,49999,10)

  def mannager(self):
    self.get_name_seriesI()
    self.set_objclass_scp()
    self.set_image()
    self.set_scpoints()