import re
import pandas as pd


def __clean_up(text: str) -> str:
    r = re.compile("Depotinhaber.*1 von [1-3]", re.DOTALL)
    text = re.sub(r, "", text)
    r = re.compile("ING-.*10247 Berlin", re.DOTALL)
    text = re.sub(r, "", text)

    return text


def parse_other_exchange(text: str) -> pd.DataFrame:
    text = __clean_up(text)

    columns = []
    end_of_tables_options = ["Provision",  "Handelsentgelt", "Transaktionsentgelt"]
    while len(columns) == 0:
        try:
            r = re.compile(f"Wertpapierabrechnung.*{end_of_tables_options.pop()}", re.DOTALL)
            columns = re.findall(r, text)[0].replace("\n\n", "\n").split("\n") + ["Endbetrag"]
        except:
            if len(end_of_tables_options) == 0:
                raise Exception("Unrecognized document format")

    text = re.sub(r, "", text)
    text = text.strip()

    r = re.compile(".*EUR\nEUR\n\n", re.DOTALL)
    values_1 = re.findall(r, text)[0].replace("\n\n", "\n").strip().split("\n")
    values_1 += ["EUR"]

    while len(values_1) > len(columns):
        values_1[3] = f"{values_1[3]} {values_1[4]}"
        del values_1[4]

    text = re.sub(r, "", text)
    r = re.compile(".*Abrechnungs", re.DOTALL)
    values_2 = re.findall(r, text)[0].replace("\n\n", "\n").split("\n")[:-1]
    to_remove = []
    for index, value in enumerate(values_2):
        if "," not in value:
            to_remove.append(value)

    [values_2.remove(value) for value in to_remove]

    values_2 = values_2[0:2] + ["", ""] + values_2[2:]
    values_1[4:] = [f"{i} {j}" for i, j in zip(values_1[4:], values_2)]
    values = values_1

    values = list(map(lambda x: x.strip(), values))

    return pd.DataFrame([values], columns=columns)


def parse_direct_trade(text: str) -> pd.DataFrame:
    text = __clean_up(text)
    r = re.compile("Wertpapierabrechnung.*Wertpapierbezeichnung", re.DOTALL)
    columns = re.findall(r, text)[0].replace("\n\n", "\n").split("\n")
    text = re.sub(r, "", text)

    r = re.compile("Nominale.*Provision", re.DOTALL)
    columns = columns + re.findall(r, text)[0].replace("\n\n", "\n").split("\n") + ["Endbetrag"]
    text = re.sub(r, "", text)

    r = re.compile(".*EUR\nEUR\n\n", re.DOTALL)
    values_1 = re.findall(r, text)[0].replace("\n\n", "\n").strip().split("\n")
    values_1 += ["EUR"]

    while len(values_1) > len(columns):
        values_1[3] = f"{values_1[3]} {values_1[4]}"
        del values_1[4]

    text = re.sub(r, "", text)
    r = re.compile(".*Abrechnungs", re.DOTALL)
    values_2 = re.findall(r, text)[0].replace("\n\n", "\n").split("\n")[:-1]
    to_remove = []
    for index, value in enumerate(values_2):
        if "," not in value:
            to_remove.append(value)

    [values_2.remove(value) for value in to_remove]

    values_2 = values_2[0:2] + ["", ""] + values_2[2:]
    values_1[4:] = [f"{i} {j}" for i, j in zip(values_1[4:], values_2)]
    values = values_1

    values = list(map(lambda x: x.strip(), values))

    return pd.DataFrame([values], columns=columns)


def parse_sparplan(text: str) -> pd.DataFrame:
    text = __clean_up(text)
    r = re.compile("Wertpapierabrechnung.*Wertpapierbezeichnung", re.DOTALL)
    columns = re.findall(r, text)[0].replace("\n\n", "\n").split("\n")
    text = re.sub(r, "", text)

    r = re.compile("Nominale.*Provision", re.DOTALL)
    columns = columns + re.findall(r, text)[0].replace("\n\n", "\n").split("\n") + ["Endbetrag"]
    text = re.sub(r, "", text)

    r = re.compile("Stück.*EUR\nEUR\n\n", re.DOTALL)
    values_1 = re.findall(r, text)[0].replace("\n\n", "\n").strip().split("\n") + ["EUR"]
    text = re.sub(r, "", text)

    r = re.compile("\n[1-9]*.*Endbetrag", re.DOTALL)
    values_2 = re.findall(r, text)[0].replace("\n\n", "\n").strip().split("\n")[:-1]
    values_2 = values_2[:-3] + ["", ""] + values_2[-3:]

    while len(values_2) > 11:
        values_2[3] = f"{values_2[3]} {values_2[4]}"
        del values_2[4]

    values_2[4:] = [f"{i} {j}" for i, j in zip(values_1, values_2[4:])]
    values = values_2

    values = list(map(lambda x: x.strip(), values))

    return pd.DataFrame([values], columns=columns)