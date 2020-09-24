from bs4 import BeautifulSoup
from files import getResponse, getStartIndex, saveToJson
from datetime import datetime


def start():
    url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
    resp = BeautifulSoup(getResponse(url, '', 'list'), 'html.parser')
    movieListHTML = resp.findAll('tbody', {"class": "lister-list"})
    movieList = movieListHTML[0].findAll('tr')
    startIndex = getStartIndex()
    print("\n\nNOTE #1:\
        \n\tIf html files already exist in ./responses, they will be used!\
        \n\tIf it's not prefered, DELETE the whole ./responses folder! (!!!NOT RECOMMENDED!!!)\
        \n\tConfirm by pressing ENTER key!")
    input()
    print("\n\nNOTE #2:\
        \n\tIf data of movies is already saved in ./data/data.json, they won't be over-written!\
        \n\tIf it's not prefered, DELETE the whole ./data folder!\
        \n\tConfirm by pressing ENTER key!")
    input()
    print("\n\nData of "+str(startIndex*10) +
          " already saved in ./data/data.json.")
    for p in range(startIndex, 25):
        movieJson = []
        for i in range(0, 10):
            c = p*10+i
            print(str(c+1)+'. starting to scrape...')
            movieJson.append(scrapeOut(movieList[c]))
            print(str(c+1)+'. scraping done!!!!!!!!!!')
        print('starting to save first {} movies...'.format(str((p+1)*10)))
        saveToJson(movieJson)
        print('first {} movies saved!!!!!!!!'.format(str((p+1)*10)))
    print("\n\nAll data crawled and saved into ./data/data.json")
    return


def scrapeOut(movie):
    base = "https://www.imdb.com/"
    theMovie = {}
    # IMDB ID
    theMovie['imdbID'] = movie.findAll('a')[0].attrs['href'].split('/')[-2]
    imdb = theMovie['imdbID']
    # Movie page
    url = base+movie.findAll('a')[0].attrs['href']

    resp = BeautifulSoup(getResponse(
        url, imdb, 'main'), 'html.parser')
    # Rank
    theMovie['rank'] = movie.findAll('span', {'name': 'rk'})[
        0].attrs['data-value']
    # Title
    theMovie['title'] = movie.findAll('td', {'class': 'titleColumn'})[
        0].findAll('a')[0].text
    # Tagline
    theMovie['taglines'] = []
    tags = BeautifulSoup(getResponse(
        url+'taglines', imdb, 'taglines'), 'html.parser')
    tags = tags.findAll('div', {'class': 'soda'})
    notag = "It looks like we don't have any Taglines for this title yet."
    if notag not in tags[0].text:
        for tag in tags:
            theMovie['taglines'].append(tag.text.strip())
    else:
        pass
    # Details:
    details = resp.findAll('div', {'id': 'titleDetails'})[
        0].findAll('div', {'class': 'txt-block'})
    for div in details:
        data = div.findAll('a')
        if 'Country:' in div.text:
            theMovie['country'] = []
            for c in data:
                theMovie['country'].append(c.text.strip())
        if 'Language:' in div.text:
            theMovie['language'] = []
            for c in data:
                theMovie['language'].append(c.text.strip())
        if 'Budget:' in div.text:
            theMovie['budgetIn$'] = div.text.split()[0].split(
                ':')[-1].replace(',', '').replace('$', '')
    # Rating info
    theMovie['ratingInfo'] = {}
    theMovie['ratingInfo']['imdbRating'] = resp.findAll(
        'span', {'itemprop': 'ratingValue'})[0].text
    theMovie['ratingInfo']['bestRating'] = resp.findAll(
        'span', {'itemprop': 'bestRating'})[0].text
    theMovie['ratingInfo']['ratingCount'] = resp.findAll(
        'span', {'itemprop': 'ratingCount'})[0].text.replace(',', '')
    # Duration
    theMovie['runtime'] = resp.findAll(
        'time')[0].text.strip().replace('h ', ':').replace('min', '')+':00'
    # Genre
    genreSet = resp.findAll('div', {'class': 'subtext'})[0].findAll('a')
    theMovie['genre'] = []
    for i in range(len(genreSet)-1):
        theMovie['genre'].append(genreSet[i].text)
    # Release info
    release = resp.findAll('a', {'title': 'See more release dates'})[
        0].text.split('(')
    theMovie['release'] = {}
    theMovie['release']['country'] = release.pop().replace(')', '').strip()
    theMovie['release']['date'] = makeDate(release[0].strip())
    # Plot summary
    theMovie['plotSummary'] = resp.findAll(
        'div', {'class': 'summary_text'})[0].text.strip()
    # Keywords
    theMovie['keyword'] = []
    words = BeautifulSoup(getResponse(
        url+'keywords', imdb, 'keywords'), 'html.parser')
    words = words.findAll('div', {'class': 'sodatext'})
    for word in words:
        theMovie['keyword'].append(word.findAll('a')[0].text)
    # Credits
    theMovie['credit'] = {}
    credit = BeautifulSoup(getResponse(
        url+'fullcredits', imdb, 'credits'), 'html.parser').findAll('div', {'id': 'fullcredits_content'})[0].findAll('table')
    # Director
    directors = credit[0].findAll('td', {'class': 'name'})
    theMovie['credit']['director'] = []
    for director in directors:
        theMovie['credit']['director'].append(
            director.findAll('a')[0].text.strip())
    # writer
    writers = credit[1].findAll('td', {'class': 'name'})
    theMovie['credit']['writer'] = []
    for writer in writers:
        if 'more credit' not in (writer.text):
            theMovie['credit']['writer'].append(
                writer.findAll('a')[0].text.strip())
    # Cast
    cast = credit[2].findAll('tr')
    theMovie['credit']['cast'] = []
    for tr in cast:
        if not tr.findAll('td', {'class': 'castlist_label'}):
            actor = {}
            actorInfo = tr.findAll('td')
            actor['name'] = actorInfo[1].findAll(
                'a')[0].text.strip().replace('\n', ' ')
            if actorInfo[-1].findAll('a'):
                char = actorInfo[-1].findAll('a')[
                    0].text.strip().replace('\n', ' ')
            else:
                char = actorInfo[-1].text.strip().replace('\n', ' ')
            actor['character'] = ' '.join(char.split())
            theMovie['credit']['cast'].append(actor)
    # company
    company = BeautifulSoup(getResponse(
        url+'companycredits', imdb, 'company'), 'html.parser')
    theMovie['credit']['productionCompany'] = []
    company = company.findAll('ul', {'class': 'simpleList'})[
        0].findAll('a')
    for i in range(len(company)):
        theMovie['credit']['productionCompany'].append(company[i].text)
    return theMovie


def makeDate(release):
    release = release.split()
    if len(release) == 1:
        return release[0]+'-01-01'
    if len(release) == 2:
        release.insert(0, '1')
    release = ' '.join(release)
    date = datetime.strptime(release, '%d %B %Y')
    return date.strftime('%Y-%m-%d')


if __name__ == "__main__":
    start()
