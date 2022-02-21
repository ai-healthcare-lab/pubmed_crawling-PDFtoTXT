# pubmed_crawling-PDFtoTXT
클린코드가 아니므로 이해하기 어렵고 PDFMiner라는 패키지에게 전적으로 의존하므로 이를 먼저 이해하는게 좋을 것 같아 링크를 먼저 첨부합니다. 

# PDFMiner Information
PDFMiner의 구조와 어떻게 동작하는지에 대한 정리글입니다. 
```c

https://www.unixuser.org/~euske/python/pdfminer/programming.html

```

## installation

```c

pip install -r requirements.txt

```



## layout
PDF는 Word나 HTML과 달리 문장이나 단락과 같은 논리적 구조로 구성되어 있지 않습니다. 이러한 특성으로 PDFMiner는 위치 정보를 이용하여 텍스트를 추출합니다. 

이러한 특성으로 PDFtoTXT 과정에서 필요없는 부분을 쉽게 필터링 하지 못 하는데 이를 위해서 각 문장이 어떤 위치에 존재하는지 알기 위한 코드입니다.
PDFMiner는 추출 과정에서LTTextBox라는 개념을 도입하여 text chunk group을 직사각형 영역으로 구분합니다. layout.ipynb를 실행하면 x1,x2,y1,y2 총 4개의 좌표로 문장, 문단끼리 구분이 됩니다. 
![initial](https://user-images.githubusercontent.com/84623098/154981111-506e1b76-7e99-40ee-ab72-2a3017ebd7a3.png)

![added](https://user-images.githubusercontent.com/84623098/154982604-35c462df-c39b-463a-88cd-d54dd533b338.png)
```c

if instance(element, LTTextBoxHorizontal):
  if 70 < element.bbox[1] < 745 and element.bbox[2] > 33:

```
위치정보를 확인하고 위 코드와 같이 조건문을 이용하여 걸러내면 되겠습니다. 



