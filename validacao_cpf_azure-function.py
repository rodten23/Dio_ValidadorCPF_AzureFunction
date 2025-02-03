import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()

@app.route(route="funvalidacpf", methods=["GET", "POST"])
def funvalidacpf(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    cpf = req.params.get('cpf')
    if not cpf:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            cpf = req_body.get('cpf')

    if cpf:        
        cpf = ''.join(filter(str.isdigit, cpf)) # Aqui removemos letras do CPF

        # Abaixo validações de 11 dígitos
        if len(cpf) != 11:
            return func.HttpResponse("CPF inválido. Deve conter 11 dígitos.", status_code=400)

        # Check if all digits are the same.
        if cpf == cpf[0] * 11:
            return func.HttpResponse("CPF inválido. Sequência de dígitos repetidos.", status_code=400)

        # Função auxiliar para calcular os dígitos verificadores.
        def calcular_digitos(cpf_part, factor):
            total = 0
            for digit in cpf_part:
                total += int(digit) * factor
                factor -= 1
            remainder = total % 11
            return '0' if remainder < 2 else str(11 - remainder)

        primeiro_digito = calcular_digitos(cpf[:9], 10)
        segundo_digito = calcular_digitos(cpf[:9] + primeiro_digito, 11)

        if cpf[-2:] == primeiro_digito + segundo_digito:
            return func.HttpResponse(f"O CPF {cpf} é válido.", status_code=200)
        else:
            return func.HttpResponse("CPF inválido.", status_code=400)
    else:
        return func.HttpResponse(
             "Informe o CPF via query params ou no body da requisição.",
             status_code=400
        )