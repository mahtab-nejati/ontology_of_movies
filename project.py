import crawl
import convert
import align

print("\n\nStart crawling? (Y/N)")
ans = input().lower()
if ans != "":
    if ans[0] == "y":
        crawl.start()

print("\n\nConvert to OWL? (Y/N)")
ans = input().lower()
if ans != "":
    if ans[0] == "y":
        convert.start()

print('\n\nDo you want to align and merge your data with "./ontology/ontology.owl"? (Y/N)')
ans = input().lower()
if ans != "":
    if ans[0] == "y":
        align.start()
