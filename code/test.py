from bs4 import BeautifulSoup
import sys
import utilities as util
import requests

def split_time(time_with_date, newspaper):
    if newspaper == 'delfi':
        s_time = time_with_date.split('T')
        date = s_time[0]
        s_time = s_time[1].split('+')
        time = s_time[0]
    
    return date, time

from_file = False

if from_file:


    with open('test.html', 'r', encoding = 'utf8') as f:

        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')

else:

    url = "https://www.delfi.lt/verslas/transportas/kaunietis-sena-automobili-iskeite-i-paspirtukus-bet-liko-be-800-eur-kompensacijos-lesos-istirpo-per-pora-dienu.d?id=85305323"
    #url = "https://www.delfi.lt"
    try:
        page = requests.get(url)

    except:
        print('Error with:', url)
        error_type, error_obj, error_info = sys.exc_info()
        print('Exc info:', error_type, error_info, error_obj)
        print('Error line', error_info.tb_lineno)

    soup = BeautifulSoup(page.text, "lxml")
    
    for meta in soup.find_all("meta"):
        meta_type = meta.get('name')
        if meta_type:
            if str(meta_type) == "cXenseParse:recs:author":
                article_author = meta['content']

            elif str(meta_type) == "cXenseParse:recs:publishtime":
                date, time = split_time(meta['content'], 'delfi')
                
    print(date)
    print(time)
    print(article_author)

    util.save_in_file(text_to_save = page.text, filename = 'test.html', testing = True)




        

