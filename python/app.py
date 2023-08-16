from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Your existing code for data extraction and DataFrame creation here


@app.route('/')
def index():
    import pytrends
    from pytrends.request import TrendReq
    pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 20)) 


    Tech_rtst_IN=pytrends.realtime_trending_searches(pn='IN',cat='t')
    Bus_rtst_IN= pytrends.realtime_trending_searches(pn='US',cat='b')
    Enter_rtst_IN= pytrends.realtime_trending_searches(pn='US',cat='e')
    Health_rtst_IN = pytrends.realtime_trending_searches(pn='IN',cat='m')
    Sports_rtst_IN = pytrends.realtime_trending_searches(pn='IN',cat='s')
    All_rtst_IN = pytrends.realtime_trending_searches(pn='US',cat='all')

    Tech_entities = list(Tech_rtst_IN['entityNames'])
    Bus_entities = list(Bus_rtst_IN['entityNames'])
    Enter_entities = list(Enter_rtst_IN['entityNames'])
    Health_entities = list(Health_rtst_IN['entityNames'])
    Sports_entities = list(Sports_rtst_IN['entityNames'])
    All_entities = list(All_rtst_IN['entityNames'])

    def extract_unique(list1:list):
        distinct = set()

        for i in range(len(list1)):
            for j in range(len(list1[i])):
                distinct.add(list1[i][j])
        return distinct

    import re
    def links_returning(name:str):
        pattern=r"\s+"
        name = re.sub(pattern, "", name)


        return ('https://www.walmart.com/search?q='+name)

    Tech_distinct_entities = sorted(extract_unique(Tech_entities)) #done
    Bus_distinct_entities = sorted(extract_unique(Bus_entities)) #done
    Enter_distinct_entities = sorted(extract_unique(Enter_entities)) #done
    Health_distinct_entities = sorted(extract_unique(Health_entities)) #done
    Sports_distinct_entities = sorted(extract_unique(Sports_entities)) #done
    All_distinct_entities = sorted(extract_unique(All_entities)) #done

    import spacy

    # Load a pre-trained spaCy NER model
    nlp = spacy.load("en_core_web_sm")

    def extract_products_from_text_list(text_list):
        extracted_products = []

        for text in text_list:
            doc = nlp(text)
            for ent in doc.ents:
                if ent.label_ == "ORG" or ent.label_ == "PRODUCT":
                    extracted_products.append(ent.text)

        return extracted_products

    # Example list of text
    text_list = Tech_distinct_entities
    text_list = sorted(text_list)

    extracted_Tech_products = extract_products_from_text_list(text_list)
    print("Extracted Products:", extracted_Tech_products)

    import pandas as pd
    Tech_df = pd.DataFrame(extracted_Tech_products,columns=['Name'])

    Tech_df['Links'] = Tech_df['Name'].apply(links_returning)

    Tech_df['Product Links'] = Tech_df.apply(lambda row: f'<a href="{row["Links"]}">{row["Name"]}</a>', axis=1)

    Tech_df.drop(columns=['Name', 'Links'], inplace=True)
    Tech_df = Tech_df.head(25)

    Health_df = pd.DataFrame(Health_distinct_entities,columns=['Name'])

    Health_df['Link'] = Health_df['Name'].apply(links_returning)

    Health_df['Product Links'] = Health_df.apply(lambda row: f'<a href="{row["Link"]}">{row["Name"]}</a>', axis=1)
    Health_df.drop(columns=['Name', 'Link'], inplace=True)
    Health_df = Health_df.head(25)

    Enter_df = pd.DataFrame(Enter_distinct_entities,columns=['Name'])

    Enter_df['Link'] = Enter_df['Name'].apply(links_returning)

    Enter_df['Product Links'] = Enter_df.apply(lambda row: f'<a href="{row["Link"]}">{row["Name"]}</a>', axis=1)
    Enter_df.drop(columns=['Name', 'Link'], inplace=True)
    Enter_df = Enter_df.head(25)

    import spacy

    # Load a pre-trained spaCy NER model
    nlp = spacy.load("en_core_web_sm")

    def extract_products_from_text_list(text_list):
        extracted_products = []

        for text in text_list:
            doc = nlp(text)
            for ent in doc.ents:
                if ent.label_ == "NORP" or ent.label_ == "GPE":
                    continue
                if ent.label_ == "ORG" or ent.label_ == "PRODUCT":
                    extracted_products.append(ent.text)

        return extracted_products

    # Example list of text
    text_list = Sports_distinct_entities

    extracted_Sports_products = extract_products_from_text_list(text_list)
    print("Extracted Products:", extracted_Sports_products)

    Sports_df = pd.DataFrame(extracted_Sports_products,columns=['Name'])

    Sports_df['Link'] = Sports_df['Name'].apply(links_returning)

    Sports_df['Product Links'] = Sports_df.apply(lambda row: f'<a href="{row["Link"]}">{row["Name"]}</a>', axis=1)
    Sports_df.drop(columns=['Name', 'Link'], inplace=True)
    Sports_df=Sports_df.head(25)

    import spacy

    # Load a pre-trained spaCy NER model
    nlp = spacy.load("en_core_web_sm")
    entity_tags = ["PERSON", "NORP", "FAC", "ORG", "GPE", "LOC", "PRODUCT", "EVENT", "WORK_OF_ART", "LAW", "LANGUAGE", "DATE", "TIME", "PERCENT", "MONEY", "QUANTITY", "ORDINAL", "CARDINAL"]

    def extract_products_from_text_list(text_list):
        extracted_products = []

        for text in text_list:
            doc = nlp(text)
            for ent in doc.ents:
                if ent.label_ in entity_tags:
                    extracted_products.append(ent.text)

        return extracted_products

    # Example list of text
    text_list = All_distinct_entities

    extracted_All_products = extract_products_from_text_list(text_list)
    print("Extracted Products:", extracted_All_products)

    All_df = pd.DataFrame(extracted_All_products,columns=['Name'])

    All_df['Link'] = All_df['Name'].apply(links_returning)

    All_df['Product Links'] = All_df.apply(lambda row: f'<a href="{row["Link"]}">{row["Name"]}</a>', axis=1)
    All_df.drop(columns=['Name', 'Link'], inplace=True)
    All_df = All_df.head(25)

    import spacy

    # Load a pre-trained spaCy NER model
    nlp = spacy.load("en_core_web_sm")
    entity_tags = ["PERSON", "ORG", "GPE", "LOC", "PRODUCT", "EVENT", "WORK_OF_ART", "LAW", "LANGUAGE", "ORDINAL", "CARDINAL"]

    def extract_products_from_text_list(text_list):
        extracted_products = []

        for text in text_list:
            doc = nlp(text)
            for ent in doc.ents:
                if ent.label_ in entity_tags:
                    extracted_products.append(ent.text)

        return extracted_products

    # Example list of text
    text_list = Bus_distinct_entities

    extracted_Bus_products = extract_products_from_text_list(text_list)
    print("Extracted Products:", extracted_Bus_products)

    Bus_df = pd.DataFrame(extracted_Bus_products,columns=['Name'])

    Bus_df['Link'] = Bus_df['Name'].apply(links_returning)

    Bus_df['Product Links'] = Bus_df.apply(lambda row: f'<a href="{row["Link"]}">{row["Name"]}</a>', axis=1)
    Bus_df.drop(columns=['Name', 'Link'], inplace=True)
    Bus_df = Bus_df.head(25)




    # Pass your DataFrame (e.g., Tech_df) to the HTML template
    tech_data = Tech_df.to_html(index=False, escape=False, classes="table table-striped")
    sports_data = Sports_df.to_html(index=False, escape=False, classes="table table-striped")
    health_data = Health_df.to_html(index=False, escape=False, classes="table table-striped")
    all_data = All_df.to_html(index=False, escape=False, classes="table table-striped")

    return render_template('index.html', tech_data=tech_data, sports_data=sports_data, health_data=health_data, all_data=all_data)

if __name__ == '__main__':
    app.run(debug=True)
