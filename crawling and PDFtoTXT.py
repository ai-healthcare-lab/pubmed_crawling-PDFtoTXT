#!/usr/bin/env python
# coding: utf-8

# In[5]:


from urllib.request import Request, urlopen
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTTextBoxHorizontal
from bs4 import BeautifulSoup
import urllib.request   
import urllib.parse
import requests

    
    
def SearchDocument(Search_word, LastPage):
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

    pageNum = 1  
    count = 0  
    lst_2 = []
    
    while pageNum < LastPage + 1:  
        
        lst = []

        url = f'https://pubmed.ncbi.nlm.nih.gov/?term={Search_word}&filter=simsearch2.ffrft&page={pageNum}'   
        html = urllib.request.urlopen(url).read()         
        soup = BeautifulSoup(html, 'html.parser')        
        title = soup.find_all(class_='docsum-title')     
        print(f'-----{pageNum}페이지 결과입니다.-----')
        
        for firstpage in title:
            sub_url = "https://pubmed.ncbi.nlm.nih.gov" + firstpage.attrs['href']    
            sub_resp = requests.get(sub_url, headers = headers)
            sub_soup = BeautifulSoup(sub_resp.text, 'html5lib')
            sub_sel = "div.full-view > div.full-text-links-list > a"  
            sub_titles = sub_soup.select(sub_sel)

            for secondpage in sub_titles:
#                 print(j)                                            # journal 이름 알 수 있음
                hypertext = secondpage.attrs['href'].split('/')  
                    
                for key_word in hypertext:
                    if 'pmc' in key_word:                            # hypertext 속에서 원하는 journal의 논문 찾기위해 키워드를 입력한다.                  
                        lst.append(secondpage.attrs['href'])
                                                
        for m in range(len(lst)):

            ssub_url = lst[m]
            req = Request(ssub_url, headers=headers)
            webpage = urlopen(req).read()
            soup = BeautifulSoup(webpage, 'html.parser')   
            sel = soup.select("div.format-menu > ul > li > a")

            for hypertext_2 in sel:
                if ".pdf" in hypertext_2.attrs['href']:
                    hypertext_2 = hypertext_2.attrs['href']
                    downloadlink=("https://www.ncbi.nlm.nih.gov"+hypertext_2)
                    lst_2.append(downloadlink)           
                    print(downloadlink)
            
        pageNum += 1
        
    return lst_2


# pdf 다운 / SearchDocument의 return 값인 다운로드 링크들이 담긴 리스트를 받는다.    
def Downloader(List):
    count = 0
    lst = []
    
    for k in range(len(List)):
        pdf_url = List[k]
        count += 1
        save_name = "C:/crawling/pdf_" + str(count) +".pdf"     
        # pdf 저장경로입니다, 편의를 위해 count를 이용해서 이름을 붙였습니다.
        
        download_file = requests.get(pdf_url, headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1: Win64: x64) AppleWebKit/537.36 (KHTML, Like Gecko) Chrome/73.0.3683.86 Safari/537.36'})
        
        document = open(save_name, 'wb')
        document.write(download_file.content)
        document.close()
        
        lst.append(save_name)
        print(save_name + "이 저장되었습니다.")
    print("다운로드가 끝났습니다.")
    return lst

# 변환 / Downloader를 통해 return 값인 리스트로 저장된 주소들을 받아서 동작한다.
def parsedocument(List):
    lines = []
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for k in List:                                              
        fh = open (k,'rb') 
        # 여기서 k는 pdf 저장경로입니다. 
            
        lines = []
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)


        for page in PDFPage.get_pages(fh):
                interpreter.process_page(page)
                layout = device.get_result()
                for element in layout:
                    if isinstance(element, LTTextBoxHorizontal):
                        if 70 < element.bbox[1] < 745 and element.bbox[2] > 33:  
                            # x1,x2,y1,y2 좌표를 이용해 불필요한 영역을 제거한다
                            
                            lines.append(element.get_text())

        for i in range(len(lines)):
            lines[i]=lines[i].strip()
            lines[i]=lines[i].replace('-\n','')
            lines[i]=lines[i].replace('\n',' ')
            lines[i]=lines[i].replace('  ',' ')

        lines=' '.join(lines)
        
        for ab in ['abstract', 'Abstract', 'ABSTRACT']:
            if ab in lines:
                index = lines.find(ab)
                pass
            
        for ack in ['acknowledgements', 'Acknowledgements', 'ACKNOWLEDGEMENTS','acknowledgments', 'Acknowledgments', 'ACKNOWLEDGMENTS']:
            if ack in lines:
                index_2 = lines.rfind(ack)
                break
            else:
                for ref in ['references','References','REFERENCES']:
                    if ref in lines:
                        index_2 = lines.rfind(ref)
                        pass 
                    
        result = lines[index:index_2]
        # abstract 이전, acknowledgement 혹은 reference 이후 부분 필터링
        
        with open(k[:-4]+'.txt', mode='w', encoding='UTF-8') as output:    # 저장경로, 편의를 위해서 전 count를 매개변수로 받아 사용하였습니다.
            output.write(result)
            
        print(k+"가 변환되었습니다.")                                      # k == pdf 저장경로
    print("변환이 끝났습니다.")


def main():
    
    searchWord = urllib.parse.quote_plus(input('검색어를 입력하세요:'))  # 검색할 단어
    pageNum = int(input('몇 페이지까지 크롤링할까요? :'))   # 몇 페이지까지 검색할지 설정
    
    SearchList = SearchDocument(searchWord, pageNum)  
    DownloadList = Downloader(SearchList)
    parsedocument(DownloadList)
            
main()


# In[ ]:




