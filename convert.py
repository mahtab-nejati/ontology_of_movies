from lxml.etree import Element, SubElement, QName, tostring
from files import readJson, saveOWL


def start():

    global kwInclude
    kwInclude = False

    print('\n\nDo you want to include keywords in the ontology? (Y/N) (!!!NOT REOMMENDED!!!)')
    ans = input().lower()
    if ans != "":
        if ans[0] == "y":
            pass
            kwInclude = not kwInclude

    movieIDs = []
    countries = []
    languages = []
    genres = []
    if kwInclude:
        keywords = []
    persons = []
    companies = []

    for movie in data:
        # getting MOVIEIDS
        movieIDs.append(movie['imdbID'])

        # getting COUNTRIES
        countries += movie['country'] + [movie['release']['country']]

        # getting LANGUAGES
        languages += movie['language']

        # getting GENRES
        genres += movie['genre']

        # getting KEYWORDS
        if kwInclude:
            keywords += movie['keyword']

        # getting PERSONS
        credit = movie['credit']
        persons += credit['director']+credit['writer']
        for name in credit['cast']:
            persons.append(name['name'])

        # getting COMPANIES
        companies += credit['productionCompany']

    collection = {}
    collection["movieIDs"] = list(set(movieIDs))
    collection["countries"] = list(set(countries))
    collection["languages"] = list(set(languages))
    collection["genres"] = list(set(genres))
    if kwInclude:
        collection["keywords"] = list(set(keywords))
    collection["persons"] = list(set(persons))
    collection["companies"] = list(set(companies))

    allElements = stepOne(collection)
    allElements = stepTwo(allElements)
    mergeElements(allElements)
    saveOWL('<?xml version="1.0" encoding="UTF-8"?>\n' +
            tostring(root, pretty_print=True).decode("utf-8"), "data_owl.owl")
    print("\n\nAll data converted to OWL and saved into ./ontology/data_owl.owl")


def stepOne(collection):

    allElements = []

    movieIDs = collection["movieIDs"]
    countries = collection["countries"]
    languages = collection["languages"]
    genres = collection["genres"]
    if kwInclude:
        keywords = collection["keywords"]
    persons = collection["persons"]
    companies = collection["companies"]

    # defining CLASSES
    classElements = Element("classElements")
    namedIndividualElements = Element("namedIndividualElements")
    subClassOfElements = Element("subClassOfElements")
    classAssertionElements = Element("classAssertionElements")
    hasNameElements = Element("hasNameElements")

    # CLASS TOP
    dec = SubElement(classElements, "Declaration")
    SubElement(dec, "Class", attrib={"IRI": "#Top"})

    # CLASS MOVIE
    dec = SubElement(classElements, "Declaration")
    SubElement(dec, "Class", attrib={"IRI": "#Movie"})
    sub = SubElement(subClassOfElements, "SubClassOf")
    SubElement(sub, "Class", attrib={"IRI": "#Movie"})
    SubElement(sub, "Class", attrib={"IRI": "#Top"})
    # defining MOVIES
    for i in range(len(movieIDs)):
        dec = SubElement(namedIndividualElements, "Declaration")
        SubElement(dec, "NamedIndividual", attrib={"IRI": "#"+movieIDs[i]})
        assertion = SubElement(classAssertionElements, "ClassAssertion")
        SubElement(assertion, "Class", attrib={"IRI": "#Movie"})
        SubElement(assertion, "NamedIndividual",
                   attrib={"IRI": "#"+movieIDs[i]})

    # CLASS COUNTRY
    dec = SubElement(classElements, "Declaration")
    SubElement(dec, "Class", attrib={"IRI": "#Country"})
    sub = SubElement(subClassOfElements, "SubClassOf")
    SubElement(sub, "Class", attrib={"IRI": "#Country"})
    SubElement(sub, "Class", attrib={"IRI": "#Top"})
    # defining COUNTRIES
    for i in range(len(countries)):
        country = countries[i].replace(
            ' ', '-').replace("'", '').replace('.', '')
        dec = SubElement(namedIndividualElements, "Declaration")
        SubElement(dec, "NamedIndividual", attrib={"IRI": "#"+country})
        assertion = SubElement(classAssertionElements, "ClassAssertion")
        SubElement(assertion, "Class", attrib={"IRI": "#Country"})
        SubElement(assertion, "NamedIndividual", attrib={"IRI": "#"+country})
        # HasName Assertions (DataProperty)
        assertion = SubElement(hasNameElements, "DataPropertyAssertion")
        SubElement(assertion, "DataProperty", attrib={"IRI": "#HasName"})
        SubElement(assertion, "NamedIndividual", attrib={"IRI": "#"+country})
        SubElement(assertion, "Literal").text = countries[i]

    # CLASS LANGUAGE
    dec = SubElement(classElements, "Declaration")
    SubElement(dec, "Class", attrib={"IRI": "#Language"})
    sub = SubElement(subClassOfElements, "SubClassOf")
    SubElement(sub, "Class", attrib={"IRI": "#Language"})
    SubElement(sub, "Class", attrib={"IRI": "#Top"})
    # defining LANGUAGES
    for i in range(len(languages)):
        language = languages[i].replace(
            ' ', '-').replace("'", '').replace('.', '')
        dec = SubElement(namedIndividualElements, "Declaration")
        SubElement(dec, "NamedIndividual", attrib={"IRI": "#"+language})
        assertion = SubElement(classAssertionElements, "ClassAssertion")
        SubElement(assertion, "Class", attrib={"IRI": "#Language"})
        SubElement(assertion, "NamedIndividual", attrib={"IRI": "#"+language})
        # HasName Assertions (DataProperty)
        assertion = SubElement(hasNameElements, "DataPropertyAssertion")
        SubElement(assertion, "DataProperty", attrib={"IRI": "#HasName"})
        SubElement(assertion, "NamedIndividual", attrib={"IRI": "#"+language})
        SubElement(assertion, "Literal").text = languages[i]

    # CLASS GENRE
    dec = SubElement(classElements, "Declaration")
    SubElement(dec, "Class", attrib={"IRI": "#Genre"})
    sub = SubElement(subClassOfElements, "SubClassOf")
    SubElement(sub, "Class", attrib={"IRI": "#Genre"})
    SubElement(sub, "Class", attrib={"IRI": "#Top"})
    # defining GENRES
    for i in range(len(genres)):
        genre = genres[i].replace(' ', '-').replace("'", '').replace('.', '')
        dec = SubElement(namedIndividualElements, "Declaration")
        SubElement(dec, "NamedIndividual", attrib={"IRI": "#"+genre})
        assertion = SubElement(classAssertionElements, "ClassAssertion")
        SubElement(assertion, "Class", attrib={"IRI": "#Genre"})
        SubElement(assertion, "NamedIndividual", attrib={"IRI": "#"+genre})
        # HasName Assertions (DataProperty)
        assertion = SubElement(hasNameElements, "DataPropertyAssertion")
        SubElement(assertion, "DataProperty", attrib={"IRI": "#HasName"})
        SubElement(assertion, "NamedIndividual", attrib={"IRI": "#"+genre})
        SubElement(assertion, "Literal").text = genres[i]

    # CLASS KEYWORD
    if kwInclude:
        dec = SubElement(classElements, "Declaration")
        SubElement(dec, "Class", attrib={"IRI": "#Keyword"})
        sub = SubElement(subClassOfElements, "SubClassOf")
        SubElement(sub, "Class", attrib={"IRI": "#Keyword"})
        SubElement(sub, "Class", attrib={"IRI": "#Top"})
        # defining KEYWORDS
        for i in range(len(keywords)):
            keyword = keywords[i].replace(
                ' ', '-').replace("'", '').replace('.', '')
            dec = SubElement(namedIndividualElements, "Declaration")
            SubElement(dec, "NamedIndividual", attrib={"IRI": "#"+keyword})
            assertion = SubElement(classAssertionElements, "ClassAssertion")
            SubElement(assertion, "Class", attrib={"IRI": "#Keyword"})
            SubElement(assertion, "NamedIndividual",
                       attrib={"IRI": "#"+keyword})

    # CLASS PERSON
    dec = SubElement(classElements, "Declaration")
    SubElement(dec, "Class", attrib={"IRI": "#Person"})
    sub = SubElement(subClassOfElements, "SubClassOf")
    SubElement(sub, "Class", attrib={"IRI": "#Person"})
    SubElement(sub, "Class", attrib={"IRI": "#Top"})
    # defining PERSONS
    for i in range(len(persons)):
        person = persons[i].replace(' ', '-').replace("'", '').replace('.', '')
        dec = SubElement(namedIndividualElements, "Declaration")
        SubElement(dec, "NamedIndividual", attrib={"IRI": "#"+person})
        assertion = SubElement(classAssertionElements, "ClassAssertion")
        SubElement(assertion, "Class", attrib={"IRI": "#Person"})
        SubElement(assertion, "NamedIndividual", attrib={"IRI": "#"+person})
        # HasName Assertions (DataProperty)
        assertion = SubElement(hasNameElements, "DataPropertyAssertion")
        SubElement(assertion, "DataProperty", attrib={"IRI": "#HasName"})
        SubElement(assertion, "NamedIndividual", attrib={"IRI": "#"+person})
        SubElement(assertion, "Literal").text = persons[i]

    # CLASS COMPANY
    dec = SubElement(classElements, "Declaration")
    SubElement(dec, "Class", attrib={"IRI": "#Company"})
    sub = SubElement(subClassOfElements, "SubClassOf")
    SubElement(sub, "Class", attrib={"IRI": "#Company"})
    SubElement(sub, "Class", attrib={"IRI": "#Top"})
    # defining COMPANIES
    for i in range(len(companies)):
        company = companies[i].replace(
            ' ', '-').replace("'", '').replace('.', '')
        dec = SubElement(namedIndividualElements, "Declaration")
        SubElement(dec, "NamedIndividual", attrib={"IRI": "#"+company})
        assertion = SubElement(classAssertionElements, "ClassAssertion")
        SubElement(assertion, "Class", attrib={"IRI": "#Company"})
        SubElement(assertion, "NamedIndividual", attrib={"IRI": "#"+company})
        # HasName Assertions (DataProperty)
        assertion = SubElement(hasNameElements, "DataPropertyAssertion")
        SubElement(assertion, "DataProperty", attrib={"IRI": "#HasName"})
        SubElement(assertion, "NamedIndividual", attrib={"IRI": "#"+company})
        SubElement(assertion, "Literal").text = companies[i]

    # defining PROPERTIES

    # OBJECT PROPERTIES
    objectPropertyElements = Element("objectPropertyElements")
    objectPropertyDomainElements = Element("objectPropertyDomainElements")
    objectPropertyRangeElements = Element("objectPropertyRangeElements")

    dec = SubElement(objectPropertyElements, "Declaration")
    SubElement(dec, "ObjectProperty", attrib={"IRI": "#ProductOf"})
    dom = SubElement(objectPropertyDomainElements, "ObjectPropertyDomain")
    SubElement(dom, "ObjectProperty", attrib={"IRI": "#ProductOf"})
    SubElement(dom, "Class", attrib={"IRI": "#Movie"})
    ran = SubElement(objectPropertyRangeElements, "ObjectPropertyRange")
    SubElement(ran, "ObjectProperty", attrib={"IRI": "#ProductOf"})
    SubElement(ran, "Class", attrib={"IRI": "#Country"})

    dec = SubElement(objectPropertyElements, "Declaration")
    SubElement(dec, "ObjectProperty", attrib={"IRI": "#SpokenIn"})
    dom = SubElement(objectPropertyDomainElements, "ObjectPropertyDomain")
    SubElement(dom, "ObjectProperty", attrib={"IRI": "#SpokenIn"})
    SubElement(dom, "Class", attrib={"IRI": "#Movie"})
    ran = SubElement(objectPropertyRangeElements, "ObjectPropertyRange")
    SubElement(ran, "ObjectProperty", attrib={"IRI": "#SpokenIn"})
    SubElement(ran, "Class", attrib={"IRI": "#Language"})

    dec = SubElement(objectPropertyElements, "Declaration")
    SubElement(dec, "ObjectProperty", attrib={"IRI": "#GenreIs"})
    dom = SubElement(objectPropertyDomainElements, "ObjectPropertyDomain")
    SubElement(dom, "ObjectProperty", attrib={"IRI": "#GenreIs"})
    SubElement(dom, "Class", attrib={"IRI": "#Movie"})
    ran = SubElement(objectPropertyRangeElements, "ObjectPropertyRange")
    SubElement(ran, "ObjectProperty", attrib={"IRI": "#GenreIs"})
    SubElement(ran, "Class", attrib={"IRI": "#Genre"})

    dec = SubElement(objectPropertyElements, "Declaration")
    SubElement(dec, "ObjectProperty", attrib={"IRI": "#ReleaseCountry"})
    dom = SubElement(objectPropertyDomainElements, "ObjectPropertyDomain")
    SubElement(dom, "ObjectProperty", attrib={"IRI": "#ReleaseCountry"})
    SubElement(dom, "Class", attrib={"IRI": "#Movie"})
    ran = SubElement(objectPropertyRangeElements, "ObjectPropertyRange")
    SubElement(ran, "ObjectProperty", attrib={"IRI": "#ReleaseCountry"})
    SubElement(ran, "Class", attrib={"IRI": "#Country"})

    if kwInclude:
        dec = SubElement(objectPropertyElements, "Declaration")
        SubElement(dec, "ObjectProperty", attrib={"IRI": "#HasKeyword"})
        dom = SubElement(objectPropertyDomainElements, "ObjectPropertyDomain")
        SubElement(dom, "ObjectProperty", attrib={"IRI": "#HasKeyword"})
        SubElement(dom, "Class", attrib={"IRI": "#Movie"})
        ran = SubElement(objectPropertyRangeElements, "ObjectPropertyRange")
        SubElement(ran, "ObjectProperty", attrib={"IRI": "#HasKeyword"})
        SubElement(ran, "Class", attrib={"IRI": "#Keyword"})

    dec = SubElement(objectPropertyElements, "Declaration")
    SubElement(dec, "ObjectProperty", attrib={"IRI": "#DirectorIs"})
    dom = SubElement(objectPropertyDomainElements, "ObjectPropertyDomain")
    SubElement(dom, "ObjectProperty", attrib={"IRI": "#DirectorIs"})
    SubElement(dom, "Class", attrib={"IRI": "#Movie"})
    ran = SubElement(objectPropertyRangeElements, "ObjectPropertyRange")
    SubElement(ran, "ObjectProperty", attrib={"IRI": "#DirectorIs"})
    SubElement(ran, "Class", attrib={"IRI": "#Person"})

    dec = SubElement(objectPropertyElements, "Declaration")
    SubElement(dec, "ObjectProperty", attrib={"IRI": "#WriterIs"})
    dom = SubElement(objectPropertyDomainElements, "ObjectPropertyDomain")
    SubElement(dom, "ObjectProperty", attrib={"IRI": "#WriterIs"})
    SubElement(dom, "Class", attrib={"IRI": "#Movie"})
    ran = SubElement(objectPropertyRangeElements, "ObjectPropertyRange")
    SubElement(ran, "ObjectProperty", attrib={"IRI": "#WriterIs"})
    SubElement(ran, "Class", attrib={"IRI": "#Person"})

    dec = SubElement(objectPropertyElements, "Declaration")
    SubElement(dec, "ObjectProperty", attrib={"IRI": "#CastIs"})
    dom = SubElement(objectPropertyDomainElements, "ObjectPropertyDomain")
    SubElement(dom, "ObjectProperty", attrib={"IRI": "#CastIs"})
    SubElement(dom, "Class", attrib={"IRI": "#Movie"})
    ran = SubElement(objectPropertyRangeElements, "ObjectPropertyRange")
    SubElement(ran, "ObjectProperty", attrib={"IRI": "#CastIs"})
    SubElement(ran, "Class", attrib={"IRI": "#Person"})

    dec = SubElement(objectPropertyElements, "Declaration")
    SubElement(dec, "ObjectProperty", attrib={"IRI": "#ProducedBy"})
    dom = SubElement(objectPropertyDomainElements, "ObjectPropertyDomain")
    SubElement(dom, "ObjectProperty", attrib={"IRI": "#ProducedBy"})
    SubElement(dom, "Class", attrib={"IRI": "#Movie"})
    ran = SubElement(objectPropertyRangeElements, "ObjectPropertyRange")
    SubElement(ran, "ObjectProperty", attrib={"IRI": "#ProducedBy"})
    SubElement(ran, "Class", attrib={"IRI": "#Company"})

    # DATA TYPE PROPERTIES
    dataPropertyElements = Element("dataPropertyElements")
    dataPropertyDomainElements = Element("dataPropertyDomainElements")
    dataPropertyRangeElements = Element("dataPropertyRangeElements")

    dec = SubElement(dataPropertyElements, "Declaration")
    SubElement(dec, "DataProperty", attrib={"IRI": "#HasID"})
    dom = SubElement(dataPropertyDomainElements, "DataPropertyDomain")
    SubElement(dom, "DataProperty", attrib={"IRI": "#HasID"})
    SubElement(dom, "Class", attrib={"IRI": "#Movie"})
    ran = SubElement(dataPropertyRangeElements, "DataPropertyRange")
    SubElement(ran, "DataProperty", attrib={"IRI": "#HasID"})
    SubElement(ran, "Datatype", attrib={"abbreviatedIRI": "xsd:string"})

    dec = SubElement(dataPropertyElements, "Declaration")
    SubElement(dec, "DataProperty", attrib={"IRI": "#IsRanked"})
    dom = SubElement(dataPropertyDomainElements, "DataPropertyDomain")
    SubElement(dom, "DataProperty", attrib={"IRI": "#IsRanked"})
    SubElement(dom, "Class", attrib={"IRI": "#Movie"})
    ran = SubElement(dataPropertyRangeElements, "DataPropertyRange")
    SubElement(ran, "DataProperty", attrib={"IRI": "#IsRanked"})
    SubElement(ran, "Datatype", attrib={"abbreviatedIRI": "xsd:int"})

    dec = SubElement(dataPropertyElements, "Declaration")
    SubElement(dec, "DataProperty", attrib={"IRI": "#HasName"})
    dom = SubElement(dataPropertyDomainElements, "DataPropertyDomain")
    SubElement(dom, "DataProperty", attrib={"IRI": "#HasName"})
    SubElement(dom, "Class", attrib={"IRI": "#Top"})
    ran = SubElement(dataPropertyRangeElements, "DataPropertyRange")
    SubElement(ran, "DataProperty", attrib={"IRI": "#HasName"})
    SubElement(ran, "Datatype", attrib={"abbreviatedIRI": "xsd:string"})

    dec = SubElement(dataPropertyElements, "Declaration")
    SubElement(dec, "DataProperty", attrib={"IRI": "#HasTagline"})
    dom = SubElement(dataPropertyDomainElements, "DataPropertyDomain")
    SubElement(dom, "DataProperty", attrib={"IRI": "#HasTagline"})
    SubElement(dom, "Class", attrib={"IRI": "#Movie"})
    ran = SubElement(dataPropertyRangeElements, "DataPropertyRange")
    SubElement(ran, "DataProperty", attrib={"IRI": "#HasTagline"})
    SubElement(ran, "Datatype", attrib={"abbreviatedIRI": "xsd:string"})

    dec = SubElement(dataPropertyElements,"Declaration")
    SubElement(dec,"DataProperty",attrib={"IRI": "#BudgetSpent"})
    dom = SubElement(dataPropertyDomainElements, "DataPropertyDomain")
    SubElement(dom,"DataProperty",attrib={"IRI": "#BudgetSpent"})
    SubElement(dom,"Class", attrib={"IRI": "#Movie"})
    ran = SubElement(dataPropertyRangeElements, "DataPropertyRange")
    SubElement(ran,"DataProperty",attrib={"IRI": "#BudgetSpent"})
    SubElement(ran,"Datatype", attrib={"abbreviatedIRI": "xsd:string"})

    dec = SubElement(dataPropertyElements, "Declaration")
    SubElement(dec, "DataProperty", attrib={"IRI": "#HasRating"})
    dom = SubElement(dataPropertyDomainElements, "DataPropertyDomain")
    SubElement(dom, "DataProperty", attrib={"IRI": "#HasRating"})
    SubElement(dom, "Class", attrib={"IRI": "#Movie"})
    ran = SubElement(dataPropertyRangeElements, "DataPropertyRange")
    SubElement(ran, "DataProperty", attrib={"IRI": "#HasRating"})
    SubElement(ran, "Datatype", attrib={"abbreviatedIRI": "xsd:float"})

    dec = SubElement(dataPropertyElements, "Declaration")
    SubElement(dec, "DataProperty", attrib={"IRI": "#HasBestRating"})
    dom = SubElement(dataPropertyDomainElements, "DataPropertyDomain")
    SubElement(dom, "DataProperty", attrib={"IRI": "#HasBestRating"})
    SubElement(dom, "Class", attrib={"IRI": "#Movie"})
    ran = SubElement(dataPropertyRangeElements, "DataPropertyRange")
    SubElement(ran, "DataProperty", attrib={"IRI": "#HasBestRating"})
    SubElement(ran, "Datatype", attrib={"abbreviatedIRI": "xsd:int"})

    dec = SubElement(dataPropertyElements, "Declaration")
    SubElement(dec, "DataProperty", attrib={"IRI": "#HasRatingCount"})
    dom = SubElement(dataPropertyDomainElements, "DataPropertyDomain")
    SubElement(dom, "DataProperty", attrib={"IRI": "#HasRatingCount"})
    SubElement(dom, "Class", attrib={"IRI": "#Movie"})
    ran = SubElement(dataPropertyRangeElements, "DataPropertyRange")
    SubElement(ran, "DataProperty", attrib={"IRI": "#HasRatingCount"})
    SubElement(ran, "Datatype", attrib={"abbreviatedIRI": "xsd:int"})

    dec = SubElement(dataPropertyElements, "Declaration")
    SubElement(dec, "DataProperty", attrib={"IRI": "#RuntimeIs"})
    dom = SubElement(dataPropertyDomainElements, "DataPropertyDomain")
    SubElement(dom, "DataProperty", attrib={"IRI": "#RuntimeIs"})
    SubElement(dom, "Class", attrib={"IRI": "#Movie"})
    ran = SubElement(dataPropertyRangeElements, "DataPropertyRange")
    SubElement(ran, "DataProperty", attrib={"IRI": "#RuntimeIs"})
    SubElement(ran, "Datatype", attrib={"abbreviatedIRI": "xsd:time"})

    dec = SubElement(dataPropertyElements, "Declaration")
    SubElement(dec, "DataProperty", attrib={"IRI": "#ReleaseDate"})
    dom = SubElement(dataPropertyDomainElements, "DataPropertyDomain")
    SubElement(dom, "DataProperty", attrib={"IRI": "#ReleaseDate"})
    SubElement(dom, "Class", attrib={"IRI": "#Movie"})
    ran = SubElement(dataPropertyRangeElements, "DataPropertyRange")
    SubElement(ran, "DataProperty", attrib={"IRI": "#ReleaseDate"})
    SubElement(ran, "Datatype", attrib={"abbreviatedIRI": "xsd:date"})

    dec = SubElement(dataPropertyElements, "Declaration")
    SubElement(dec, "DataProperty", attrib={"IRI": "#PlotSummary"})
    dom = SubElement(dataPropertyDomainElements, "DataPropertyDomain")
    SubElement(dom, "DataProperty", attrib={"IRI": "#PlotSummary"})
    SubElement(dom, "Class", attrib={"IRI": "#Movie"})
    ran = SubElement(dataPropertyRangeElements, "DataPropertyRange")
    SubElement(ran, "DataProperty", attrib={"IRI": "#PlotSummary"})
    SubElement(ran, "Datatype", attrib={"abbreviatedIRI": "xsd:string"})

    dec = SubElement(dataPropertyElements, "Declaration")
    SubElement(dec, "DataProperty", attrib={"IRI": "#HasRole"})
    dom = SubElement(dataPropertyDomainElements, "DataPropertyDomain")
    SubElement(dom, "DataProperty", attrib={"IRI": "#HasRole"})
    SubElement(dom, "Class", attrib={"IRI": "#Person"})
    ran = SubElement(dataPropertyRangeElements, "DataPropertyRange")
    SubElement(ran, "DataProperty", attrib={"IRI": "#HasRole"})
    SubElement(ran, "Datatype", attrib={"abbreviatedIRI": "xsd:string"})

    allElements.append(classElements)
    allElements.append(objectPropertyElements)
    allElements.append(dataPropertyElements)
    allElements.append(namedIndividualElements)
    # allElements.append(annotationPropertyElements)
    allElements.append(subClassOfElements)
    allElements.append(classAssertionElements)
    allElements.append(objectPropertyDomainElements)
    allElements.append(objectPropertyRangeElements)
    allElements.append(dataPropertyDomainElements)
    allElements.append(dataPropertyRangeElements)
    allElements.append(hasNameElements)
    return allElements


def stepTwo(allElements):

    hasNameElements = allElements.pop()
    productOfElements = Element("productOfElements")
    spokenInElements = Element("spokenInElements")
    genreIsElements = Element("genreIsElements")
    releaseCountryElements = Element("releaseCountryElements")
    if kwInclude:
        hasKeywordElements = Element("hasKeywordElements")
    directorIsElements = Element("directorIsElements")
    writerIsElements = Element("writerIsElements")
    castIsElements = Element("castIsElements")
    producedByElements = Element("producedByElements")
    hasIDElements = Element("hasIDElements")
    isRankedElements = Element("isRankedElements")
    hasTaglineElements = Element("hasTaglineElements")
    budgetSpentElements = Element("budgetSpentElements")
    hasRatingElements = Element("hasRatingElements")
    hasBestRatingElements = Element("hasBestRatingElements")
    hasRatingCountElements = Element("hasRatingCountElements")
    runtimeIsElements = Element("runtimeIsElements")
    releaseDateElements = Element("releaseDateElements")
    plotSummaryElements = Element("plotSummaryElements")
    hasRoleElements = Element("hasRoleElements")

    # defining MOVIES
    for movie in data:

        # HasID Assertions (DataProperty)
        assertion = SubElement(hasIDElements, "DataPropertyAssertion")
        SubElement(assertion, "DataProperty", attrib={"IRI": "#HasID"})
        SubElement(assertion, "NamedIndividual",
                   attrib={"IRI": "#"+movie['imdbID']})
        SubElement(assertion, "Literal").text = movie['imdbID']

        # IsRanked Assertions (DataProperty)
        assertion = SubElement(isRankedElements, "DataPropertyAssertion")
        SubElement(assertion, "DataProperty", attrib={"IRI": "#IsRanked"})
        SubElement(assertion, "NamedIndividual",
                   attrib={"IRI": "#"+movie['imdbID']})
        SubElement(assertion, "Literal").text = movie['rank']

        # HasName Assertions (DataProperty)
        assertion = SubElement(hasNameElements, "DataPropertyAssertion")
        SubElement(assertion, "DataProperty", attrib={"IRI": "#HasName"})
        SubElement(assertion, "NamedIndividual",
                   attrib={"IRI": "#"+movie['imdbID']})
        SubElement(assertion, "Literal").text = movie['title']

        # HasTaglines Assertions (DataProperty)
        try:
            for tl in movie['taglines']:
                assertion = SubElement(
                    hasTaglineElements, "DataPropertyAssertion")
                SubElement(assertion, "DataProperty",
                           attrib={"IRI": "#HasTagline"})
                SubElement(assertion, "NamedIndividual",
                           attrib={"IRI": "#"+movie['imdbID']})
                SubElement(assertion, "Literal").text = tl
        except:
            pass

        # ProductOf Assertions (ObjectProperty)
        for co in movie['country']:
            country = co.replace(' ', '-').replace("'", '').replace('.', '')
            assertion = SubElement(
                productOfElements, "ObjectPropertyAssertion")
            SubElement(assertion, "ObjectProperty",
                       attrib={"IRI": "#ProductOf"})
            SubElement(assertion, "NamedIndividual",
                       attrib={"IRI": "#"+movie['imdbID']})
            SubElement(assertion, "NamedIndividual",
                       attrib={"IRI": "#"+country})

        # SpokenIn Assertions (ObjectProperty)
        for lang in movie['language']:
            language = lang.replace(' ', '-').replace("'", '').replace('.', '')
            assertion = SubElement(spokenInElements, "ObjectPropertyAssertion")
            SubElement(assertion, "ObjectProperty",
                       attrib={"IRI": "#SpokenIn"})
            SubElement(assertion, "NamedIndividual",
                       attrib={"IRI": "#"+movie['imdbID']})
            SubElement(assertion, "NamedIndividual",
                       attrib={"IRI": "#"+language})

        # BugdetSpent Assertions (DataProperty)
        try:
            amount = movie['budgetIn$']
            assertion = SubElement(budgetSpentElements, "DataPropertyAssertion")
            SubElement(assertion,"DataProperty",attrib={"IRI": "#BudgetSpent"})
            SubElement(assertion,"NamedIndividual",attrib={"IRI": "#"+movie['imdbID']})
            SubElement(assertion,"Literal").text = amount
        except:
            pass

        # HasRating Assertions (DataProperty)
        assertion = SubElement(hasRatingElements, "DataPropertyAssertion")
        SubElement(assertion, "DataProperty", attrib={"IRI": "#HasRating"})
        SubElement(assertion, "NamedIndividual",
                   attrib={"IRI": "#"+movie['imdbID']})
        SubElement(
            assertion, "Literal").text = movie['ratingInfo']['imdbRating']

        # HasBestRating Assertions (DataProperty)
        assertion = SubElement(hasBestRatingElements, "DataPropertyAssertion")
        SubElement(assertion, "DataProperty", attrib={"IRI": "#HasBestRating"})
        SubElement(assertion, "NamedIndividual",
                   attrib={"IRI": "#"+movie['imdbID']})
        SubElement(
            assertion, "Literal").text = movie['ratingInfo']['bestRating']

        # HasRatingCount Assertions (DataProperty)
        assertion = SubElement(hasRatingCountElements,"DataPropertyAssertion")
        SubElement(assertion,"DataProperty",attrib={"IRI": "#HasRatingCount"})
        SubElement(assertion,"NamedIndividual",attrib={"IRI": "#"+movie['imdbID']})
        SubElement(assertion, "Literal").text = movie['ratingInfo']['ratingCount']

        # RuntimeIs Assertions (DataProperty)
        assertion = SubElement(runtimeIsElements, "DataPropertyAssertion")
        SubElement(assertion, "DataProperty", attrib={"IRI": "#RuntimeIs"})
        SubElement(assertion, "NamedIndividual",
                   attrib={"IRI": "#"+movie['imdbID']})
        SubElement(assertion, "Literal").text = movie['runtime']

        # GenreIs Assertions (ObjectProperty)
        for gn in movie['genre']:
            genre = gn.replace(' ', '-').replace("'", '').replace('.', '')
            assertion = SubElement(genreIsElements, "ObjectPropertyAssertion")
            SubElement(assertion, "ObjectProperty", attrib={"IRI": "#GenreIs"})
            SubElement(assertion, "NamedIndividual",
                       attrib={"IRI": "#"+movie['imdbID']})
            SubElement(assertion, "NamedIndividual", attrib={"IRI": "#"+genre})

        # ReleaseCountry Assertions (ObjectProperty)
        country = movie['release']['country'].replace(
            ' ', '-').replace("'", '').replace('.', '')
        assertion = SubElement(releaseCountryElements,
                               "ObjectPropertyAssertion")
        SubElement(assertion, "ObjectProperty",
                   attrib={"IRI": "#ReleaseCountry"})
        SubElement(assertion, "NamedIndividual",
                   attrib={"IRI": "#"+movie['imdbID']})
        SubElement(assertion, "NamedIndividual", attrib={"IRI": "#"+country})

        # ReleaseDate Assertions (DataProperty)
        assertion = SubElement(releaseDateElements, "DataPropertyAssertion")
        SubElement(assertion, "DataProperty", attrib={"IRI": "#ReleaseDate"})
        SubElement(assertion, "NamedIndividual",
                   attrib={"IRI": "#"+movie['imdbID']})
        SubElement(assertion, "Literal").text = movie['release']['date']

        # PlotSummary Assertions (DataProperty)
        assertion = SubElement(plotSummaryElements, "DataPropertyAssertion")
        SubElement(assertion, "DataProperty", attrib={"IRI": "#PlotSummary"})
        SubElement(assertion, "NamedIndividual",
                   attrib={"IRI": "#"+movie['imdbID']})
        SubElement(assertion, "Literal").text = movie['plotSummary']

        # HasKeyword Assertions (ObjectProperty)
        if kwInclude:
            for kw in movie['keyword']:
                keyword = kw.replace(
                    ' ', '-').replace("'", '').replace('.', '')
                assertion = SubElement(
                    hasKeywordElements, "ObjectPropertyAssertion")
                SubElement(assertion, "ObjectProperty",
                           attrib={"IRI": "#HasKeyword"})
                SubElement(assertion, "NamedIndividual",
                           attrib={"IRI": "#"+movie['imdbID']})
                SubElement(assertion, "NamedIndividual",
                           attrib={"IRI": "#"+keyword})

        # DirectorIs Assertions (ObjectProperty)
        for di in movie['credit']['director']:
            director = di.replace(' ', '-').replace("'", '').replace('.', '')
            assertion = SubElement(
                directorIsElements, "ObjectPropertyAssertion")
            SubElement(assertion, "ObjectProperty",
                       attrib={"IRI": "#DirectorIs"})
            SubElement(assertion, "NamedIndividual",
                       attrib={"IRI": "#"+movie['imdbID']})
            SubElement(assertion, "NamedIndividual",
                       attrib={"IRI": "#"+director})

        # WriterIs Assertions (ObjectProperty)
        for wr in movie['credit']['writer']:
            writer = wr.replace(' ', '-').replace("'", '').replace('.', '')
            assertion = SubElement(
                writerIsElements, "ObjectPropertyAssertion")
            SubElement(assertion, "ObjectProperty",
                       attrib={"IRI": "#WriterIs"})
            SubElement(assertion, "NamedIndividual",
                       attrib={"IRI": "#"+movie['imdbID']})
            SubElement(assertion, "NamedIndividual",
                       attrib={"IRI": "#"+writer})

        for ac in movie['credit']['cast']:
            actor = ac['name'].replace(
                ' ', '-').replace("'", '').replace('.', '')
            # CastIs Assertions (ObjectProperty)
            assertion = SubElement(castIsElements, "ObjectPropertyAssertion")
            SubElement(assertion, "ObjectProperty", attrib={"IRI": "#CastIs"})
            SubElement(assertion, "NamedIndividual",
                       attrib={"IRI": "#"+movie['imdbID']})
            SubElement(assertion, "NamedIndividual", attrib={"IRI": "#"+actor})
            # HasRole Assertions (DataProperty)
            assertion = SubElement(hasRoleElements, "DataPropertyAssertion")
            SubElement(assertion, "DataProperty", attrib={"IRI": "#HasRole"})
            SubElement(assertion, "NamedIndividual", attrib={"IRI": "#"+actor})
            SubElement(assertion, "Literal").text = ac['character']

        # ProducedBy Assertions (ObjectProperty)
        for co in movie['credit']['productionCompany']:
            company = co.replace(' ', '-').replace("'", '').replace('.', '')
            assertion = SubElement(
                producedByElements, "ObjectPropertyAssertion")
            SubElement(assertion, "ObjectProperty",
                       attrib={"IRI": "#ProducedBy"})
            SubElement(assertion, "NamedIndividual",
                       attrib={"IRI": "#"+movie['imdbID']})
            SubElement(assertion, "NamedIndividual",
                       attrib={"IRI": "#"+company})

    allElements.append(hasNameElements)
    allElements.append(productOfElements)
    allElements.append(spokenInElements)
    allElements.append(genreIsElements)
    allElements.append(releaseCountryElements)
    if kwInclude:
        allElements.append(hasKeywordElements)
    allElements.append(directorIsElements)
    allElements.append(writerIsElements)
    allElements.append(castIsElements)
    allElements.append(producedByElements)
    allElements.append(hasIDElements)
    allElements.append(isRankedElements)
    allElements.append(hasTaglineElements)
    allElements.append(budgetSpentElements)
    allElements.append(hasRatingElements)
    allElements.append(hasBestRatingElements)
    allElements.append(hasRatingCountElements)
    allElements.append(runtimeIsElements)
    allElements.append(releaseDateElements)
    allElements.append(plotSummaryElements)
    allElements.append(hasRoleElements)

    return allElements


def mergeElements(allElements):
    for pElement in allElements:
        for chElement in pElement.iterchildren():
            root.append(chElement)


class NS():
    xml = "http://www.w3.org/XML/1998/namespace"
    rdf = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    rdfs = "http://www.w3.org/2000/01/rdf-schema#"
    owl = "http://www.w3.org/2002/07/owl#"
    xsd = "http://www.w3.org/2001/XMLSchema#"
    imdb = "http://www.semanticweb.org/top/ontologies/imdb"


root = Element('Ontology', nsmap={"xml": NS.xml, "rdf": NS.rdf, "rdfs": NS.rdfs, "owl": NS.owl, "xsd": NS.xsd, "imdb": NS.imdb}, attrib={
               "xmlns": "http://www.w3.org/2002/07/owl#", QName(NS.xml, "base"): NS.imdb, "ontologyIRI": NS.imdb})

SubElement(root, "Prefix", attrib={"name": "", "IRI": NS.imdb})
SubElement(root, "Prefix", attrib={"name": "xml", "IRI": NS.xml})
SubElement(root, "Prefix", attrib={"name": "rdf", "IRI": NS.rdf})
SubElement(root, "Prefix", attrib={"name": "rdfs", "IRI": NS.rdfs})
SubElement(root, "Prefix", attrib={"name": "owl", "IRI": NS.owl})
SubElement(root, "Prefix", attrib={"name": "xsd", "IRI": NS.xsd})
SubElement(root, "Prefix", attrib={"name": "imdb", "IRI": NS.imdb+"#"})

data = readJson()

if __name__ == "__main__":
    start()
