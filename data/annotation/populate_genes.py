import sqlite3
import pandas as pd

con = sqlite3.connect('../db/projects_info.sqlite3')
cur = con.cursor()

for version in ['75', '84', '104']:
    cur.execute("DROP TABLE myvcf_browser_gene{}".format(version))
    cur.execute("CREATE TABLE myvcf_browser_gene{} (Ensgene_ID text, Gene_name text, Description text)".format(version))

    data = pd.read_csv('ENSEMBL_Gene_v{}.txt'.format(version), sep='\t', header=0)
    for index,row in data.iterrows():
        query = 'INSERT INTO myvcf_browser_gene{} VALUES ("{}", "{}", "{}")'.format(version,
                                                                                    row['#Ensembl Gene ID'],
                                                                                    row['Associated Gene Name'],
                                                                                    row['Description'])
        cur.execute(query)

con.commit()
con.close()
