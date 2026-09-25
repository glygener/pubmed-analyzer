from models import Article
publications = {}
def publication_per_year_trend(pub_year):
 if pub_year in publications:
    publications[pub_year] += 1
 else:
   publications[pub_year] = 1
 print(f'Publication year: {pub_year} Publications: {publications[pub_year]}')
publication_per_year_trend(2025)
publication_per_year_trend(2025)
publication_per_year_trend(2025)
publication_per_year_trend(2016)
publication_per_year_trend(2016)

