# pubmed_crawling-PDFtoTXT
Clean Code가 아니므로 이해하기 어렵고 PDFMiner라는 패키지에게 전적으로 의존하므로 이를 먼저 이해하는게 좋을 것 같아 링크를 먼저 첨부합니다. 

# PDFMiner Information
PDFMiner의 구조와 어떻게 동작하는지에 대한 정리글입니다. 
```c

https://www.unixuser.org/~euske/python/pdfminer/programming.html

```

## installation

```c

pip install -r requirements.txt

```
## Final version 
실행하면 두 개의 input 값을 주어야 합니다. 
첫 번째는 PubMed 에서 크롤링할 검색어를 입력해야하며 두 번째로는 몇 페이지까지 검색을 하는지 입니다. 
PubMed는 1000 페이지까지 크롤링이 가능합니다. 


## layout
PDF는 Word나 HTML과 달리 문장이나 단락과 같은 논리적 구조로 구성되어 있지 않습니다. 이러한 특성으로 PDFMiner는 위치 정보를 이용하여 텍스트를 추출합니다. 

 PDFtoTXT 과정에서 페이지 번호나 저널 표시 등 분석에 불필요한 부분을 필터링하기 위한 방법은 다음과 고안하였습니다. 
 
PDFMiner는 추출 과정에서 LTTextBox라는 개념을 도입하여 text chunk group을 직사각형 영역으로 구분합니다. 
해당 text chunk group은 텍스트 사이의 거리로 구분이 되며 반드시 문단이지는 않습니다.

밑 사진에서는 빨간색 영역의 사각형이 LTTextBox 입니다. 
![initial](https://user-images.githubusercontent.com/84623098/154981111-506e1b76-7e99-40ee-ab72-2a3017ebd7a3.png)

layout.ipynb를 실행하면 이처럼 LTTextBox의 위치 정보인 총 4개의 좌표( x1,x2,y1,y2 )를 얻을 수 있습니다.

![added](https://user-images.githubusercontent.com/84623098/154982604-35c462df-c39b-463a-88cd-d54dd533b338.png)
```c

if instance(element, LTTextBoxHorizontal):
  if 70 < element.bbox[1] < 745 and element.bbox[2] > 33:

```

위치 정보를 확인하고 parsedocument 함수의 해당 조건문을 이용하여 걸러내면 되겠습니다. 



