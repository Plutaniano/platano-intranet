import re

from flask import flash
from typing import Union, Tuple

def validate_nome(nome: str) -> Union[bool, str]:
    nome = nome.strip().title()

    if len(nome) < 10:
        flash('Nome muito curto.')
        return False
    
    if any(char.isdigit() for char in nome):
        flash('Seu nome não pode conter números.')
        return False
    
    return nome

def validate_codigo(codigo: str) -> Union[bool, int]:
    codigo = codigo.strip()
    regex_expr = r"\b[aA]{0,1}\d{5}\b"
    result = re.match(regex_expr, codigo)

    try:
        return result[0]
    except (IndexError, TypeError):
        flash('Código A inválido.')
        return False



def validate_password(password: str, confirm: str) -> Union[bool, Tuple[str, str]]:
    if len(password) < 6:
        flash('Senha muito curta.')
        return False

    if password != confirm:
        flash('Senhas não batem.')
        return False
    
    return (password, confirm)


def validate_email(email: str) -> Union[bool, str]:
    email = email.strip()
    regex_expr = r"\S+@\S+\.\S+"
    result = re.match(regex_expr, email)
    print(result)

    try:
        return result[0]
    except (IndexError, TypeError):
        flash('Email inválido.')
        return False

