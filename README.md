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


[injection SQL]: https://fr.wikipedia.org/wiki/Injection_SQL