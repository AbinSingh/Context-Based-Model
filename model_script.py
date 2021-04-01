
import spacy
import en_core_web_sm
import pandas as pd
import re


def model_builder(text):
    import spacy
    import en_core_web_sm
    import pandas as pd
    import re
    text=text
    nlp = en_core_web_sm.load()
    doc=nlp(text)

    ## Extract entities and Labels ##

    entity=[]
    labels=[]
    for ent in doc.ents:
        entity.append(ent.text)
        labels.append(ent.label_)
    
    data=pd.DataFrame({'Entities':entity,'Labels':labels})

    MONEY=data.loc[data['Labels']=='MONEY','Entities']
    DATE=data.loc[data['Labels']=='DATE','Entities']
    PERCENT=data.loc[data['Labels']=='PERCENT','Entities']
    CARDINAL=data.loc[data['Labels']=='CARDINAL','Entities']
    LOC=data.loc[data['Labels']=='LOC','Entities']
    GPE=data.loc[data['Labels']=='GPE','Entities']

    my_date=[]

    for i in DATE.values:
        if '-' in i:
            split_values=i.split('-')
            #print(split_values)
            for x in split_values:
                my_date.append(x)
            DATE=my_date
        else:
            DATE=DATE
        
    def date_from_cardinal(CARDINAL):
        year=[]
        for i in CARDINAL:
            year_split=i.split('.')[0]
            year.append(year_split)
        return year
    
    if 'CARDINAL' in data['Labels'].values:
        date_01=list(DATE)
        date_02=date_from_cardinal(CARDINAL.values)
        YEAR_LIST=date_01+date_02
    else:
        YEAR_LIST=list(DATE)

    pattern=r'[0-9]+'

    total_year_list=[]
    for i in YEAR_LIST:
        sub_val=re.findall(pattern,i)
        for j in sub_val:
            total_year_list.append(j)

    if 'LOC' in data['Labels'].values:
        Location=list(GPE.unique())+list(LOC)
    else:
        Location=list(GPE.unique())
    
    if len(MONEY)>1:
        projected_value=max(MONEY)
    else:
        projected_value=[]
    
    if len(total_year_list)>1:
        forecast_year=max(total_year_list)
    else:
        forecast_year=[]
    
    if len(MONEY)>0:
        Market_value=min(MONEY)
    else:
        Market_value=[]
    
    if len(total_year_list)>0:
        Current_year=min(total_year_list)
    else:
        Current_year=[]
    
    if len(PERCENT)>0:
        CAGR=min(PERCENT)
    else:
        CAGR=[]
    
    text_lower=text.lower()
    if 'global' in text_lower:
        global_loc='global'
        
        if Location == None:
            Location=global_loc
        else:
            Location.append(global_loc)
        
    if 'cagr' in Location:
        Location.remove('cagr')
    
    my_dict={'CAGR':CAGR,'Projected_market_value':projected_value,'Market_value':Market_value,'Current_year':Current_year,'Forcasted_year':forecast_year,'Location':Location}
    return my_dict