### Projet : Parseur YAML avec Automate à Pile

#### Description

Ce projet implémente un parseur pour le langage YAML en utilisant un automate à pile. Le parseur analyse un document YAML et détermine s'il est valide selon la grammaire définie.

#### Structure du Projet

- **parser.py** : Parseur syntaxique principal.
- **tokenizer.py** : Analyseur lexical pour convertir le texte en tokens.
- **examples/** : Contient des exemples de fichiers YAML (valides et invalides).

#### Prérequis

- Python 3.x

#### Installation

1. Cloner le dépôt :

   ```bash
   git clone https://github.com/thomas-brn/yaml_parser
   ```

2. Naviguer dans le répertoire :

   ```bash
   cd yaml_parser
   ```

#### Utilisation

1. Placer le fichier YAML à analyser dans le répertoire.

2. Exécuter le parseur :

   ```bash
   python parser.py <fichier.yaml>
   ```

#### Exemples

- Analyser un fichier valide :

  ```bash
  python parser.py examples/valid_example.yaml
  ```

- Analyser un fichier invalide :

  ```bash
  python parser.py examples/invalid_example.yaml
  ```

## Grammaire du Langage YAML

La grammaire suivante définit une version simplifiée du langage YAML, exprimée en utilisant la **Forme de Backus-Naur étendue (EBNF)**. Cette grammaire sert de base pour le parseur implémenté dans le projet.

```ebnf
<document> ::= (<élément>)*

<élément> ::= <commentaire>
            | <clé_valeur>
            | <séquence>
            | <mapping>

<commentaire> ::= '#' <texte> '\n'

<clé_valeur> ::= <indentation> <clé> ':' <espace>? <valeur>? '\n'

<clé> ::= <scalair>

<valeur> ::= <scalair>
           | <séquence>
           | <mapping>

<séquence> ::= (<indentation> '-' <espace>? <valeur>? '\n')+

<mapping> ::= (<clé_valeur>)+

<scalair> ::= <chaîne>
            | <nombre>
            | <booléen>
            | <null>

<chaîne> ::= '"' [^"\n]* '"'          (* Chaîne entre guillemets doubles *)
            | "'" [^'\n]* "'"         (* Chaîne entre guillemets simples *)
            | [^\s:#\[\]\{\}][^\n#]*  (* Chaîne non encadrée *)

<nombre> ::= '-'? [0-9]+ ('.' [0-9]+)?

<booléen> ::= 'true' | 'false'

<null> ::= 'null' | '~'

<espace> ::= ' ' | '\t'

<indentation> ::= (<espace>)*

<texte> ::= [^\n]*

```

### Explications :

- **<document>** : Représente un document YAML complet composé de zéro ou plusieurs éléments.
  
- **<élément>** : Peut être un commentaire, une paire clé-valeur, une séquence ou un mapping.
  
- **<commentaire>** : Une ligne commençant par `#` suivie de n'importe quel texte jusqu'à la fin de la ligne.
  
- **<clé_valeur>** : Une clé suivie de `:`, éventuellement suivie d'un espace et d'une valeur. La valeur peut être absente (dans le cas où une structure imbriquée suit).
  
- **<clé>** : Un scalaire représentant la clé dans une paire clé-valeur.
  
- **<valeur>** : Peut être un scalaire, une séquence ou un mapping.
  
- **<séquence>** : Une ou plusieurs lignes commençant par `-` (tiret), suivies d'une valeur optionnelle.
  
- **<mapping>** : Une ou plusieurs paires clé-valeur, potentiellement imbriquées en utilisant l'indentation.
  
- **<scalair>** : Une valeur scalaire qui peut être une chaîne, un nombre, un booléen ou null.
  
- **<chaîne>** : Peut être une chaîne entre guillemets simples ou doubles, ou une chaîne non encadrée sans caractères spéciaux.
  
- **<nombre>** : Un entier ou un nombre à virgule flottante, éventuellement précédé d'un signe moins.
  
- **<booléen>** : Les littéraux `true` ou `false`.
  
- **<null>** : Représente une valeur nulle, avec les littéraux `null` ou `~`.
  
- **<espace>** : Un espace ou une tabulation.
  
- **<indentation>** : Zéro ou plusieurs espaces ou tabulations, utilisé pour définir le niveau d'indentation.
  
- **<texte>** : N'importe quel caractère sauf un saut de ligne.

### Notes Importantes :

- **Indentation** : L'indentation est significative en YAML. Les éléments imbriqués doivent être correctement indentés par rapport à leur parent. Le parseur utilise l'indentation pour déterminer la structure hiérarchique du document.
  
- **Commentaires** : Les commentaires commencent par `#` et s'étendent jusqu'à la fin de la ligne. Ils sont ignorés par le parseur.
  
- **Séquences** : Les séquences sont définies par des lignes commençant par `-` (tiret). Chaque élément de la séquence peut être un scalaire, un mapping ou une autre séquence.
  
- **Mappings** : Les mappings sont des collections de paires clé-valeur. Une clé est suivie de `:`, puis d'une valeur. Les mappings peuvent être imbriqués pour représenter des structures de données complexes.
  
- **Scalaires** : Les scalaires représentent des valeurs simples comme les chaînes de caractères, les nombres, les booléens et les valeurs nulles.
  
- **Chaînes Non Encadrées** : Les chaînes peuvent être non encadrées si elles ne contiennent pas d'espaces ou de caractères spéciaux tels que `:`, `#`, `[`, `]`, `{`, `}`.

### Exemples :

1. **Paire Clé-Valeur Simple :**

   ```yaml
   nom: "Alice"
   ```

   - `<clé_valeur>` avec `<clé>` = `nom` et `<valeur>` = `"Alice"`

2. **Séquence de Scalaires :**

   ```yaml
   - Pomme
   - Banane
   - Cerise
   ```

   - `<séquence>` de `<scalair>` non encadrés.

3. **Mapping Imbriqué :**

   ```yaml
   personne:
     nom: "John"
     âge: 25
   ```

   - `<mapping>` où la `<clé>` est `personne` et la `<valeur>` est un autre `<mapping>` avec les paires `nom: "John"` et `âge: 25`.

4. **Séquence de Mappings :**

   ```yaml
   - nom: "Johnny"
     âge: 30
   - nom: "Joe"
     âge: 40
   ```

   - `<séquence>` dont chaque élément est un `<mapping>`.
