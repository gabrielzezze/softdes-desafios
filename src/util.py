def lambda_handler(event, context):
    try:
        import json
        import numbers

        def not_equals(first, second):
            if isinstance(first, numbers.Number) and isinstance(second, numbers.Number):
                return abs(first - second) > 1e-3
            return first != second

        # TODO implement
        ndes = int(event["ndes"])
        code = event["code"]
        args = event["args"]
        resp = event["resp"]
        diag = event["diag"]
        exec(code, locals())

        test = []
        for index, arg in enumerate(args):
            if not "desafio{0}".format(ndes) in locals():
                return "Nome da função inválido. Usar 'def desafio{0}(...)'".format(
                    ndes
                )

            if not_equals(eval("desafio{0}(*arg)".format(ndes)), resp[index]):
                test.append(diag[index])

        return " ".join(test)
    except:
        return "Função inválida."


def converteData(orig):
    return (
        orig[8:10]
        + "/"
        + orig[5:7]
        + "/"
        + orig[0:4]
        + " "
        + orig[11:13]
        + ":"
        + orig[14:16]
        + ":"
        + orig[17:]
    )
