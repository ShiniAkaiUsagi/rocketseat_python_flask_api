import re


def is_valid_cpf(cpf: str) -> bool:
    """Valida CPF com base nos dígitos verificadores."""
    cpf = "".join(filter(str.isdigit, cpf))

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    def calc_dv(digits):
        soma = sum(int(d) * w for d, w in zip(digits, range(len(digits) + 1, 1, -1)))
        resto = soma % 11
        return "0" if resto < 2 else str(11 - resto)

    dv1 = calc_dv(cpf[:9])
    dv2 = calc_dv(cpf[:9] + dv1)

    return cpf[-2:] == dv1 + dv2


def is_valid_email(email: str) -> bool:
    """Valida formato de e-mail com regex simples."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email))
