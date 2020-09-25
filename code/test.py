from bs4 import BeautifulSoup
import sys
import utilities as util
import requests


from_file = True

if from_file:


    with open('test.html', 'r', encoding = 'utf8') as f:
        article = []
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')

        #look for more info
    for meta in soup.find_all('meta'):
        
        meta_property = meta.get('property')
        if meta_property:
            
            #category
            if str(meta_property) == "article:section":
                if meta['content']:
                    print(meta['content'])
                    
            #publish time
            elif str(meta_property) == "article:published_time":
                if meta['content']:
                    print(meta['content'])

            #image
            elif str(meta_property) == "og:image":
                if meta['content']:
                    print(meta['content'])
        input()

        


else:

    #url = 'https://www.lrytas.lt/lietuvosdiena/kriminalai/2020/09/24/news/r-daskeviciaus-zmogzudystes-pedsakai-atvede-pas-buvusi-biciuli-kaip-is-eilinio-torpedos-jis-virto-mafijos-sulu-16455629/'
    url = 'https://www.lrytas.lt/sveikata/medicinos-zinios/2020/09/24/news/po-koronaviruso-protrukio-lietuvoje-a-verygos-kreipimasis-i-savivaldybes-su-vienu-prasymu-16452763/'
    try:
        page = requests.get(url)

    except:
        print('Error with:', url)
        error_type, error_obj, error_info = sys.exc_info()
        print('Exc info:', error_type, error_info, error_obj)
        print('Error line', error_info.tb_lineno)

    util.save_in_file(text_to_save = page.text, filename = 'test.html', testing = True)
    quit()

    soup = BeautifulSoup(page.text, "lxml")
    





        

