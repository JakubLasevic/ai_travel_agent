import pandas as pd
import spacy
import os
import numpy as np 
import traceback 

from data_processing import recommend_destination
from intent_detection import detect_intent_spacy
from mappings import type_mapping, budget_mapping

class Chatbot:
    def __init__(self, locations_path="destinations.csv", pois_path="points_of_interest.csv"):
        """
        Initializes the Chatbot by loading NLP model (optional) and destination data.
        Args:
            locations_path (str): Path to the destinations CSV file.
            pois_path (str): Path to the points_of_interest CSV file.
        """
        print("Initializing Chatbot...")
        self.nlp = None 
        try:
            self.nlp = spacy.load("en_core_web_lg")
            print("spaCy model 'en_core_web_lg' loaded.")
        except OSError:
            print("WARNING: spaCy model 'en_core_web_lg' not found. NLP features disabled.")
            print("To enable NLP, run: python -m spacy download en_core_web_lg")

        self.df = pd.DataFrame() 
        self.load_data(locations_path, pois_path) 

    def load_data(self, locations_csv_path, pois_csv_path):
        """
        Loads and preprocesses location and POI data. Stores the combined DataFrame in self.df.
        Expects a 'Description' column in the locations CSV.
        Optionally reads 'POIDescription' from the POIs CSV.
        """
        try:
            # --- File Existence Checks ---
            locations_exist = os.path.exists(locations_csv_path)
            pois_exist = os.path.exists(pois_csv_path)

            if not locations_exist:
                print(f"--- CRITICAL ERROR: Locations file not found at '{locations_csv_path}'. Cannot load data. ---")
                self.df = pd.DataFrame()
                return

            # --- Load Locations ---
            locations_df = pd.read_csv(locations_csv_path)
            print(f"Loading locations: {len(locations_df)} rows from {locations_csv_path}")

            # --- Check Required Location Columns (Including Description) ---
            required_loc_cols = ['LocationID', 'LocationName', 'Type', 'Budget', 'Travel Style', 'Country', 'Best Time to Visit', 'Latitude', 'Longitude', 'Description']
            missing_loc_cols = [col for col in required_loc_cols if col not in locations_df.columns]
            if missing_loc_cols:
                 print(f"--- CRITICAL ERROR: Missing required columns in locations CSV: {missing_loc_cols}. Cannot load data. ---")
                 self.df = pd.DataFrame()
                 return

            # --- Preprocess Locations ---
            if 'Type' in locations_df.columns:
                 locations_df['Type'] = locations_df['Type'].replace(type_mapping, regex=False)
            if 'Budget' in locations_df.columns:
                 locations_df['Budget'] = locations_df['Budget'].replace(budget_mapping, regex=False)
            locations_df['Description'] = locations_df['Description'].fillna("No description available for this location.")
            locations_df['Description'] = locations_df['Description'].astype(str) # Ensure string type

            # --- Handle POIs ---
            if not pois_exist:
                print(f"--- WARNING: POIs file not found at '{pois_csv_path}'. Adding empty POI list to locations. ---")
                locations_df['points_of_interest'] = [[] for _ in range(len(locations_df))]
                self.df = locations_df 
            else:
                # --- Load and Process POIs ---
                pois_df = pd.read_csv(pois_csv_path)
                print(f"Loading POIs: {len(pois_df)} rows from {pois_csv_path}")

                # --- Check Required POI Columns ---
                required_poi_cols = ['ParentLocationID', 'POIName', 'POIType', 'POILat', 'POILng']
                optional_poi_cols = ['POIDescription']
                base_poi_cols = required_poi_cols 
                cols_to_load = base_poi_cols[:] 
                has_poi_desc = False
                if 'POIDescription' in pois_df.columns:
                    cols_to_load.append('POIDescription')
                    has_poi_desc = True
                    print("Found optional 'POIDescription' column in POIs CSV.")
                else:
                    print("Optional 'POIDescription' column not found in POIs CSV. Descriptions will be empty.")


                missing_poi_cols = [col for col in base_poi_cols if col not in pois_df.columns]
                if missing_poi_cols:
                    print(f"--- WARNING: Missing required columns in POIs CSV: {missing_poi_cols}. POIs may not load correctly. ---")
                    locations_df['points_of_interest'] = [[] for _ in range(len(locations_df))]
                    self.df = locations_df 
                else:
                    # --- Prepare POIs ---
                    pois_subset_df = pois_df[['ParentLocationID'] + [col for col in cols_to_load if col != 'ParentLocationID']].copy()

                    # Rename columns for consistency
                    poi_rename_map = {'POIName': 'name', 'POIType': 'type', 'POILat': 'lat', 'POILng': 'lng'}
                    if has_poi_desc:
                        poi_rename_map['POIDescription'] = 'description'
                    pois_subset_df = pois_subset_df.rename(columns=poi_rename_map)

                    # Fill NaN/missing POI descriptions if column exists
                    if has_poi_desc:
                        pois_subset_df['description'] = pois_subset_df['description'].fillna("") # Use empty string for missing POI desc
                        pois_subset_df['description'] = pois_subset_df['description'].astype(str)

                    # Define columns to include in the final POI dict
                    final_poi_dict_cols = ['name', 'type', 'lat', 'lng']
                    if has_poi_desc:
                        final_poi_dict_cols.append('description')

                    # Group POIs and aggregate into lists of dicts
                    grouped_pois = pois_subset_df.groupby('ParentLocationID')
                    poi_lists = grouped_pois.apply(
                        lambda group: group[final_poi_dict_cols].to_dict('records')
                    ).rename('points_of_interest') 

                    # Merge POIs with locations
                    combined_df = pd.merge(
                        locations_df,
                        poi_lists,
                        left_on='LocationID',
                        right_index=True,
                        how='left'
                    )
                    # Fill missing POI lists with empty lists
                    combined_df['points_of_interest'] = combined_df['points_of_interest'].apply(lambda x: x if isinstance(x, list) else [])
                    self.df = combined_df # Assign the final merged DataFrame

            print(f"Data loading complete. DataFrame shape: {self.df.shape}")
            if not self.df.empty:
                 print("\nSample of loaded data (first 2 rows):")
                 print(self.df.head(2).to_string()) 
            else:
                 print("DataFrame is empty after loading attempt.")


        except FileNotFoundError as e:
            print(f"--- FILE ERROR during data loading: {e} ---")
            self.df = pd.DataFrame()
        except Exception as e:
            print(f"--- UNEXPECTED ERROR during data loading: {e} ---")
            traceback.print_exc()
            self.df = pd.DataFrame()

    def get_location_data_by_name(self, name):
        """
        Retrieves the data row for a specific location by its name. Case-insensitive.

        Args:
            name (str): The name of the location.

        Returns:
            pd.Series or None: The data series for the location, or None if not found.
        """
        if self.df.empty:
            print("DataFrame is empty, cannot search for location.")
            return None
        if not name or not isinstance(name, str):
             print("Invalid location name provided for search.")
             return None
        try:
            location_data = self.df.loc[self.df['LocationName'].str.lower() == name.lower()]
            if not location_data.empty:
                return location_data.iloc[0]
            else:
                print(f"Location '{name}' not found in DataFrame.")
                return None
        except Exception as e:
            print(f"Error searching for location '{name}': {e}")
            traceback.print_exc()
            return None

    def get_description(self, location_data):
        """
        Retrieves the description for a location from its data Series.

        Args:
            location_data (pd.Series): The data for the location.

        Returns:
            str: The description string, or a default message if not found/valid.
        """
        default_desc = "Sorry, I couldn't find a description for this location."
        if location_data is None or not isinstance(location_data, pd.Series):
            return default_desc

        # Use .get with a default value, robust against missing column
        description = location_data.get('Description', default_desc)

        # Check for actual NaN values using pandas function, or empty/whitespace strings
        if pd.isna(description) or not isinstance(description, str) or not description.strip():
            # Fallback if description is missing/invalid in the data
            name = location_data.get('LocationName', 'This location')
            country = location_data.get('Country', '')
            loc_type = location_data.get('Type', '')
            return f"Information for {name}{f' in {country}' if country else ''}{f' ({loc_type})' if loc_type else ''} is available, but a detailed description is missing."
        else:
            # Return the description directly from the CSV
            return description.strip() 


    # --- process_message handles general chat, intent detection, recommendations ---
    def process_message(self, user_input, context):
        """
        Processes a general user message, updates context using NLU, gets recommendations,
        and generates appropriate chatbot responses.

        Args:
            user_input (str): The message text from the user.
            context (dict): The current conversation context for the user (from Flask session).

        Returns:
            tuple: (response_text, locations_list)
                   - response_text: A string containing the chatbot's reply.
                   - locations_list: A list of location dicts for buttons, or empty list.
        """
        # Ensure spaCy model is loaded before using it
        if self.nlp is None:
             print("ERROR: spaCy model not loaded, cannot process message using NLP.")
             # Provide a fallback response or handle differently
             return "Sorry, I'm having trouble understanding language right now. Can you be more specific?", []

        response_lines = [] 
        user_input_processed = user_input.strip().lower() 

        if not user_input_processed:
            response_lines.append("Hmm, I didn't quite catch that. Can you rephrase?")
            return "\n".join(response_lines), []

        try:
            detect_intent_spacy(user_input_processed, context, self.nlp)
            print(f"Context after intent detection: {context}") # Log context changes

            if self.df.empty:
                print("ERROR: DataFrame is empty, cannot provide recommendations.")
                return "Sorry, I don't have any destination data available right now.", []

            # Assuming recommend_destination returns a list of dicts or an error string/None
            recommendations = recommend_destination(context, self.df)

            locations_for_buttons = [] # Data for frontend buttons

            if isinstance(recommendations, list):
                if not recommendations:
                    # No destinations match the criteria
                     response_lines.append('No destination from my list matches your preferences.')
                     if context.get('type') and context.get('budget') and context.get('style'):
                         response_lines.append("Maybe try adjusting the type, budget, or style?")
                     else:
                          response_lines.append("Could you tell me more about the type, budget, or style you're looking for?")

                elif len(recommendations) > 3: # Threshold for asking clarifying questions
                    # Ask clarifying questions if criteria seem missing
                    if not context.get('type'):
                        response_lines.append('What type of destination are you looking for? (e.g., city, beach, mountain, island)')
                    elif not context.get('budget'):
                        response_lines.append('What is your ideal budget? (e.g., affordable, mid-range, luxury)')
                    elif not context.get('style'): # Check if style list/set is empty
                         response_lines.append('What style of destination are you looking for? (e.g., relaxing, adventurous, historical)')
                    else:
                        # Criteria seem set, but still many results - offer top ones
                        response_lines.append(f"Found quite a few options! Here are some top suggestions for a {context.get('budget','any budget').lower()} {context.get('type','any type').lower()} trip matching your style:")
                        display_limit = 5 # Show top 5
                        for i, recommendation in enumerate(recommendations[:display_limit]):
                            # Add data for buttons
                            locations_for_buttons.append({
                                'name': recommendation.get('name'),
                                'lat': recommendation.get('latitude'),
                                'lng': recommendation.get('longitude'),
                                'id': recommendation.get('id') # Pass ID if available
                            })
                        if len(recommendations) > display_limit:
                             response_lines.append(f"(Showing {display_limit} of {len(recommendations)} matches)")

                else: # 1-3 recommendations
                    response_lines.append(f"Based on your preferences, here are a few ideas:")
                    for i, recommendation in enumerate(recommendations):
                         desc_line = f"- {recommendation.get('name', 'Unknown')} in {recommendation.get('country', '?')}"
                         details = []
                         if recommendation.get('type'): details.append(recommendation.get('type'))
                         if recommendation.get('budget'): details.append(recommendation.get('budget'))
                         if details: desc_line += f" ({', '.join(details)})"
                         if recommendation.get('best_time_to_visit'): desc_line += f". Best time to visit: {recommendation.get('best_time_to_visit')}."
                         response_lines.append(desc_line)
                         locations_for_buttons.append({
                            'name': recommendation.get('name'),
                            'lat': recommendation.get('latitude'),
                            'lng': recommendation.get('longitude'),
                            'id': recommendation.get('id')
                         })
            else:
                # Handle cases where recommend_destination might return a non-list (e.g., error message)
                 response_lines.append(str(recommendations))

            # Join response lines into a single string
            final_response_text = "\n".join(response_lines)
            return final_response_text, locations_for_buttons

        except Exception as e:
             print(f"--- ERROR in process_message: {e} ---")
             traceback.print_exc()
             # Return a generic error message and empty locations
             return "Sorry, something went wrong while processing your request.", []

