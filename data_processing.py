import pandas as pd
from mappings import type_mapping, budget_mapping, style_synonym_mapping, suitable_for_synonyms_mapping





def recommend_destination(context, destination_data):
    """
    Recommends destinations based on intent and entities, handling list of budgets from mapping.
    """
    recommendations = []
    filtered_destinations = destination_data

    if "recommend_type" in context['intents']:
        if 'type' in context:
            destination_type = context['type']
            temp = filtered_destinations['Type']
            filtered_destinations = filtered_destinations[filtered_destinations['Type'].str.lower() == destination_type.lower()]
        else:
            return "Could you please specify what type of destination you are looking for (e.g., city, beach)?"

    if "recommend_budget" in context['intents']:
        if 'budget' in context:
            budget_level = context['budget']
            filtered_destinations = filtered_destinations[
                filtered_destinations['Budget'].apply(lambda x: x == context['budget'])
            ]
        else:
            return "Could you please specify your budget level (e.g., budget-friendly, mid-range, luxury)?"
        
    if "recommend_suitable_for" in context['intents']:
        if context['suitable_for']:
            suitable_for = context['suitable_for']
            temp_destinations = pd.DataFrame(columns=['LocationID','LocationName','Country','Language','Type','Budget','Best Time to Visit','Travel Style','Suitable For','Keywords/Main Attractions'])
            for suitable_for_detail in suitable_for:
                    for exact_suitable_for in suitable_for_synonyms_mapping[suitable_for_detail.lower()]:
                        temp_destinations += filtered_destinations[
                            filtered_destinations['Suitable For'].str.lower().str.contains(exact_suitable_for.lower(), na=False)
                        ]
            if temp_destinations.empty:
                for suitable_for_detail in suitable_for:
                    filtered_destinations = filtered_destinations[
                        filtered_destinations['Suitable For'].str.lower().str.contains(suitable_for_detail.lower(), na=False)
                    ]
                
        else:
            return "Could you please specify what travel style you are looking for (e.g., adventure, relaxing)?"


    if "recommend_style" in context['intents']:
        if context['style']:
            travel_style = context['style']
            temp_destinations = pd.DataFrame(columns=['LocationID','LocationName','Country','Language','Type','Budget','Best Time to Visit','Travel Style','Suitable For','Keywords/Main Attractions'])
            for style in travel_style:
                    for exact_style in style_synonym_mapping[style.lower()]:
                        temp_destinations += filtered_destinations[
                            filtered_destinations['Travel Style'].str.lower().str.contains(exact_style.lower(), na=False)
                        ]
            if temp_destinations.empty:
                for style in travel_style:
                    filtered_destinations = filtered_destinations[
                        filtered_destinations['Travel Style'].str.lower().str.contains(style.lower(), na=False)
                    ]
                
        else:
            return "Could you please specify what travel style you are looking for (e.g., adventure, relaxing)?"


    if context['intents'] == "recommend_general":
        if not destination_data.empty:
            recommended_sample = filtered_destinations.sample(min(3, len(filtered_destinations)))
            for index, row in recommended_sample.iterrows():
                recommendations.append(f"- {row['LocationName']}, {row['Country']} ({row['Type']}, Budget: {row['Budget']})")
            if recommendations:
                return "Here are some general recommendations:\n" + "\n".join(recommendations)
            else:
                return "Sorry, no general recommendations at the moment."
        else:
            return "Sorry, I don't have any destination data to make recommendations."

    if not filtered_destinations.empty:
        recommended_sample = filtered_destinations.sample(min(4, len(filtered_destinations)))
        for index, row in recommended_sample.iterrows():
            recommendations.append({'id':row['LocationID'],'name' :row['LocationName'], 'country': row['Country'], "type": row['Type'], 'budget': row['Budget'], 'best_time_to_visit': row['Best Time to Visit'], 'style':row['Travel Style'],'latitude':row['Latitude'], 'longitude':row['Longitude']})
        if recommendations:
            return recommendations
        
    return recommendations