# Modélisation de sujet par des modéles de Machine Learning à partir des projet et propostions de lois lors du mandat Macron 2017-2022 et 2022-2027



### But 
Ce projet présenté dans le cadre du module "Projet démo" du Master Data/IA d'HETIC. 
Le but de ce projet est de comprendre les champs lexicaux utilisés par les différentes groupes politiques et déput-ées (mais aussi du Gouvernement) de la légistature précédante puis actuelle à partir des projets/propositions de Lois déposées. Grâce à différents modéles d'IA

Afin d'avoir un modéle robuste et pertinant c'est la légistature précédantes qui sera utilisé (Macron 2017-2022) puis actuelle (Macron 2022-2027). 

<details>
<summary> + d'info sur le choix de la donnée</summary>
Afin d'avoir un modéle robuste et pertinant c'est la légistature précédantes qui sera utilisé (Macron 2017-2022) puis actuelle (Macron 2022-2027). 
Nous sommes aux début de la nouvelle légistature, donc il le nombre de données et restraint. Avec peu de données les modéles 
risque d'être surentrainé ou sous-entrainer 
</details>

### Rappels
La différence entre projets et propositions de Lois : 
* Les projets de Lois sont déposés par les membres du gouvermenents
* Les proposistions de Lois sont déposés par les député-es

Initialement le projet devais étudiés les ammendements, mais contenue de différents problémes rencontrés (listé ci-dessous) les propositions de projet de Lois seront étudiées.

* Des député-es et groupes politiques déposé des ammendements que l'on pourrait qualifier d'inutile 
  * Changer un mot ou une expression par une autre afin de ralentir le travail parlementaire 
  * Modifications pour enlever tous sens aux textes déposés et ralentir le travail parlementaire 


###  Scraping des projets et propositions de Lois 
* Utilisation de BS4
*  utilisation de REGEX pour récupérer tous les  propositions/projets de Lois 
*  Nettoyage de la donnée
   * Stop word 
   * Ponctuation
   * Balise HTML/CSS 
  
* Fichier CSV avec les collonnes suivantes :
  * date
  * Personnes ayant déposées
    * Projet de Lois : par défaut gouververnement 
    * Propositions de Lois 
      * Dans une 1er version : groupe politique 
      * Dans une 2nd versions : groupe politique et député-e-s
    * Exposés des motifs 

### Traitement de la données 
L'utilisation de plusieurs de plusieurs modéles IA sera nécessaire afin comprendre les champs lexiaux utilisés.

Nuage de mots : worldcloud 

### Livrable
* Web app python pour présenter les résultats
### [Draft] Technics 
* Fait sur google collab puis récuperation de la données 
* Stockage dans une solution cloud ?
* Train dans une solution cloud ? 

### About me 
Je suis Camille L. étuditant-e en 1ére année de Master Data/IA à HETIC (Montreuil). Je suis une personne non-binaire, j'utilise les pronoms iel/iels (ou il/elle quand si vous n'êtez pas comfortable avec le pronom iel) et accord neutre en français. 
Pour plus d'information sur mes projets passés, en cours ou à venir hésitez pas à visiter mon [site](https://camlebrun.github.io)

