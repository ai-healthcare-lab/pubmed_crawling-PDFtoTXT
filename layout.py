#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from typing import Iterable

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTItem

def show_ltitem_hierarchy(o: LTItem, depth=0):                                
    """Show location and text of LTItem and all its descendants"""
    if depth == 0:
        print('element                        x1  y1  x2  y2   text')
        print('------------------------------ --- --- --- ---- -----')
    
    print(
        f'{get_indented_name(o, depth):<30.30s} '
        f'{get_optional_bbox(o)} '
        f'{get_optional_text(o)}'
    )

    if isinstance(o, Iterable):
        for i in o:
            show_ltitem_hierarchy(i, depth=depth + 1)


def get_optional_text(o: LTItem) -> str:
    """Text of LTItem if available, otherwise empty string"""
    if hasattr(o, 'get_text'):
        return o.get_text().strip()
    return ''


def get_indented_name(o: LTItem, depth: int) -> str:
    """Indented name of LTItem"""
    return '  ' * depth + o.__class__.__name__


def get_optional_bbox(o: LTItem) -> str:
    """Bounding box of LTItem if available, otherwise empty string"""
    if hasattr(o, 'bbox'):
        return ''.join(f'{i:<4.0f}' for i in o.bbox)
    return ''


file_path = 'C:/crawling/jaemin2.pdf'           # 파일경로 
show_ltitem_hierarchy(extract_pages(os.path.expanduser(file_path)))
extract_pages(file_path)


# In[1]:


from pdfminer.high_level import extract_pages
for page_layout in extract_pages("C:/crawling/pdf_3.pdf"):  # 파일 경로
    for element in page_layout:
#         print(element.bbox)
            print(element)


# In[ ]:




