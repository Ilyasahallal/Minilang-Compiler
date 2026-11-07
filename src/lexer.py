def tokenize(source: str):
    tokens = []
    i = 0
    n = len(source)

    KEYWORDS = {
        "let": "LET",
        "print": "PRINT"
    }

    OPERATORS = {
        "+": "PLUS",
        "-": "MINUS",
        "*": "STAR",
        "/": "SLASH",
        "=": "EQUAL",
        ";": "SEMICOLON",
        "(": "LPAREN",
        ")": "RPAREN"
    }

    while i < n:
        char = source[i]

        if char.isspace():
            i += 1

        elif char.isalpha() or char == "_":
            start = i

            while i < n and (
                source[i].isalnum() or source[i] == "_"
            ):
                i += 1

            word = source[start:i]

            if word in KEYWORDS:
                tokens.append((KEYWORDS[word], word))
            else:
                tokens.append(("IDENTIFIER", word))

        elif char.isdigit():
            start = i

            while i < n and source[i].isdigit():
                i += 1

            number = source[start:i]
            tokens.append(("NUMBER", number))

        elif char in OPERATORS:
            tokens.append((OPERATORS[char], char))
            i += 1

        else:
            raise ValueError(f"Caractère inconnu : {char}")

    return tokens