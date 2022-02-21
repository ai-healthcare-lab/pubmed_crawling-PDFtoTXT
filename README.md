# pubmed_crawling-PDFtoTXT

## installation

```c

pip install -r requirements.txt

```
## layout
pdf는 Word나 HTML과 달리 문장이나 단락과 같은 논리적 구조로 구성되어 있지 않습니다. 
pdfminer는 위치 정보를 이용하여 텍스트를 추출합니다. 

이를 위해서 각 문장이 어떤 위치에 존재하는지 알기 위한 코드입니다.
실행하면 x1,x2,y1,y2 총 4개의 좌표로 문장, 문단끼리 구분이 됩니다. 
![initial](https://user-images.githubusercontent.com/84623098/154981111-506e1b76-7e99-40ee-ab72-2a3017ebd7a3.png)



# pdfminer information
누군가 이 pdfminer를 이용할 때 이해하기 좋을 것 같아 적어놓았습니다.
pdfminer의 구조와 어떻게 동작하는지에 대한 정리글입니다. 
```c

https://www.unixuser.org/~euske/python/pdfminer/programming.html

```
