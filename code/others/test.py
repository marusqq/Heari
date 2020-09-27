from bs4 import BeautifulSoup
import sys
import utilities as util
import requests


from_file = False

if from_file:


    with open('test.html', 'r', encoding = 'utf8') as f:
        article = []
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')

    for article in soup.find_all('div', class_ = "one-article"):

        title = article.find('a')['title'].rstrip(' ')

        link = article.find('a')['href']

        img = article.find('img')['src']

        category = article.find('a', class_ = 'cat').text
        
        second_title = article.find('p')
        second_title_class = second_title.get('class')
        if second_title_class:
            if 'visible-lg' in str(second_title_class):
                if title[len(title) - 1] in ['!', '.', '?']:
                    title = title + ' ' + second_title.text
                else:
                    title = title + '. ' + second_title.text

        


else:

    #url = 'https://www.lrytas.lt/lietuvosdiena/kriminalai/2020/09/24/news/r-daskeviciaus-zmogzudystes-pedsakai-atvede-pas-buvusi-biciuli-kaip-is-eilinio-torpedos-jis-virto-mafijos-sulu-16455629/'
    #url = 'https://www.vz.lt/verslo-aplinka/2020/09/25/del-koronaviruso-kai-kur-uzsienyje-balsavimas-vyks-tik-pastu'
    url = "https://www.vz.lt/paslaugos/2020/09/25/garantijas-uz-kelioniu-organizatoriu-prievoliu-ivykdymo-uztikrinimainvega-teiks-ir-luminor-bankui"
    
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
    





        

