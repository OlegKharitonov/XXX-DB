import os
import requests
from bs4 import BeautifulSoup as BS
from Zcheckcyrr import has_cyrillic
from testtime import correct_time
from GetPic import getimage
import re


xfilms = []
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44', 'accept': '*/*'}

def getcontest_TPL (new, pathim):
    req = requests.get(new, headers = HEADERS)
    req.encoding = 'utf-8'
    req = req.text
    soupre = BS(req, 'html.parser')

    items = []
    pics = []
    scen = []
    title = ''
    aka = ''
    year = ''
    year2 = ''
    country = ''
    genre = ''
    time = ''
    regie = ''
    studio = ''
    cast = ''
    scenes = ''
    desc = ''

    inf = soupre.find('div', id="download").get_text(strip=True)
    des = soupre.find('table', id="details").get_text
    info = soupre.find('table', id="details").get_text(strip=True)
    ddes = str(des).split('">')

    if '/ ' in inf:
        title = inf.split('/')[0].replace('Скачать', '').strip()
    else:
        title = inf.split('(')[0].replace('Скачать', '').strip()

    if '[' in title:
        title = title.split('[')[0].strip()

    if '|' in title:
        title = title.split('|')[0].strip()

    title = title.replace('.torrentДобавить trupornolabs.org в поисковую строку', '')

    if has_cyrillic(title):
        if '/' in inf and '(' in inf:
            title = inf.split('/', 1)[1].split('(')[0].replace('Скачать', '').strip()
        if '(' in inf:
            title = inf.split('(', 1)[1].split(')')[0].replace('Скачать', '').strip()

    print(title)

    #
    # try:
    #     year = re.findall(r'\d\d\d\d', inf)[0]
    # except:
    #     year = ''

    for de in ddes:
        de = de.replace('</span>','').split('<br>')[0].strip()
        print(de)
        if 'Год' in de:
            year = re.findall(r'\d\d\d\d', de)[0]
            # year2 = de.split(':')[1].replace('г.', '').strip()
        if 'Страна' in de or 'Country' in de:
            country = de.split(':')[1].replace('Франция', 'France').replace('Италия', 'Italy').\
                replace('Германия', 'Germany').\
                replace('США', 'USA').replace('pic', '').strip()
            if '<br/>' in country:
                country = country.split('<br/>')[0].strip()
        if 'Жанр' in de:
            genre = de.split(':')[1].strip()
            if '<br/>' in genre:
                genre = genre.split('<br/>')[0].strip()
        if 'Продолжительность' in de or 'Duration' in de:
            tm = de.split(':', 1)[1].strip()
            if '<br/>' in tm:
                tm = tm.split('<br/>')[0].strip()
            time = correct_time(tm)
        if 'Режиссер' in de or 'Directed' in de or 'Director' in de:
            regie = de.split(':')[1].replace(' &amp;', ',').strip()
            if '<br/>' in regie:
                regie = regie.split('<br/>')[0].strip()
        if 'Студия' in de or 'Studio' in de:
            try:
                studio = de.split(':')[1].split('<br>')[0].strip()
            except:
                studio = ''
            if '<br/>' in studio:
                studio = studio.split('<br/>')[0].strip()
        if 'В ролях' in de or 'Cast:' in de or 'Cast :' in de:
            cast = de.split(':', 1)[1].replace('<br>', ',').strip()
            if '<br/>' in cast:
                cast = cast.replace('<br/>', ',').replace(' ,', ',').strip()
            if ',' in cast[0:1]:
                cast = cast[1:].replace('  ', ' ').strip()
            if '<hr/>' in cast:
                cast = cast.split('<hr/>')[0].strip()
            if '<span' in cast:
                cast = cast.split('<span')[0].strip()
        if 'Описание' in de or 'Description' in de:
            desc = de.split(':')[1].strip()
            if '<br/>' in desc:
                desc = desc.replace('<br/>', ',').replace(' ,', ',').strip()
            if ',' in desc[0:1]:
                desc = desc[1:].replace('  ', ' ').strip()
        if 'Scene' in de:
            scenes = de.split(':')[1].strip()
            if '<br/>' in scenes:
                scenes = scenes.replace('<br/>', ',').replace(' ,', ',').strip()
            if ',' in scenes[0:1]:
                scenes = scenes[1:].replace('  ', ' ').strip()
        if 'img src' in de and 'fastpic' in de :
            pc = de.replace('<img src="', '').split('"/')[0].strip()
            pics.append(pc)
        if 'img src' in de and 'images2' in de :
            pc = de.replace('<img src="', '').split('"/')[0].strip()
            pics.append(pc)

    if soupre.find('div', class_="hidewrap"):
        p = soupre.find('div', class_="hidewrap")
        ppp = p.find_all('a')
        for ii in ppp:
            pics.append(ii.get('href'))

    pics = set(pics)
    print(pics)

    def picnames(title, year):
        pn = title + ' ' + year
        ims = [pn + ' cover', pn + ' scenes', pn + ' 01', pn + ' 02', pn + ' 03', pn + ' 04', pn + ' 05', pn + ' 06', pn + ' 07', pn + ' 08', pn + ' 09', pn + ' 10', pn + ' 11', pn + ' 12', pn + ' 13', pn + ' 14', pn + ' 15']
        return ims

    ims = picnames(title, year)
    cover = ims[0]
    backcover = ''
    pic_name = ims[0].replace(' cover','')

    imagelist = list(zip(pics, ims))
    print(imagelist)

    for imm in imagelist:
        print(imm)
        os.chdir(pathim)
        getimage(imm)

    xfilms.append({
        'title': title,
        'aka': aka,
        'year': year,
        'country': country,
        'studio': studio,
        'director': regie,
        'stars': cast,
        'genre': genre,
        'scenes': scenes,
        'time': time,
        'description': desc,
        'info': '',
        'cover': cover,
        'backcover': backcover,
        'pics': pic_name
    })

    return xfilms

# getcontest (new, pathim)