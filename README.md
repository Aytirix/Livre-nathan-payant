/!\ Ce programme est uniquement à des fins éducatives et il est totalement illégal de ne pas payer pour les livres ! /!

Programme permettant de télécharger n'importe quel livre édité par Nathan.

PS : La faille de sécurité qui permet de télécharger presque n'importe quel livre sans être connecté à un compte a été corrigée par Nathan.

La faille de sécurité permettant de télécharger presque n'importe quel livre sans être connecté à un compte fonctionnait sous certaines conditions spécifiques :

Le livre devait avoir une version numérique disponible.
Une version Spécimen à feuilleter devait être disponible.
Un extrait papier devait également être disponible.
Lorsque l'on cliquait sur "Extrait papier", le livre s'affichait en version numérique avec environ 25 pages. En examinant le trafic réseau avec un filtre "xhtml", on pouvait remarquer qu'une requête contenait le livre à afficher, nommée "TOC.xhtml".

En utilisant l'URL "https://biblio.nathan.fr/epubs/NATHAN/bibliomanuels/distrib_gp/2/3/12188/online/OEBPS/TOC.xhtml", toutes les pages jusqu'à la page 38 étaient accessibles.

Dans cette URL, l'identifiant de l'extrait du livre était 12188. Avec un programme, il était facile de comparer le contenu de la page gratuite avec d'autres identifiants, tels que 12189, 12187, 12190, 12186, etc.

En effet, tout le contenu de la page TOC.xhtml en version gratuite devrait être présent dans la version payante du livre. Ainsi, en comparant cela avec le contenu de toutes les autres pages et en trouvant une correspondance, il était normalement possible de trouver la version payante du livre.

Par exemple, le lien vers la version payante du lien ci-dessus était :
"https://biblio.nathan.fr/epubs/NATHAN/bibliomanuels/distrib_gp/2/3/12187/online/OEBPS/TOC.xhtml"
Il n'y avait qu'un seul écart entre la version gratuite et la version payante.
Le plus grand écart observé était de 300 entre une version gratuite et une version payante.
