import textract
import glob
from parser import parse_other_exchange, parse_direct_trade, parse_sparplan
from merger import merge_summaries
import tqdm

files = glob.glob("post/*.pdf")

dataframes = []

for file in tqdm.tqdm(files):
    t = textract.process(file)
    text = t.decode("utf-8")

    if "Wertpapierabrechnung" not in text:
        continue

    if "Sparplan" in text or "Zwischensumme" in text:
        new_df = parse_sparplan(text)
    elif "Handelsplatzgeb" in text:
        new_df = parse_other_exchange(text)
    else:
        new_df = parse_direct_trade(text)

    dataframes.append(new_df)

summary = merge_summaries(dataframes)
summary.to_csv("summary.tsv", sep="\t", index=False)

