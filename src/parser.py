
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def advance(self):
        self.position += 1

    def expect(self, token_type):
        token = self.current_token()

        if token is None or token[0] != token_type:
            raise SyntaxError(
                f"Token attendu : {token_type}, reçu : {token}"
            )

        self.advance()
        return token

    # NUMBER
    def parse_number(self):
        token = self.expect("NUMBER")

        return {
            "type": "Number",
            "value": int(token[1])
        }

    # NUMBER | IDENTIFIER | "(" expression ")"
    def parse_factor(self):
        token = self.current_token()

        if token is None:
            raise SyntaxError("Expression incomplète")

        if token[0] == "NUMBER":
            return self.parse_number()

        if token[0] == "IDENTIFIER":
            self.advance()
            return {
                "type": "Identifier",
                "name": token[1]
            }

        if token[0] == "LPAREN":
            self.advance()
            node = self.parse_expression()
            self.expect("RPAREN")
            return node

        raise SyntaxError(f"Facteur invalide : {token}")

    # factor (("*" | "/") factor)*
    def parse_term(self):
        node = self.parse_factor()

        while (
            self.current_token() is not None
            and self.current_token()[0] in ("STAR", "SLASH")
        ):
            operator = self.current_token()[1]
            self.advance()

            right = self.parse_factor()

            node = {
                "type": "BinaryOp",
                "operator": operator,
                "left": node,
                "right": right
            }

        return node

    # term (("+" | "-") term)*
    def parse_expression(self):
        node = self.parse_term()

        while (
            self.current_token() is not None
            and self.current_token()[0] in ("PLUS", "MINUS")
        ):
            operator = self.current_token()[1]
            self.advance()

            right = self.parse_term()

            node = {
                "type": "BinaryOp",
                "operator": operator,
                "left": node,
                "right": right
            }

        return node

    # let IDENTIFIER = expression ;
    def parse_let(self):
        self.expect("LET")
        name = self.expect("IDENTIFIER")[1]
        self.expect("EQUAL")

        value = self.parse_expression()

        self.expect("SEMICOLON")

        return {
            "type": "LetStatement",
            "name": name,
            "value": value
        }

    # print ( expression ) ;
    def parse_print(self):
        self.expect("PRINT")
        self.expect("LPAREN")

        value = self.parse_expression()

        self.expect("RPAREN")
        self.expect("SEMICOLON")

        return {
            "type": "PrintStatement",
            "value": value
        }

    def parse_statement(self):
        token = self.current_token()

        if token is None:
            raise SyntaxError("Instruction attendue")

        if token[0] == "LET":
            return self.parse_let()

        if token[0] == "PRINT":
            return self.parse_print()

        raise SyntaxError(f"Instruction inconnue : {token}")

    def parse(self):
        statements = []

        while self.current_token() is not None:
            statements.append(self.parse_statement())

        return {
            "type": "Program",
            "body": statements
        }
