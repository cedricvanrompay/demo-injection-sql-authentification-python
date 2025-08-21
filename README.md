# Application de démonstration de sécurité en Python

Une application Web ultra-simple
pour démontrer quelques grands principes de sécurité informatiques,
principalement les injections SQL et l'authentification.

> [!IMPORTANT]
> Cette application a beaucoup de vulnérabilités
> (c'est à dire de problèmes de sécurité).
> Ne pas réutiliser son code pour de vraies applications

L'application est une application de messagerie,
où les utilisateurs peuvent avoir des conversations les uns avec les autres.

Pour la lancer, il suffit d'avoir Python (Python 3) et de faire:

```
python serveur.py
```

Comme il n'y a besoin d'aucune autre librairie que la librairie standard,
pas besoin d'utiliser `pip`, pas besoin d'environnement virtuel etc...
Juste besoin d'avoir installé Python
(ou [Docker](https://www.docker.com/)
et utiliser [l'image Docker officielle de Python](https://hub.docker.com/_/python/#run-a-single-python-script)).

La principale vulnérabilité de cette application
est une [injection SQL][] dans la fonctionalité « Trouver un utilisateur »
(sur la page d'accueil).

D'autres fonctionalités comme la messagerie
ont aussi des vulnérabilités de type « [injection SQL][] ».

Il y d'autres problèmes de sécurité.
On peut en citer certains, ordonnées plus au moins
du plus facile au plus compliqué à identitifier:

* les mots de passes sont stockés tels quels (on dit « en clair »)
  sans [hachage de mot de passe](https://en.wikipedia.org/wiki/Key_derivation_function#Password_hashing)
* la fonctionalité « Trouver un utilisateur » est vulnérable à
  une [attaque XSS](https://fr.wikipedia.org/wiki/Cross-site_scripting)
* le mot de passe reçu est comparé au mot de passe attendu
  via une [comparaison qui ne se fait pas à temps constant](https://en.wikipedia.org/wiki/Timing_attack#String_comparison_algorithms)


## Quelques exemples d'injections SQL sur cette application

Utilisez le texte suivant dans le formulaire « Trouver un utilisateur »
(notez bien qu'il n'y a pas d'apostrophe après le deuxième `1`) :

```
alice' OR '1' = '1
```

Au lieu de vous montrer seulement un seul utilisateur,
l'application devrait lister _tous_ les utilisateurs.
Remarquez la requête SQL que le serveur a écrite
dans le terminal ou vous aviez lancé `python serveur.py`:

```
requete: SELECT pseudo, date_creation FROM utilisateurs WHERE pseudo = 'alice' OR '1' = '1'
```

On peut faire des injections SQL qui font bien plus que juste « lister tous les utilisateurs »,
par exemple:

```
' UNION SELECT pseudo, mot_de_passe FROM utilisateurs WHERE '1'='1
```

(avec une apostrophe au début mais sans apostrophe à la fin)
on voit non seulement tous les utilisateurs,
mais aussi leur mots de passe!

Notez que normalement on ne stocke pas les mots de passe tels quels dans la base de données,
on est censé appliquer un algorithme de « hachage de mot de passe ».
Mais le hachage de mot de passe n'est pas une protection absolue,
et c'est donc un très gros problème si un attaquant est capable de récupérer les mots de passe,
même haché.


## Se protéger des injections SQL

Utilisez une « requête préparée » (en Anglais: _prepared statement_),
toutes les bases de données ont cette fonctionalité.

Voir par exemple : https://docs.python.org/3/library/sqlite3.html#how-to-use-placeholders-to-bind-values-in-sql-queries


## Quelques principes généraux de sécurité

- se demander comment le programme se comporte s'il reçoit de la donnée
  à laquelle on n'avait pas pensé en écrivant le code
- se méfier des données qui viennent de l'extérieur du système
  et pourrait donc facilement être contrôlées par un attaquant


[injection SQL]: https://fr.wikipedia.org/wiki/Injection_SQL