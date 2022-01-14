import xml.dom.minidom

domtree = xml.dom.minidom.parse("all.xml")
group = domtree.documentElement

movies = group.getElementsByTagName('movies')

for movie in movies:
    print("---Movie---")
    if movie.hasAttributes('year'):
        print(f"{movie.getAttribute('year')}")
