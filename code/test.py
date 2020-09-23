from bs4 import BeautifulSoup


with open('test.html', 'r', encoding='utf8') as f:

    contents = f.read()
    soup = BeautifulSoup(contents, 'lxml')

        