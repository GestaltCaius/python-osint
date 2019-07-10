# Python OSINT tool

![Imgur](https://i.imgur.com/DLGUyNp.png)

> Outil de renseignement d'origine source ouverte (OSINT) écrit en Python 3.7+
> Rodolphe GUILLAUME - APPING_I 2

<!-- # Plan du rapport

> 1. Introduction : on présente le problème qu'on veut résoudre et l'outil qu'on
>    veut développer
> 2. Le fonctionnement de l'outil
> 3. Les difficultés rencontrées, si on a réussi à tout faire ou pas
> 4. Les améliorations possibles
>    Et ne pas hésiter à faire des captures d'écran. Le prof ne lancera pas tous
>    les codes. On sera plus noté sur le rapport -->

# Usage

**Python 3.7** minimum est requis pour utiliser ce package.

<!-- ```bash
$ python3.7 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt 
$ python3 main.py --username johndoe 
Searching Namespace(email=None, firstname=None, lastname=None, username='johndoe')...
Results available in /home/rod/projects/python-osint/osint_result.log...
``` -->

![img](https://i.imgur.com/bMmWn9P.png)


<!-- ```bash
$ python3 main.py --help
usage: main.py [-h] [-u USERNAME] [-e EMAIL] [-f FIRSTNAME] [-l LASTNAME]

Python OSINT

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Username (nickname online)
  -e EMAIL, --email EMAIL
                        Email address
  -f FIRSTNAME, --firstname FIRSTNAME
                        Firstname (must come with a lastname as well)
  -l LASTNAME, --lastname LASTNAME
                        Lastname (must come with a firstname as well)
``` -->
![img](https://i.imgur.com/bvKJh0e.png)

# Python OSINT ?

Presque tous les outils de sécurité sont déjà disponibles en tant que packages python. J'ai donc pensé à un projet moins technique, l'OSINT.

En effet, depuis que les sites comme [pipl.com](https://pipl.com/) sont devenus payants, je n'avais plus d'outil pour rechercher des informations sur les gens quand par exemple je reçois des CV.

L'OSINT, *open source intelligence*, est une méthode de recherche utilisant toutes les ressources accessibles publiquement. Le site [Bellingcat](https://www.bellingcat.com/) ou encore les enquêtes de [Sylvqin](https://www.youtube.com/watch?v=Lh7BTN1QHH0&list=PL882MGbVSMNa8-CHvqdqSgZZTRnJrYv3L) utilisent cette méthode d'investigation.

Avec Internet et les moteurs de recherche, l'OSINT est devenu très simple à mettre en place.


J'ai donc voulu créer un outil en python permettant d'automatiser ce genre d'investigation.

Généralement, l'OSINT se fait à partir du *nom* et *prénom* de la personne, ou bien son *adresse mail* ou encore son *pseudo*.

Avec ces informations en main, on lance les recherches qui y sont liées. Mais on ne s'arrête pas là ! Google, et les autres moteurs également, mettent à disposition ce qu'on appelle les *dorks*. On peut voir ces *Google Dorks* comme des paramètres, des filtres, que l'on rajoute à notre recherche pour recevoir des résultats plus précis et pertinents.

Dans notre cas, il serait par exemple intéressant de filtrer par site web pour faire apparaître des profils sur les réseaux sociaux, des CV, des commentaires, des posts...

# Bing Search avec Python

Avant de pouvoir effectuer des recherches pertinentes, il faut pouvoir faire des recherches simples.

Aucun des moteurs de recherche n'offre d'API pour effectuer des recherches. Google a le Google Custom Search, mais il est limité en nombre de recherches par jour, et n'est pas aussi complet que le Google Search classique.

Bing propose une API Azure, mais elle est payante...

J'ai donc décidé de créer mon propre scraper de Bing Search.

J'ai choisi Bing, car d'après mes recherches c'est le moteur de recherche le moins regardant concernant le scraping. Pour les autres moteurs, il faut limiter son scraping pour ne pas se faire attraper (attendre quelques ms entre chaque requêtes, etc.)

Bing supporte les Google Dorks, donc cela ne devrait pas trop impacter nos résultats.

J'ai choisi d'utiliser *BeautifulSoup* au lieu de *scrapy*. J'ai l'impression que scrapy était un peu trop complet et puissant pour mon cas d'usage. En effet, je voulais seulement récupérer la liste des résultats d'une page de résultat de recherche. Je n'avais pas besoin de crawler.

# Stratégie OSINT

J'ai suivi la méthode d'OSINT de [Petro Cherkasets](https://medium.com/@Peter_UXer) présentée dans son article [OSINT: How to find information on anyone](https://medium.com/@Peter_UXer/osint-how-to-find-information-on-anyone-5029a3c7fd56).

Il propose des plans d'action pour chaque information de départ.

<!-- Nom et prénom | Pseudo | Email
|:---:|:---:|:---:|
|![](https://miro.medium.com/max/700/1*4WMnGFT_Z0UJ3QN3vDLrhw.png)|![](https://miro.medium.com/max/700/1*wUJUgCHpwyLv84bQVI91wg.png)|![](https://miro.medium.com/max/700/1*saUQhMbxfk8AyaROKFN2nQ.png)| -->

<span>
<img src="https://miro.medium.com/max/700/1*4WMnGFT_Z0UJ3QN3vDLrhw.png" style="float: left; width: 33%;">
<img src="https://miro.medium.com/max/700/1*wUJUgCHpwyLv84bQVI91wg.png" style="float: left; width: 33%;">
<img src="https://miro.medium.com/max/700/1*saUQhMbxfk8AyaROKFN2nQ.png" style="float: left; width: 34%;">
</span>

C'est le moment d'utiliser les Google Dorks.

# Google dorks basiques

Les dorks les plus connus sont :

* `site:{google.com}`
* `filetype:{pdf, xls, csv, png}`

Ils permettent de filtrer les résultats pour un site en particulier, ou bien par format de fichier.

C'est utile pour trouver des profils sur les réseaux sociaux, ou bien pour trouver des CV en précisant le type PDF par exemple.

J'ai filtré sur les sites suivants :

```py
# constants.py

websites = [
    'twitter.com',
    'facebook.com',
    'instagram.com',
    'gotinder.com',
    'github.com',
    'linkedin.com',
    'badoo.com',
]
```

J'ai choisi de cibler les réseaux sociaux en priorité.

La première étape de ma recherche OSINT consiste à utiliser nos 3 entrées avec ces sites: `"John Doe" site:twitter.com`.

J'ai alors une liste de résultats assez basiques, et souvent peu pertinents à partir du 3ème résultat de la page. Ces premiers résultats sont donc filtrés. Je retire les résultats qui ne font pas apparaître mon input de recherche dans leur contenu.

Par exemple, si j'ai recherché le pseudo "toto", je retire tous les résultats n'ayant pas la chaine "toto" dans leurs contenu -- titre, description, URL.

## Les réseaux sociaux

Après cette première passe, j'ai décidé d'ajouter une couche spécifique aux réseaux sociaux. En effet, il existe un autre dork permettant d'exclure les résultats provenants d'un site. L'opposé du dork `site` en somme.

Il s'agit de `-site`. En mélangeant `site` et `-site` il est possible de mettre en avant les commentaires et posts des utilisateurs sur les réseaux.

En effet, en cherchant sur un site mais en excluant le profil de la personne sur ce même site, on récupère les contenus mentionnant son pseudo mais n'étant pas sur sa propre page. En d'autres termes, on récupère les commentaires qu'il a posté sur les contenus des autres !

Un exemple sera peut-être plus parlant, cela ressemble à cela :

`DarkAngel64 site:instagram.com -site:instagram.com/DarkAngel64`

Pour ces résultats là, j'ai décidé de ne pas filtrer les résultats. En effet, même si la brève description du résultat sur Bing ne présente pas les entrées de notre recherche OSINT, il s'agit peut-être de profils ou posts liés à la personne que l'on recherche.

En testant les dorks manuellement, j'avais remarqué que parfois les moteurs présentent des résultats qui ne semblent pas pertinents au premier abord, mais qui au final ont un lien avec notre recherche.

Par exemple, lorsque je tapais mon pseudo, je trouvais un profil Twitter qui n'avait rien à voir avec moi. Mais en cliquant dessus j'ai trouvé un vieux commentaire que j'avais laissé sous un de ses posts.

## Listes de ressources humaines et CV

On a vu précedemment que l'on pouvait filtrer par type de fichier, mais on ne s'en est toujours pas servi. C'est le moment !

On va pouvoir filtrer sur les PDF pour les CV et par feuille de calcul pour les mailing lists de RH.

Encore une fois, avec un exemple c'est plus parlant :

* `"toto@toto.com" filetype:csv | filetype:xls | filetype:xlsx`
* `"CV" OR "Curriculum Vitae" filetype:PDF "John" "Doe"`

Là encore on ne filtre pas derrière.

# Structure des résultats

J'ai représenté les résultats avec la dataclass SearchResult. L'utilisation des dataclass oblige l'utilisateur à utiliser Python 3.7 au minimum, mais j'avais très envie de tester cette nouvelle fonctionnalité de Python !

```py
# bing_search.py

@dataclass
class SearchResult:
    title: str = 'Untitled'
    url: str = 'No URL'
    caption: str = 'No caption'
    category: str = 'other'
```

Mon scraper récupère le titre, la description, et le lien du résultat. J'ai rajouté le champ *category* afin de pouvoir rajouter cette information moi-même pendant les étapes de mon OSINT. Cela permet par la suite de mieux filtrer les résultats.

Les catégories sont par exemple :

* social media
* real name
* email
* username
* CV

# Présentation des résultats

L'utilisation d'un fichier de logs pour les résultats me semblait être la meilleure option.

Cela permet de facilement filtrer les résultats avec `grep`, et de cliquer sur les URLs qui nous intéressent.

<!-- ```
$ python3 main.py --username zboubinours --email rodolphe.guillaume@epita.fr
Searching Namespace(email='rodolphe.guillaume@epita.fr', firstname=None, lastname=None, username='zboubinours')...
Results available in /home/rod/projects/python-osint/osint_result.log...

$ grep -i '\[social media\]' osint_result.log
[SOCIAL MEDIA][twitter.com] neal (@zboubinours) | twitter || the latest tweets from neal (@zboubinours). mrou. xoxo. arcachon (@ https://twitter.com/zboubinours)
[SOCIAL MEDIA][twitter.com] nate finch on twitter: "problem solved. #golang… || 8/21/2017 · tweet with a location. you can add location information to your tweets, such as your city or precise location, from the web and via third-party applications. (@ https://twitter.com/natethefinch/status/899730215957561344)
[SOCIAL MEDIA][www.facebook.com] corentin anciaux is back !!!!!!!!! live... - corentin ... || corentin anciaux is back !!!!! live from 24h louvain-la-neuve, kissouille les zboubinours (@ https://www.facebook.com/114023142137383/videos/175039282702435)
``` -->

![img](https://i.imgur.com/RhE2tu9.png)

# Difficultés rencontrées

Le plus difficile à été de trouver des requêtes pertinentes et de trouver un moyen de retirer un maximum de résultats inutiles.

Le problème est qu'en étant trop selectif on peut perdre des résultats intéressants, comme expliqué dans la partie réseaux sociaux, où parfois des résultats indexés sont pertinents lorsque l'on prend le temps d'aller voir nous même le contenu de la page indexée.

Cependant cette difficulté est surtout un axe d'amélioration possible du programme.

# Axes d'amélioration

En parlant d'axes d'amélioration, en plus de la précision et la quantité des résultats, on pourrait également proposer une expérience utilisateur plus agréable.

J'avais pensé à une présentation sous la forme d'un front web avec Flask et Jinja2 en utilisant les composants Card et List de Bootstrap.

La possibilité d'extraire les résultats sous forme de CSV ou Excel serait également un plus.

Enfin, l'utilisation de Bing me gêne un peu. Je préfererais mixer Google et DuckDuckGo. Le premier est le plus pertinent et puissant pour les recherches, et le second permet d'obtenir des résultats sans le filtre magique de Google qui adapte les résultats en fonction de l'utilisateur.

# Ressources utilisées

* [Google Search with python](https://stackoverflow.com/questions/37083058/programmatically-searching-google-in-python-using-custom-search)
* [Automating OSINT blog](http://www.automatingosint.com/blog/)
* [How to OSINT medium](https://medium.com/@Peter_UXer/osint-how-to-find-information-on-anyone-5029a3c7fd56)
* [How to Scrape Bing Search Results with Python](https://www.rubydevices.com.au/blog/how-to-scrape-bing)
* [BeautifulSoup and Bing Search](https://stackoverflow.com/questions/47928608/how-to-use-beautifulsoup-to-parse-google-search-results-in-python)
* [Tutoriel python logging](https://docs.python.org/fr/3/howto/logging.html)