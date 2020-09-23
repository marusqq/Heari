from bs4 import BeautifulSoup


with open('test.html', 'r', encoding='utf8') as f:

    contents = f.read()
    soup = BeautifulSoup(contents, 'lxml')


    #https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-all-next-and-find-next
    for article in soup.find_all('article'):
        title = article.find('h3')
        link = title.parent
        long_title = link.descendants

        for a in long_title:
            print(a)  

        print(long_title)
        print(title.text)
        print(link['href'])
        quit()