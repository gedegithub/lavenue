<div align="center">
<img width=200 src="https://raw.githubusercontent.com/tienne-B/lavenue/master/logo.svg?sanitize=true">

# Lavenue
</div>

Pour la bonne gestion et sémantique d'assemblée délibérante, *Lavenue* est un logiciel proposé pour faciliter l'utilisation du *Code Lespérance* (CL) et d'automatiser l'application des décisions faites. L'implémentation de ce logiciel se fera en python avec le framework Django, pour des raisons pragmatiques.

## Contexte
À la suite des instances de la FAÉCUM qui se déroulaient de manière virtuelle en hiver 2021, des failles importantes avec la capacité de pouvoir tenir ces rencontres sans outils à ces fins ont été soulevées. Ces failles font que c'est plus dur aux participants de pouvoir facilement interagir avec les procédures pour faire des propositions, ainsi que de connaitre l'ordre de parole qui est opaque.

### But
Ce logiciel va être basé sur l'internet avec deux grands axes. La première est d'augmenter la transparence des assemblées en facilitant les interactions et demandes et de supporter la présidence et secrétariat avec leurs travaux. La deuxième est dans la génération de documentation, pour automatiser les procès-verbaux et des résolutions. Un effet tierce de cet effort est la capacité d'analyser les assemblées en tant que données à des fins de recherche.

### Public cible et utilisation
*Lavenue* pourra être utilisé par les associations étudiantes qui utilisent le *Code Lespérance* ou des codes similaires. Ces associations l'utiliseront durant leurs assemblées par tout parti:
* les participants pour demander la parole et faire des propositions;
* la présidence pour octroyer des tours de parole et prendre des actions;
* le secrétariat pour rédiger des sommaires des interventions.

Ce logiciel sera aussi utilisé au préalable par des officiers de l'association afin de mettre un horaire pour l'assemblée.

Entretemps, le public peut accéder aux ressources informationnelles comme les procès-verbaux qui ont été rédigés sur la plateforme.

### Portée du projet
La portée du projet consiste à l'implémentation des procédures et des exigences du *Code Lespérance* pour le déroulement et proposition d'assemblée délibérante, ainsi que la création de documents connexes aux procédures.

Ce qui n'est pas dans la portée inclut la gestion et présentation des rapports et documentation non structurée qui peuvent faire partie des instances. Nous n'allons pas non plus nous occuper des exigences audiovisuelles pour les assemblées.

### Définitions
* Code Lespérance (CL): Un code de procédure pour les assemblées délibérantes
* Procès-verbal (PV): Document qui récapitule les procédés d'une assemblée (CL Annexe B.1)

Les propos qui font référence à des règles de procédure seront indiqués avec une note (CL #) avec la règle ou partie du code.

### Assomptions
La grande assomption ici est qu'il y a une structure informatisable créé par l'utilisation de procédures fixes et de l'adaptabilité de cette structure en logiciel. Une divergence entre les attentes du logiciel avec le déroulement de l'assemblée réel pourrait rendre plus difficile et frustrant d'utilisation. Même si pas formalisé, il peut avoir des différences entre les l'application des procédures en théorie par le CL et l'utilisation en practice.

## Besoins des utilisateurs
### Observateurs
* S'ajouter/se retirer à l'ordre de parole
* Faire des interventions prioritaires (point d'ordre/de privilège)
* Voir l'ordre de parole et des points
* Voir les propositions

### Participants
* *Les capacités des observateurs +*
* Faire des propositions
* Créer des (sous-)amendements
* Voter

### Secrétariat
* Ajouter des tours de parole au nom d'autrui
* Écrire des propositions au nom d'autrui
* Écrire des sommaires pour les interventions
* Voter

### Présidence
* Donner des tours de parole
* Accepter des propositions
* Fermer la scéance
* Voter

### Non-participants
* Voir calendrier des instances
* Voir documentation structuré des instances (résolutions/PVs)
* S'inscrire/se connecter pour l'accès

## Solutions
### Gestion d'assemblée
Un utilisateur administrateur (Le Secrétaire) peut créer un objet `assemblee` avec un nom, puis y ajouter des `seance`s qui comportent une date et heure de début et fin. Lors de la création de l'objet, des liens sont générés avec du hashage pour qu'autres utilisateurs peuvent s'y joindre avec le rôle attribué avec le lien spécifique pour:
* Membre/Observateur
* Présidence
* Secrétariat

Les liens ne seront pas divulgués ni devinable du à l'hashage. C'est au créateur de l'événement de faire la distribution. Une autre option aussi serait a l'administrateur d'attribuer un 'username' et un 'password' à chaque utilisateur de l'application web. Les séances seront par contre ajoutées automatiquement à un calendrier `iCal` public avec le nom de l'assemblée et détail connexes.

En se connectant à une assemblée par un lien attribué, les niveaux de permission de l'utilsateur seraient déjà été attribués, ce qui serait aussi réflété dans son interface, à savoir si l'utilisateur est votant ou non avec des attributs de prendre la parole. Ceci va créer un objet `intervenant` de l'`assemblee` qui peut être attaché à un `utilisateur` du site. Cet objet portera aussi des attributs pour le rôle de l'intervenant comme énumération:
* Observateur
* Membre
* Présidence
* Secrétariat

Avec la création d'assemblée se fera aussi la création initiale de l'ordre du jour. Chaque item de l'ordre du jour est un objet `point` qui inclut la `seance`, le numéro le plus spécifique du point, le point parent (s'il a lieu) et le nom. Pour clarifier avec un exemple, un point "4.3.2" aura le numéro "2" et le point parent le point avec numéro "3" qui lui aurait le "4".

#### Interface de participant
##### Interface principale
Les participants auront comme page principale une interface avec:
* Bouton pour demander un tour de parole
* Boutons pour point d'ordre ou privilège
* La libellé du point ou proposition actuelle
* Liste des propositions préparées

Pour demander, la parole, comme tour ordinaire ou privilégié, sera avec des boutons qui envoient comme message par WebSocket la demande, avec type si spécifié ainsi que la priorité accordée. Le bouton devient après pour retirer sa demande, qui est traitée de la même façon. Quand le tour est pris, un message WebSocket sera reçu pour l'indiquer sur l'interface et réinitialiser le bouton.

Chaque demande crée un objet `intervention` qui prend l'`intervenant` demandeur, le `point` actuel, la `proposition` actuelle, le type d'intervention, la séquence de l'intervention et le tour de parole. Comme types d'intervention, il y a:
* Ordinaire
* D'ordre
* De privilège

##### Création de propositions
Le secrétaire peut créer des objets `proposition`, qui ont un type associé comme énumération des items dans CL 58, 59, 60, 61 et 62. Ces propositions seront attachées par la suite à une `intervention` quand présentées, soit par la personne durant son temps de parole ou par le secrétariat. L'utilisateur peut aussi indiquer s'il s'agit une position, donc du numéro (0 si pas attribué ou nul si pas une position). Un préambule et la libellée sont aussi modifiables.

Les propositions ont une URL unique hashé pour permettre autres participants accès. Autres participants peuvent l'amender, ce qui est avec la même interface, mais avec un champ qui indique la proposition qu'il remplace. Les amendements seront saisis comme un tout, avec la différence entre les versions calculées automatiquement (`diff`).

##### Vote
Si la proposition ne reçoit pas de débat ou que la présidence ouvre le vote, les utilisateures cliquent sur le bouton 'vote', ce qui crée un objet `vote` attaché à une proposition. Les objets ont des attributs pour le nombre de votes pour, contre, abstentions, et si le vote a passé. Les votes par unanimité ne font pas d'objet de vote.

Avec une demande de vote, les trois options sont présentées aux participants éligibles, qui envoie par WebSocket leurs choix ou s'ils se retirent.

Et le décomptage du nombre de bulletins determine si la proposition est passée ou pas.

#### Interfaces de présentation
Il y a un couple d'interfaces de lecture (pour présenter):
* Une liste de l'ordre de parole futur
* La proposition en étude

Ce premier indiquerait le point actuel et proposition en haut, puis s'il y a des points privilégiés (et par qui), puis une liste de l'ordre de parole non épuisé, qui indique (par séparation ou note) leur tour.

La proposition en étude serait un raccourci de la page de proposition en lecture seule, qui inclut le préambule.

#### Interface du secrétariat
La page principale du secrétariat comporte une indication de la `proposition` et `intervention` actuelle, avec un champ pour écrire à propos du discours. Il sera aussi possible de voir les `proposition`s de l'`intervenant` puis les attacher à l'`intervention`, ou d'en créer au nom de l'`intervenant`.

Toute modification aux objets doivent être disponible en temps réel aux autres `intervenant`s du secrétariat, fait avec des `WebSocket`s.

Le secrétariat peut aussi voir l'ordre des `interventions` et peut modifier les privilèges des utilsateurs, en modifiant et/ou révoquant leurs droits et types.

Un administrateur peut entre autres:
* Créer des assemblées/séances
* Inviter des utilisateurs aux assemblées
* Voir documentation publique
* Voir documentation restreinte
* Se connecter aux assemblées

#### Interface de présidence
La page principale de la présidence comporte le `point` et la `proposition` actuelle avec l'ordre de parole. En sélectionnant un nom sur l'ordre, le message `WebSocket` pour l'échange d'`intervention` est envoyé pour mettre à jour les interfaces. Il a aussi un bouton pour indiquer son intervention et pour passer au `vote` de la `proposition` actuelle. Dans le admin on peut deceler facilement l'existence de duplicates entre noms, pour s'assurer que des délégations n'ont pas plus de votes qu'accordé.

La présidence à aussi une liste des `intervenant`s à prendre la parole selon l'ordre attribué. Ce qui permettrait aux autre utilisateurs de suivre l'ordre de prise de parole. 

### Génération de documentation
La structure des données collectées permettrait à la génération de certains documents qui découlent de l'assemblée. Ceux-ci incluent:
* l'ordre du jour
* les procès-verbaux
* les résolutions
* le cahier de positions

Toute la documentation générée est tres bien stockée dans le Django admin sous forme de formulaires, accessible en tout temps par le secrétariat, l'administrateur du logiciel.