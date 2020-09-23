from bs4 import BeautifulSoup


with open('test.html', 'r', encoding='utf8') as f:

    contents = f.read()
    soup = BeautifulSoup(contents, 'lxml')

    #https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-all-next-and-find-next
    for article in soup.find_all('article'):
        authors = []
        for author in article.find_all("p"):
            p_class = author.get('class')
            if "author" in str(p_class):
                authors.append(author.text)
        title = article.find('h3')
        link = title.parent
        long_title = title.find_next('p')

        print(title.text)
        print(long_title.text)
        print(link['href'])
        quit()