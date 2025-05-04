import spacy
from spacy_merger import merge_hyphenated_tokens
from mappings import type_synonym_mapping,budget_synonym_mapping,style_synonym_mapping,suitable_for_synonyms_mapping



def detect_intent_spacy(user_input, context, nlp):
    """
    Detects user intent using spaCy for more advanced NLU.

    Args:
        user_input (str): The user's input text.

    Returns:
        tuple: (intent_str, entities_dict) - detected intent and extracted entities.
    """

    recommend_intent_keywords = ["recommend", "suggest", "find", "destination", "place", "go"]  
    type_intent_keywords = ["type", "kind", "like", "want", "city", "island", "beach", "mountain", "countryside", "coastal", "lake", "region", "site"] # Added more type keywords to cover more categories
    destination_types = [value[0] for value in type_synonym_mapping.values() if value]
    budget_intent_keywords = ["budget", "cheap", "inexpensive", "affordable", "luxury", "expensive", "costly", "budget-friendly", "mid-range", "moderate", "low", "high"] # Added budget related keywords
    for value in budget_synonym_mapping.values():
        budget_intent_keywords.extend(value)
        
    suitable_for_intent_keywords = [item for sublist in suitable_for_synonyms_mapping.values() for item in sublist]

    style_intent_keywords = ["style", "travel", "vacation", "vacation style", "travel style", "like", "want", "adventure", "relax", "cultural", "romantic", "nature", "historical", "foodie", "wellness"]
    for value in style_synonym_mapping.values():
        style_intent_keywords.extend(value)
    #travel_styles = style_synonym_mapping.keys()

    doc = nlp(user_input)
    intent = "recommend_general" # Default
    entities = {}
    detected_intents = []
    entities['style'] = set()
    entities['suitable_for'] = set()

    #Merge hyphenated words
    doc = merge_hyphenated_tokens(doc)

    # Check for TYPE intent
    if any(token.lemma_ in type_intent_keywords for token in doc):
        detected_intents.append("recommend_type")
        for dtype_standardized, dtype_synonyms in type_synonym_mapping.items(): # Iterate through synonym mapping
            for synonym in dtype_synonyms: # Check for each synonym
                if synonym.lower() in user_input.lower():
                    entities['type'] = dtype_standardized.title() # Use standardized type (Title Case)
                    break # Exit inner loop after finding a synonym
            if 'type' in entities: # Exit outer loop if type entity is found
                break

    """
    # Check for BUDGET intent
    print("\n--- DEBUGGING BUDGET INTENT ---") # Debug block start
    print(f"User Input: '{user_input}'") # Print the user input
    print(f"Budget Intent Keywords: {budget_intent_keywords}") # Print the keyword list

    budget_intent_found = False # Flag to track if budget intent keywords are found

    for token in doc:
        token_lemma = token.lemma_
        print(f"  Token: '{token.text}', Lemma: '{token_lemma}'") # Print each token and its lemma
        if token_lemma in budget_intent_keywords:
            budget_intent_found = True
            print(f"    Lemma '{token_lemma}' FOUND in budget_intent_keywords!") # Indicate a match
    
    """
    #necessary        
    if any(token.lemma_ in budget_intent_keywords for token in doc): # Use the flag instead of re-evaluating any()
        detected_intents.append("recommend_budget")
        print("Budget intent detected (based on keyword found).") # Confirmation message
        for budget_standardized, budget_synonyms in budget_synonym_mapping.items():
                for synonym in budget_synonyms:
                    if synonym.lower() in user_input.lower():
                        entities['budget'] = budget_standardized.capitalize()
                        break
                if 'budget' in entities:
                    break
    else:
        print("No budget intent keywords found in input.") # Indicate no keywords found

    """
    print(f"  any(token.lemma_ in budget_intent_keywords for token in doc) evaluated to: {budget_intent_found}") # Print the final result of the condition
    print("--- DEBUGGING BUDGET INTENT END ---\n") # Debug block end
    """


     # Check for STYLE intent (MODIFIED for synonym handling)
    if any(token.lemma_ in style_intent_keywords for token in doc):
        detected_intents.append("recommend_style")
        print("style intent detected")
        for style_standardized, style_synonyms in style_synonym_mapping.items(): # Iterate through style synonym mapping
            for synonym in style_synonyms: # Check for each synonym
                if synonym.lower() in user_input.lower():
                    entities['style'].add(style_standardized.capitalize()) # Use standardized style (Title Case)
                    break # Exit inner loop after finding a synonym



    if any(token.lemma_ in suitable_for_intent_keywords for token in doc):
        detected_intents.append("recommend_suitable_for")
        print("suitable_for intent detected")
        for suitable_for_standardized, suitable_for_synonyms in suitable_for_synonyms_mapping.items(): # Iterate through style synonym mapping
            for synonym in suitable_for_synonyms: # Check for each synonym
                if synonym.lower() in user_input.lower():
                    entities['suitable_for'].add(suitable_for_standardized.capitalize()) # Use standardized style (Title Case)
                    break # Exit inner loop after finding a synonym
            
    
    if 'type' in entities:
        context['type'] = entities["type"]
    if 'budget' in entities:
        context['budget'] = entities['budget']
    if entities['suitable_for']:
        for item in entities["suitable_for"]:
            if item not in context["suitable_for"]:
                context['suitable_for'].append(item)
        #context['suitable_for'].update(entities["suitable_for"])
    if entities['style']:
        for item in entities["style"]:
            if item not in context["style"]:
                context['style'].append(item)
        #context['style'].update(entities["style"])
    if detected_intents:
        for item in detected_intents:
            if item not in context["intents"]:
                context['intents'].append(item)
        #context['intents'].update(detected_intents)
    

    print(f" Intents: {detected_intents}")
    return detected_intents, context

            

