import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()

@app.route(route = 'fnvalidacaocpf', methods=['GET', 'POST'], auth_level=func.AuthLevel.ANONYMOUS)
def fnvalidacaocpf(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Validando o CPF informado.')

    cpf = req.params.get('cpf')
    if not cpf:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('cpf')

    if cpf:
        cpf = ''.join(filter(str.isdigit, cpf)) # Aqui são removidas letras do CPF.

        # Aqui paramos o processo se não for informado o CPF.
        if cpf == '':
            return func.HttpResponse('Favor, informe o número de CPF.', status_code = 400)

        # Aqui valida se tem 11 dígitos.
        if len(cpf) != 11:
            return func.HttpResponse('CPF inválido, pois deve conter 11 dígitos.', status_code = 400)

        # Aqui é validado que os dígitos não são todos iguais.
        if cpf == cpf[0] * 11:
            return func.HttpResponse('CPF inválido. Os dígitos estão repetidos.', status_code = 400)

        # Função para calcular os dígitos verificadores.
        def calcular_digitos(cpf_prefixo, verificador):
            total = 0
            for digito in cpf_prefixo:
                total += int(digito) * verificador
                verificador -= 1
            restante = total % 11
            return '0' if restante < 2 else str(11 - restante)

        primeiro_digito = calcular_digitos(cpf[:9], 10)
        segundo_digito = calcular_digitos(cpf[:9] + primeiro_digito, 11)

        if cpf[-2:] == primeiro_digito + segundo_digito:
            return func.HttpResponse(f"O CPF {cpf} é válido!", status_code=200)
        else:
            return func.HttpResponse("Opa, este é um CPF inválido!", status_code=400)
    else:
        return func.HttpResponse(
             "Informe o CPF via query params ou no body da requisição.",
             status_code=400
        )