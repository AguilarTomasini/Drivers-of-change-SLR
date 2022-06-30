# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 23:20:09 2022

@author: mtomasin
"""

import pandas as pd
from datetime import datetime

change_categories = [
    '"Deforestation"',
    '"Degradation"',
    '"Regeneration"',
    '"Rehabilitation"',
    '"Restoration"',
    '"Exclosures"'
]

drivers_of_change = [
    '"Drivers of change"',
    #'impacts',
    #'factors',
    '"climate change"',
    #'mitigation',
    #'adaptation',
    #'management',
    'resilience',
    'anthropogenic',
    #'use',
    '"ecosystem services"',
    '"governance"',
    'sustainable|sustainability',
    'fires',
    '"SOCIO-ECONOMIC drivers"',
    #'"NATURAL drivers"',
    '"Poverty reduction"',
    'Conservation',
    '"Land use"'
]

dry_forest = [ 
    '"Dry forest"',
    '"Miombo woodlands"',
    #'"Sudanian woodlands"',
    '"Dry afromontane forest"',
    '"Combretum-Terminalia"',
   # '"Acacia-Commiphora"',
    '"Acacia woodlands"',
    '"dry miombo"',
    '"Mopane woodlands"'
    ]
    
names_country = [
    '"East Africa"',
    'Ethiopia',
    '"South Sudan"', 
    'Kenya',
    'Tanzania',
    'Uganda',
    'Zambia',
    'Malawi',
    'Mozambique',
    'Zimbabwe',
    'Djibouti',
    'Somalia'
    ]
    



list_of_search_combinations = []

# Generate combinations with change categories
while len(change_categories)>0:
    word_1 = change_categories.pop()
    for word_3 in names_country:
        if word_1 == 'Exclosures' and word_3 not in ['Kenya','Tanzania', 'Uganda','Zambia', 'Malawi','Mozambique','Zimbabwe' ]:
                list_of_search_combinations.append(word_1+'+'+word_3)
        for word_2 in dry_forest:  
            if word_2 == '"Mopane woodlands"' and word_3 in ["Ethiopia", "South Sudan", "Djibouti", "Somalia", "Uganda", "Kenya"]:
                pass
            elif word_2 == '"Sudanian woodlands"' and word_3 != "South Sudan":
                pass
            elif word_2 == '"Acacia woodlands"' and word_3 not in ["Ethiopia", "South Sudan", "Somalia", "Uganda", "Kenya", "Tanzania"]:
                pass
            elif word_2 == '"Acacia-Commiphora"' and word_3 not in ["Ethiopia", "South Sudan", "Somalia", "Uganda", "Kenya", "Tanzania"]:
                pass
            elif word_2 == '"Dry afromontane forest"' and word_3 not in ["Ethiopia", "Kenya", "Tanzania", "Zambia"]:
                pass
            elif word_2 == '"Combretum-Terminalia"' and word_3 not in ["Ethiopia", "South Sudan", "Uganda", "Kenya", "Tanzania"]:
                pass
            elif word_2 == '"dry miombo"' and word_3 not in ["Kenya", "Tanzania", "Malawi", "Zambia", "Zimbabwe", "Mozambique"]:
                pass
            elif word_2 == '"Mopane woodlands"' and word_3 not in ["Tanzania", "Malawi", "Zambia", "Zimbabwe", "Mozambique"]:
                pass
            else:
                if word_1 != 'Exclosures':
                    list_of_search_combinations.append(word_1+'+'+word_2+'+'+word_3)
                else:
                    pass

# Generate combinations with drivers of change 
while len(drivers_of_change)>0:
    word_1 = drivers_of_change.pop()
    for word_2 in dry_forest:
        for word_3 in names_country:
            if word_2 == '"Mopane woodlands"' and word_3 in ["Ethiopia", "South Sudan", "Djibouti", "Somalia", "Uganda", "Kenya"]:
                pass
            elif word_2 == '"Sudanian woodlands"' and word_3 != "South Sudan":
                pass
            elif word_2 == '"Acacia woodlands"' and word_3 not in ["Ethiopia", "South Sudan", "Somalia", "Uganda", "Kenya", "Tanzania"]:
                pass
            elif word_2 == '"Acacia-Commiphora"' and word_3 not in ["Ethiopia", "South Sudan", "Somalia", "Uganda", "Kenya", "Tanzania"]:
                pass
            elif word_2 == '"Dry afromontane forest"' and word_3 not in ["Ethiopia", "Kenya", "Tanzania", "Zambia"]:
                pass
            elif word_2 == '"Combretum-Terminalia"' and word_3 not in ["Ethiopia", "South Sudan", "Uganda", "Kenya", "Tanzania"]:
                pass
            elif word_2 == '"dry miombo"' and word_3 not in ["Kenya", "Tanzania", "Malawi", "Zambia", "Zimbabwe", "Mozambique"]:
                pass
            elif word_2 == '"Mopane woodlands"' and word_3 not in ["Tanzania", "Malawi", "Zambia", "Zimbabwe", "Mozambique"]:
                pass
            else:
                list_of_search_combinations.append(word_1+'+'+word_2+'+'+word_3)

date = datetime.strftime(datetime.now(), '%d%m%Y_%H%M%S')

df_sc = pd.Series(list_of_search_combinations)
df_sc.name = 'search word combinations'
df_sc.to_csv(f'output/{date}_drivers_dry_forest_reserachpapers.csv', sep=',', index=False, header=True)
    