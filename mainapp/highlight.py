from PIL import Image
import string

def highlight(files, texts_list, keyword_list):
    for i,pages in enumerate(files):
         for j, page in enumerate(pages):
         invert_img = page.load()

