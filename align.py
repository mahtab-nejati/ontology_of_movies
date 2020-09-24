from lxml.etree import Element, SubElement, fromstring, tostring, QName
from files import getOntology, saveOWL
import re


def start():
    available = False
    while not available:
        print('\n\nFirst!  Remove the "NameSpace Declarations" and "Prefix" tags from the begining of \n\
            files "data_owl.owl" and "ontology.owl" in directory "./ontology/" .\n\
            Save each file with namse "data_owl_r.owl" and "ontology_r.owl" in the same directory.\n\
            Press "Enter" when you\'re done!')
        input()

        mOntology = getOntology("data_owl_r.owl")
        qOntology = getOntology("ontology_r.owl")
        if mOntology == "" or qOntology == "":
            continue
        forbidden = ['xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"', 'xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"', 'xmlns:owl="http://www.w3.org/2002/07/owl#"',
                     'xmlns:xsd="http://www.w3.org/2001/XMLSchema#"', 'xmlns:imdb=', 'xmlns=', '"http://www.w3.org/2002/07/owl#"', 'xml:base=', 'ontologyIRI=']
        if any(ns in mOntology for ns in forbidden) or any(ns in qOntology for ns in forbidden):
            continue
        break
    print("\nGreat! Alignment in progress. It might take a couple of minutes...")
    mergeOntology(mOntology, qOntology)
    saveOWL('<?xml version="1.0" encoding="UTF-8"?>\n' +
            tostring(aligned, pretty_print=True).decode("utf-8"), "aligned.owl")
    print("\n\nAll data aligned, merged, and saved into ./ontology/aligned.owl")


def mergeOntology(monto, qonto):

    mOntology = monto
    qOntology = qonto

    mOntology = re.sub('"#ProductOf"', '"#MadeIn"', mOntology)
    mOntology = re.sub('"xsd:date"', '"xsd:string"', mOntology)
    mRoot = fromstring(mOntology.encode("utf-8"))

    qOntology = re.sub('"#tagh"', '"#Top"', qOntology)
    qOntology = re.sub('"#has_actor"', '"#CastIs"', qOntology)
    qOntology = re.sub('"#has_director"', '"#DirectorIs"', qOntology)
    qOntology = re.sub('"#has_writer"', '"#WriterIs"', qOntology)
    qOntology = re.sub('"#has_genre"', '"#GenreIs"', qOntology)
    qOntology = re.sub('"#has_language"', '"#SpokenIn"', qOntology)
    qOntology = re.sub('"#made_in"', '"#MadeIn"', qOntology)
    qOntology = re.sub('"#rate"', '"#HasRating"', qOntology)
    qOntology = re.sub('"#release_date"', '"#ReleaseDate"', qOntology)
    qOntology = re.sub('"#runtime"', '"#RuntimeIs"', qOntology)
    qOntology = re.sub('"#name"', '"#HasName"', qOntology)
    qRoot = fromstring(qOntology.encode("utf-8"))

    toDrop = []

    mClassInstances = {'Movie': 0, 'Country': 0,
                       'Genre': 0, 'Language': 0, 'Person': 0}
    mObjectPropertyInstances = {'CastIs': 0, 'DirectorIs': 0,
                                'GenreIs': 0, 'MadeIn': 0, 'SpokenIn': 0, 'WriterIs': 0}
    mDataPropertyInstances = {'HasRating': 0,
                              'ReleaseDate': 0, 'RuntimeIs': 0, 'HasName': 0}

    for mEl in mRoot:
        elstring = stripC(tostring(mEl, pretty_print=True))
        if "ClassAssertion" in elstring and '"#Movie"' in elstring:
            mRoot.append(fromstring(
                re.sub('"#Movie"', '"#Film"', elstring).encode('utf-8')))
        if (("DataPropertyDomain" in elstring or "ObjectPropertyDomain" in elstring or "DataPropertyRange" in elstring or "ObjectPropertyRange" in elstring) and '"#Movie"' in elstring):
            toDrop.append(elstring)
            mRoot.append(fromstring(
                re.sub('"#Movie"', '"#Film"', elstring).encode('utf-8')))
        if "ClassAssertion" in elstring:
            if '"#Person"' in elstring:
                mClassInstances['Person'] += 1
            elif '"#Movie"' in elstring:
                mClassInstances['Movie'] += 1
            elif '"#Country"' in elstring:
                mClassInstances['Country'] += 1
            elif '"#Language"' in elstring:
                mClassInstances['Language'] += 1
            elif '"#Genre"' in elstring:
                mClassInstances['Genre'] += 1
        elif "ObjectPropertyAssertion" in elstring:
            if '"#CastIs"' in elstring:
                mObjectPropertyInstances['CastIs'] += 1
            elif '"#DirectorIs"' in elstring:
                mObjectPropertyInstances['DirectorIs'] += 1
            elif '"#GenreIs"' in elstring:
                mObjectPropertyInstances['GenreIs'] += 1
            elif '"#MadeIn"' in elstring:
                mObjectPropertyInstances['MadeIn'] += 1
            elif '"#SpokenIn"' in elstring:
                mObjectPropertyInstances['SpokenIn'] += 1
            elif '"#WriterIs"' in elstring:
                mObjectPropertyInstances['WriterIs'] += 1
        elif "DataPropertyAssertion" in elstring:
            if '"#HasRating"' in elstring:
                mDataPropertyInstances['HasRating'] += 1
            elif '"#ReleaseDate"' in elstring:
                mDataPropertyInstances['ReleaseDate'] += 1
            elif '"#RuntimeIs"' in elstring:
                mDataPropertyInstances['RuntimeIs'] += 1
            elif '"#HasName"' in elstring:
                mDataPropertyInstances['HasName'] += 1

    mStatistics = {'class': mClassInstances,
                   'objectP': mObjectPropertyInstances, 'dataP': mDataPropertyInstances}

    qClassInstances = {'Film': 0, 'Movie': 0, 'Country': 0,
                       'Genre': 0, 'Language': 0, 'Person': 0}
    qObjectPropertyInstances = {'CastIs': 0, 'DirectorIs': 0,
                                'GenreIs': 0, 'MadeIn': 0, 'SpokenIn': 0, 'WriterIs': 0}
    qDataPropertyInstances = {'HasRating': 0,
                              'ReleaseDate': 0, 'RuntimeIs': 0, 'HasName': 0}
    for qEl in qRoot:
        elstring = stripC(tostring(qEl, pretty_print=True))
        if "DataPropertyAssertion" in elstring and "#HasName" in elstring:
            indID = '"'+qEl.xpath('./NamedIndividual/@IRI')[0]+'"'
            repl = '"#'+qEl.xpath('./Literal/text()')[0].replace(
                ' ', '-').replace("'", '').replace('.', '')+'"'
            qOntology = re.sub(indID, repl, qOntology)
        if "ClassAssertion" in elstring:
            if '"#Person"' in elstring:
                qClassInstances['Person'] += 1
            elif '"#Movie"' in elstring:
                qClassInstances['Movie'] += 1
            elif '"#Film"' in elstring:
                qClassInstances['Film'] += 1
            elif '"#Country"' in elstring:
                qClassInstances['Country'] += 1
            elif '"#Language"' in elstring:
                qClassInstances['Language'] += 1
            elif '"#Genre"' in elstring:
                qClassInstances['Genre'] += 1
        elif "ObjectPropertyAssertion" in elstring:
            if '"#CastIs"' in elstring:
                qObjectPropertyInstances['CastIs'] += 1
            elif '"#DirectorIs"' in elstring:
                qObjectPropertyInstances['DirectorIs'] += 1
            elif '"#GenreIs"' in elstring:
                qObjectPropertyInstances['GenreIs'] += 1
            elif '"#MadeIn"' in elstring:
                qObjectPropertyInstances['MadeIn'] += 1
            elif '"#SpokenIn"' in elstring:
                qObjectPropertyInstances['SpokenIn'] += 1
            elif '"#WriterIs"' in elstring:
                qObjectPropertyInstances['WriterIs'] += 1
        elif "DataPropertyAssertion" in elstring:
            if '"#HasRating"' in elstring:
                qDataPropertyInstances['HasRating'] += 1
            elif '"#ReleaseDate"' in elstring:
                qDataPropertyInstances['ReleaseDate'] += 1
            elif '"#RuntimeIs"' in elstring:
                qDataPropertyInstances['RuntimeIs'] += 1
            elif '"#HasName"' in elstring:
                qDataPropertyInstances['HasName'] += 1

    qStatistics = {'class': qClassInstances,
                   'objectP': qObjectPropertyInstances, 'dataP': qDataPropertyInstances}

    qOntology = re.sub('"#title"', '"#HasName"', qOntology)
    qRoot = fromstring(qOntology.encode("utf-8"))

    fList = []

    for mEl in mRoot.iterchildren():
        elstring = stripC(tostring(mEl, pretty_print=True))
        if "SubClassOf" in elstring and "#Movie" in elstring and "#Top" in elstring:
            continue
        if elstring in toDrop:
            continue
        fList.append(elstring)
    for qEl in qRoot.iterchildren():
        elstring = stripC(tostring(qEl, pretty_print=True))
        fList.append(elstring)

    fList = list(set(fList))

    aClassInstances = {'Film': 0, 'Movie': 0, 'Country': 0,
                       'Genre': 0, 'Language': 0, 'Person': 0}
    aObjectPropertyInstances = {'CastIs': 0, 'DirectorIs': 0,
                                'GenreIs': 0, 'MadeIn': 0, 'SpokenIn': 0, 'WriterIs': 0}
    aDataPropertyInstances = {'HasRating': 0,
                              'ReleaseDate': 0, 'RuntimeIs': 0, 'HasName': 0}

    for elstring in fList:
        if "ClassAssertion" in elstring:
            if '"#Person"' in elstring:
                aClassInstances['Person'] += 1
            elif '"#Movie"' in elstring:
                aClassInstances['Movie'] += 1
            elif '"#Film"' in elstring:
                aClassInstances['Film'] += 1
            elif '"#Country"' in elstring:
                aClassInstances['Country'] += 1
            elif '"#Language"' in elstring:
                aClassInstances['Language'] += 1
            elif '"#Genre"' in elstring:
                aClassInstances['Genre'] += 1
        elif "ObjectPropertyAssertion" in elstring:
            if '"#CastIs"' in elstring:
                aObjectPropertyInstances['CastIs'] += 1
            elif '"#DirectorIs"' in elstring:
                aObjectPropertyInstances['DirectorIs'] += 1
            elif '"#GenreIs"' in elstring:
                aObjectPropertyInstances['GenreIs'] += 1
            elif '"#MadeIn"' in elstring:
                aObjectPropertyInstances['MadeIn'] += 1
            elif '"#SpokenIn"' in elstring:
                aObjectPropertyInstances['SpokenIn'] += 1
            elif '"#WriterIs"' in elstring:
                aObjectPropertyInstances['WriterIs'] += 1
        elif "DataPropertyAssertion" in elstring:
            if '"#HasRating"' in elstring:
                aDataPropertyInstances['HasRating'] += 1
            elif '"#ReleaseDate"' in elstring:
                aDataPropertyInstances['ReleaseDate'] += 1
            elif '"#RuntimeIs"' in elstring:
                aDataPropertyInstances['RuntimeIs'] += 1
            elif '"#HasName"' in elstring:
                aDataPropertyInstances['HasName'] += 1

    aStatistics = {'class': aClassInstances,
                   'objectP': aObjectPropertyInstances, 'dataP': aDataPropertyInstances}

    reportStatistics(mStatistics, qStatistics, aStatistics)

    makeAligned(fList)


def stripC(s):
    s = s.decode('utf-8')
    s = s.replace('  ', '')
    s = s.replace('\t', '')
    s = s.replace('\n', '')
    s = s.replace('\r', '')
    return s


def reportStatistics(mStat, qStat, aStat):
    print("\n\nAlignment Statistical Report:")

    classes = ['Movie', 'Country', 'Genre', 'Language', 'Person']
    objectPs = ['CastIs', 'DirectorIs', 'GenreIs',
                'MadeIn', 'SpokenIn', 'WriterIs']
    dataPs = ['HasRating', 'ReleaseDate', 'RuntimeIs', 'HasName']

    print("\n***Class***")
    a1 = qStat['class']['Film']
    a2 = mStat['class']['Movie']
    a3 = aStat['class']['Film']
    print("\nOntology.Film VS Data.Movie:")
    print("Number of instances in Ontology.Film\t\t"+str(a1))
    print("Number of instances in Data.Movie\t\t"+str(a2))
    print("Number of common instances\t\t\t" +
          str(a1+a2-a3))
    print("Similarity metric\t\t\t\t" +
          str((a1+a2-a3)/a3))
    print("##########################################################")

    for case in classes:
        a1 = qStat['class'][case]
        a2 = mStat['class'][case]
        a3 = aStat['class'][case]
        print("Ontology."+case+" VS Data."+case+":")
        print("Number of instances in Ontology."+case+"\t\t" + str(a1))
        print("Number of instances in Data."+case + "\t\t"+str(a2))
        print("Number of common instances\t\t\t" +
              str(a1+a2-a3))
        print("Similarity metric\t\t\t\t" +
              str((a1+a2-a3)/a3))
        print("##########################################################")

    print("\n***ObjectProperty***\n")
    for case in objectPs:
        a1 = qStat['objectP'][case]
        a2 = mStat['objectP'][case]
        a3 = aStat['objectP'][case]
        print("Ontology."+case+" VS Data."+case+":")
        print("Number of instances in Ontology."+case+"\t\t" + str(a1))
        print("Number of instances in Data."+case + "\t\t"+str(a2))
        print("Number of common instances\t\t\t" + str(a1+a2-a3))
        print("Similarity metric\t\t\t\t" + str((a1+a2-a3)/a3))
        print("##########################################################")

    print("\n***DataProperty***\n")
    for case in dataPs:
        a1 = qStat['dataP'][case]
        a2 = mStat['dataP'][case]
        a3 = aStat['dataP'][case]
        print("Ontology."+case+" VS Data."+case+":")
        print("Number of instances in Ontology."+case+"\t\t" + str(a1))
        print("Number of instances in Data."+case + "\t\t"+str(a2))
        print("Number of common instances\t\t\t" + str(a1+a2-a3))
        print("Similarity metric\t\t\t\t" + str((a1+a2-a3)/a3))
        print("##########################################################")

    print("\n\nPress ENTER key to progress.")
    input()


def makeAligned(elList):
    for element in elList:
        aligned.append(fromstring(element))


class NS():
    xml = "http://www.w3.org/XML/1998/namespace"
    rdf = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    rdfs = "http://www.w3.org/2000/01/rdf-schema#"
    owl = "http://www.w3.org/2002/07/owl#"
    xsd = "http://www.w3.org/2001/XMLSchema#"
    imdb = "http://www.semanticweb.org/top/ontologies/imdb"


aligned = Element('Ontology', nsmap={
    "xml": NS.xml, "rdf": NS.rdf, "rdfs": NS.rdfs, "owl": NS.owl, "xsd": NS.xsd, "imdb": NS.imdb}, attrib={"xmlns": "http://www.w3.org/2002/07/owl#", QName(NS.xml, "base"): NS.imdb, "ontologyIRI": NS.imdb})

SubElement(aligned, "Prefix", attrib={"name": "", "IRI": NS.imdb})
SubElement(aligned, "Prefix", attrib={"name": "xml", "IRI": NS.xml})
SubElement(aligned, "Prefix", attrib={"name": "rdf", "IRI": NS.rdf})
SubElement(aligned, "Prefix", attrib={"name": "rdfs", "IRI": NS.rdfs})
SubElement(aligned, "Prefix", attrib={"name": "owl", "IRI": NS.owl})
SubElement(aligned, "Prefix", attrib={"name": "xsd", "IRI": NS.xsd})
SubElement(aligned, "Prefix", attrib={"name": "imdb", "IRI": NS.imdb+"#"})

if __name__ == "__main__":
    start()
