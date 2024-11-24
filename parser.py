# Ce fichier contient le code pour le parseur, qui analyse la structure d'un document YAML à partir de la liste de tokens générée par le tokenizer.

from tokenizer import tokenize, Token

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens  # Liste des tokens à analyser
        self.current = 0  # Index du token actuel
        self.success = True  # Indicateur de succès de l'analyse

    def parse(self):
        try:
            while self.current < len(self.tokens):
                self.element()  # Analyse chaque élément
            return True  # Retourne True si l'analyse est réussie
        except Exception as e:
            print(f"Parsing error: {e}")  # Affiche l'erreur de parsing
            return False  # Retourne False si une erreur est rencontrée

    def element(self):
        token = self.tokens[self.current]  # Récupère le token actuel
        if token.type == 'COMMENT':
            self.current += 1  # Ignore les commentaires
        elif token.type == 'KEY':
            self.mapping()  # Analyse une paire clé-valeur
        elif token.type == 'DASH':
            self.sequence()  # Analyse un élément de séquence
        elif token.type == 'VALUE':
            self.current += 1  # Ignore les valeurs scalaires seules
        else:
            raise Exception(f"Unexpected token {token}")  # Lève une exception pour un token inattendu

    # Analyse une paire clé-valeur
    # Une paire clé-valeur est composée d'une clé (KEY) et d'une valeur associée (VALUE)
    # Elle peut également contenir des mappings ou des séquences imbriqués
    def mapping(self):
        token = self.tokens[self.current]
        indent_level = token.indent_level  # Niveau d'indentation de la clé
        self.current += 1  # Passe au token suivant (après la clé)
        # Vérifie s'il y a une valeur associée à la clé
        if self.current < len(self.tokens) and self.tokens[self.current].type == 'VALUE':
            self.current += 1  # Passe au token suivant (après la valeur)
        # Vérifie les mappings ou séquences imbriqués
        while self.current < len(self.tokens) and self.tokens[self.current].indent_level > indent_level:
            self.element()  # Analyse les éléments imbriqués

    # Analyse un élément de séquence
    # Un élément de séquence commence par un tiret (-) suivi d'une valeur associée (VALUE)
    # Il peut également contenir des mappings ou des séquences imbriqués
    def sequence(self):
        token = self.tokens[self.current]
        indent_level = token.indent_level  # Niveau d'indentation de l'élément de séquence
        self.current += 1  # Passe au token suivant (après le tiret)
        # Vérifie s'il y a une valeur associée à l'élément de séquence
        if self.current < len(self.tokens) and self.tokens[self.current].type == 'VALUE':
            self.current += 1  # Passe au token suivant (après la valeur)
        # Vérifie les éléments imbriqués
        while self.current < len(self.tokens) and self.tokens[self.current].indent_level > indent_level:
            self.element()  # Analyse les éléments imbriqués

# Utilisation du parseur
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python parser.py <fichier_yaml>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        input_text = f.read()

    tokens = tokenize(input_text)  # Tokenize le texte d'entrée
    parser = Parser(tokens)  # Crée une instance du parseur avec les tokens
    result = parser.parse()  # Analyse les tokens
    if result:
        print("Le document YAML est valide.")  # Affiche un message si le document est valide
    else:
        print("Le document YAML n'est pas valide.")  # Affiche un message si le document n'est pas valide