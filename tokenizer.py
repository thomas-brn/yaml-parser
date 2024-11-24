# Ce fichier contient le code pour le tokenizer, qui convertit une chaîne de texte en une liste de tokens.
# Les tokens sont des objets qui représentent les éléments de base du langage YAML, tels que les clés, les valeurs et les éléments de séquence.
# Le tokenizer utilise des expressions régulières pour identifier les différents types de tokens dans le texte d'entrée.
# Chaque token contient des informations sur son type, sa valeur, son niveau d'indentation et le numéro de ligne où il se trouve.
# Le tokenizer génère une liste de tokens à partir du texte d'entrée, qui est ensuite utilisée par le parser pour analyser la structure du document YAML.

import re

class Token:
    def __init__(self, type_, value, indent_level=0, line_number=0):
        self.type = type_ # Type du token (KEY, VALUE, DASH, COMMENT)
        self.value = value # Valeur du token
        self.indent_level = indent_level # Niveau d'indentation du token
        self.line_number = line_number # Numéro de ligne du token

    def __repr__(self):
        return f"Token(type={self.type}, value={self.value}, indent_level={self.indent_level}, line={self.line_number})"


def tokenize(input_text):
    tokens = []
    lines = input_text.split('\n')  # Divise le texte d'entrée en lignes individuelles
    
    ## Par exemple, si le texte d'entrée est:
    ## key1: value1
    ## key2: value2
    ## - item1
    ## - item2
    ## - item3
    
    ## Le texte sera divisé en une liste de lignes:
    ## ['key1: value1', 'key2: value2', '- item1', '- item2', '- item3']
    
    # Parcours les lignes du texte d'entrée
    for line_number, line in enumerate(lines, start=1):
        original_line = line  # Conserve la ligne originale pour les messages d'erreur
        
        # Ignore les lignes vides
        if not line.strip():
            continue

        # Gestion des commentaires
        if re.match(r'^\s*#', line):  # Si la ligne commence par un commentaire
            tokens.append(Token('COMMENT', line.strip(), line_number=line_number))  # Ajoute un token de type COMMENT
            continue

        # Retire les commentaires de la ligne, par exemple:
        # "key: value # Commentaire" devient "key: value
        line = re.sub(r'#.*$', '', line).rstrip()  # Supprime tout ce qui suit un '#' et les espaces en fin de ligne
        if not line.strip():  # Si la ligne est vide après avoir retiré le commentaire
            continue

        # Calcul du niveau d'indentation, par exemple:
        # "  key: value" a un niveau d'indentation de 2
        indent_level = len(line) - len(line.lstrip(' '))  # Compte le nombre d'espaces en début de ligne

        # Vérification des paires clé-valeur
        key_value_match = re.match(r'^\s*(\S.*?)\s*:\s*(.*)', line)  # Vérifie si la ligne correspond à une paire clé-valeur
        if key_value_match:
            key = key_value_match.group(1)  # Extrait la clé
            value = key_value_match.group(2)  # Extrait la valeur
            tokens.append(Token('KEY', key.strip(), indent_level, line_number))  # Ajoute un token de type KEY
            if value:
                tokens.append(Token('VALUE', value.strip(), indent_level, line_number))  # Ajoute un token de type VALUE si une valeur est présente
            continue

        # Vérification des éléments de séquence
        seq_match = re.match(r'^\s*-\s*(.*)', line)  # Vérifie si la ligne correspond à un élément de séquence
        if seq_match:
            value = seq_match.group(1)  # Extrait la valeur après le tiret
            tokens.append(Token('DASH', '-', indent_level, line_number))  # Ajoute un token de type DASH
            if value:
                tokens.append(Token('VALUE', value.strip(), indent_level, line_number))  # Ajoute un token de type VALUE si une valeur est présente
            continue

        # Si la ligne ne correspond à aucune structure connue, lever une exception
        raise Exception(f"Erreur lexicale à la ligne {line_number}: '{original_line.strip()}'")  # Lève une exception pour une ligne non reconnue

    return tokens  # Retourne la liste des tokens générés
