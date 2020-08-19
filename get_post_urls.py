import bs4
with open("post.html", "r") as f:
   html = bs4.BeautifulSoup(f.read())
downloads = html.select("div.action-bar--buttons span a:first-child")
urls = list(map(lambda x: "https://banking.ing.de/app/" + x["href"][2:], downloads))

with open('post_urls.txt', 'w') as f:
    for item in urls:
        f.write("%s\n" % item)
