class Simbolo:
    """ Representa un símbolo individual de la gramática.
    Atributos privados:
        nombre (str): El nombre o valor del símbolo (ej: 'E', '+', 'num').
        es_terminal (bool): True si el símbolo es terminal, False si es no-terminal. """
    def __init__(self, nombre: str, es_terminal: bool = False) -> None: #los : son para indicar el dato esperado
        """Constructor que se inicializa cuando creo un símbolo con su nombre y tipo."""
        self._nombre: str = nombre
        self._es_terminal: bool = es_terminal
    #Son los metódos para acceder a los atributos privados.
    @property       #esto hace que el metódos se pueda usar como un atributo, es decir, sin paréntesis.
    def nombre(self) -> str:
        """Retorna el nombre del símbolo."""
        return self._nombre

    @property
    def es_terminal(self) -> bool:
        """Retorna True si el símbolo es terminal."""
        return self._es_terminal

    @es_terminal.setter #Permite modigicar es_terminal
    def es_terminal(self, valor: bool) -> None:
        #Permite actualizar el tipo del símbolo (usado por Gramatica al parsear).
        self._es_terminal = valor

    def __repr__(self) -> str: #Representación legible del símbolo, indicando su nombre y si es terminal o no.
        tipo = "T" if self._es_terminal else "NT"
        return f"Simbolo({self._nombre!r}, {tipo})"

    def __eq__(self, other: object) -> bool: #Compara dos símbolos por su nombre, ignorando si son terminales o no.
        if isinstance(other, Simbolo):
            return self._nombre == other._nombre
        return False

    def __hash__(self) -> int: #Permite usar símbolos como claves en diccionarios/elementos de conjuntos, basándose solo en su nombre.
        return hash(self._nombre)
