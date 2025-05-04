type_mapping = {
    'specific_site': 'Specific Site',  
    'city': 'City',
    'region': 'Region', 
    'mountain_region': 'Mountain Region', 
    'coastal_region': 'Coastal Region', 
    'island_group': 'Island', 
    'island': 'Island',      
    'lake_region': 'Lake Region', 
}

budget_mapping = {
    'Mid-range': 'Moderate',       
    'Luxury': 'Luxury',
    'Budget-friendly': 'Budget-friendly',
    'Mid-range to Luxury': 'Moderate',  # Map to BOTH 'Moderate' and 'Luxury'
    'Budget-friendly to Mid-range': 'Budget-friendly', # Map to BOTH 'Budget-friendly' and 'Moderate'
    'Budget-friendly to Luxury': 'Budget-friendly', # Map to BOTH 'Budget-friendly' and 'Luxury'
}



#synonyms matching
type_synonym_mapping = {
    'city': ['city', 'urban', 'metropolis', 'cities'], # Synonyms for 'city'
    'island': ['island', 'islands', 'isle', 'cay'], # Synonyms for 'island'
    'mountain region': ['mountain region', 'mountain', 'alpine', 'mountainous'], # Synonyms for 'mountain region'
    'coastal region': ['coastal region', 'coast', 'beach', 'beaches', 'seaside', 'shore', 'coastline'], # Synonyms for 'coastal region'
    'lake region': ['lake region', 'lake', 'lakeside','lakefront'], # Synonyms for 'lake region'
    'region': ['region', 'area', 'district', 'territory', 'province'], # Synonyms for 'region'
    'specific site': ['specific site', 'landmark', 'attraction', 'place of interest', 'sight'] # Synonyms for 'specific site'
}

budget_synonym_mapping = {
    'budget-friendly': ['budget-friendly', 'cheap', 'affordable', 'inexpensive', 'low-cost', 'economical', 'thrifty', 'saving'], # Synonyms for 'budget-friendly'
    'moderate': ['moderate', 'mid-range', 'average-priced', 'mid-level', 'reasonable'], # Synonyms for 'moderate'
    'luxury': ['luxury', 'expensive', 'high-end', 'upscale', 'premium', 'costly', 'lavish', 'opulent','high-end'] # Synonyms for 'luxury'
}

style_synonym_mapping = {
    'romantic': ['romantic', 'couples', 'getaway', 'lovers', 'honeymoon', 'affectionate', 'intimate'],
    'cultural': ['cultural', 'culture seekers', 'culture enthusiasts', 'tradition', 'heritage', 'local vibe'],
    'art': ['art', 'art lovers', 'art enthusiasts', 'museums', 'galleries', 'design lovers', 'architecture enthusiasts'],
    'food': ['foodie', 'food', 'gastronomy', 'tapas', 'paella', 'wine lovers', 'beer lovers', 'chocolate lovers', 'seafood lovers'],
    'city break': ['city break', 'city explorers', 'urban', 'city trip', 'metropolitan', 'city center'],
    'historical': ['historical', 'historic','history', 'history buffs', 'history enthusiasts', 'ancient history', 'medieval', 'byzantine', 'ottoman', 'roman history', 'wwii history', 'ancient civilization'],
    'relax': ['relaxed','relax', 'relaxation seekers', 'peaceful', 'tranquil', 'calm', 'easygoing', 'laid-back'],
    'adventure': ['adventure', 'adventurous', 'adventure seekers', 'active holiday', 'thrill seekers', 'hiking', 'skiing', 'surfing', 'diving', 'kayaking', 'canyoning', 'rafting', 'via ferrata', 'mountain sports'],
    'nightlife': ['nightlife', 'nightlife seekers', 'nightlife enthusiasts', 'nightlife vibe', 'bars', 'clubs', 'energetic city', 'lively city', 'vibrant city'],
    'architecture': ['architecture', 'architecture lovers', 'architecture enthusiasts', 'modern architecture', 'baroque architecture', 'art nouveau architecture', 'design architecture', 'royal palaces', 'castles', 'chateaux'],
    'nature': ['nature', 'nature lovers', 'nature enthusiasts', 'scenic beauty', 'natural wonder', 'national parks', 'wildlife', 'birdwatching', 'garden enthusiasts', 'flower lovers', 'geological interest', 'unique flora', 'green spaces', 'rugged beauty'],
    'unique experience': ['unique experience', 'unique experience seekers', 'off-the-beaten-path', 'unusual', 'distinctive', 'memorable', 'authentic', 'original'],
    'beach': ['beach', 'beach lovers', 'beach vacation', 'coastal', 'seaside', 'beaches nearby', 'sunny weather & beach lovers', 'beach vacationers', 'golden beaches', 'sandy beaches', 'coastal region', 'coast nearby', 'coastal scenery', 'coastal drives'],
    'hiking': ['hiking', 'hikers', 'walking trails', 'scenic walks', 'mountain walks', 'coastal walks', 'mudflat hiking'],
    'skiing': ['skiing', 'skiers', 'ski resorts', 'winter sports'],
    'cycling': ['cycling', 'cyclists', 'bike tours', 'cycle routes', 'bike paths', 'cycling friendly'],
    'photography': ['photography', 'photographers', 'photo spots', 'picturesque', 'instagrammable', 'scenic views', 'stunning photography'],
    'relaxing getaway': ['relaxing getaway', 'peaceful getaway', 'relaxed getaway seekers', 'tranquil escape', 'serene retreat', 'unwind', 'rejuvenate', 'restful holiday'],
    'mountain': ['mountain', 'mountain views', 'mountain scenery', 'mountain lovers', 'mountain enthusiasts', 'mountain & city blend', 'mountain & beach blend', 'mountain town', 'mountain village', 'mountain sports', 'mountain peaks', 'austrian mountain culture', 'swiss alps', 'fjord scenery'],
    'castle': ['castle', 'castle lovers', 'castle enthusiasts', 'chateaux', 'royal palaces', 'fortresses', 'medieval castle', 'fairytale castle', 'historic castles', 'castle ruins'],
    'river': ['river', 'river views', 'river scenery', 'river cruises', 'danube river', 'riverfront', 'rivers confluence', 'river valley', 'river cruises enthusiasts'],
    'garden': ['garden', 'garden enthusiasts', 'garden lovers', 'flower lovers', 'tulip gardens', 'hanging gardens', 'botanical gardens', 'royal gardens', 'formal gardens'],
    'wellness': ['wellness', 'wellness seekers', 'spa & wellness', 'spa & wellness seekers', 'thermal bath', 'thermal bath', 'geothermal spa', 'geothermal spas', 'hot springs', 'sauna culture', 'massage', 'rejuvenation', 'wellbeing'],
    'music': ['music', 'music lovers', 'classical music lovers', 'fado music', 'live music', 'opera', 'concerts', 'music festivals', 'music scene'],
    'literary atmosphere': ['literary', 'literary enthusiasts', 'literature lovers', 'book lovers', 'literary connections', 'book towns', 'poets', 'writers', 'authors', 'reading', 'bookshops'],
    'spirituality': ['spiritual', 'spiritual seekers', 'religious seekers', 'pilgrimage', 'pilgrimage seekers', 'religious', 'monasteries', 'abbeys', 'churches', 'temples', 'holy sites', 'divine', 'sacred'],
    'golf': ['golf', 'golfers', 'golf resorts', 'golf courses', 'golfing', 'tee time'],
    'wine': ['wine', 'wine lovers', 'wine tourism', 'wine tasting', 'vineyards', 'wine route', 'wine cellars', 'wine chateaux', 'wine regions', 'wine culture'],
    'beer': ['beer', 'beer lovers', 'beer gardens', 'beer culture', 'craft beer', 'brewery tours', 'beer tents', 'pub culture'],
    'whiskey': ['whiskey', 'whiskey lovers', 'whiskey distilleries', 'scotch whisky', 'irish whiskey', 'whiskey trails'],
    'coffee culture': ['coffee culture', 'coffee lovers', 'cafes', 'coffee houses', 'espresso', 'cappuccino', 'latte', 'coffee shops', 'european cafes', 'coffee scene'],
    'design': ['design', 'design lovers', 'design enthusiasts', 'modern design', 'interior design', 'fashion design', 'urban design', 'architectural design', 'graphic design'],
    'shopping': ['shopping', 'shoppers', 'shopaholics', 'retail therapy', 'boutiques', 'department stores', 'markets', 'souvenirs', 'fashion enthusiasts'],
    'energetic': ['energetic', 'energetic city explorers', 'lively atmosphere seekers', 'vibrant atmosphere', 'bustling', 'dynamic', 'fast-paced', 'action-packed'],
    'charming villages': ['charming villages', 'picturesque villages', 'charming towns', 'picturesque towns', 'village life', 'rural charm', 'quaint villages', 'historic villages'],
    'rugged beauty': ['rugged beauty', 'rugged landscapes', 'dramatic landscapes', 'dramatic cliffs', 'rugged coastline', 'wild landscapes', 'untamed nature', 'unspoiled nature', 'raw beauty'] ,
    'baltic charm': ['baltic charm', 'baltic cities', 'baltic region', 'baltic heritage', 'baltic sea', 'baltic coast', 'baltic culture']
}

suitable_for_synonyms_mapping = {
    'families': ['family', 'theme park enthusiast', 'disney fan', 'family fun seeker', 'lego fan', 'creative fun seeker', 'ride seeker', 'european culture (themed) fan', 'amusement park enthusiast'],
    'couples': ['couple', 'romantic getaway', 'romantic getaway seeker'],
    'groups': ['group'],
    'individuals_solo': ['individual'],
    'budget': ['budget traveler'],
    'luxury': ['luxury traveler', 'glamour seeker', 'monaco visitor'],
    'adventure': ['cyclist', 'adventure seeker', 'diver', 'sailor', 'kayaker', 'adventure seeker (surfer)', 'surfer', 'off-the-beaten-path seeker', 'skier', 'via ferrata enthusiast', 'mountain sports fan', 'adrenaline seeker', 'canyoning enthusiast', 'rafting enthusiast', 'active holiday seeker', 'arctic exploration fan', 'thrill seeker', 'unique experience seeker'],
    'nature_outdoors': ['sunny weather lover', 'scenic beauty enthusiast', 'nature enthusiast', 'northern lights hunter', 'green space lover', 'mountain & city blend seeker', 'danube river view seeker', 'mountain view lover', 'city & nature blend seeker', 'hiker', 'garden enthusiast', 'volcano enthusiast', 'mountain & beach blend seeker', 'rugged beauty fan', 'remote beauty fan', 'island hopper', 'scenic drive lover', 'scenic walk lover', 'rugged coastline fan', 'coastal scenery fan', 'scenic beauty seeker', 'mountain lover', 'scenic beauty fan', 'fairytale landscape lover', 'mountain enthusiast', 'wilderness seeker', 'unique landscape enthusiast', 'fairytale landscape fan', 'northern spain beauty seeker', 'rural france enthusiast', 'accessible nature seeker', 'geological interest seeker', 'cliffs of moher visitor', 'unique nature seeker', 'fjord scenery fan', 'flower lover', 'waterfall enthusiast', 'english countryside fan', 'sunset view lover', 'garden lover'],
    'beach': ['beach lover', 'beach lover (nearby)', 'sunny weather & beach lover (nearby)', 'sun seeker', 'swimmer', 'beach vacationer'],
    'city_explorers': ['young adult', 'friendly atmosphere seeker', 'city explorer', 'modern & traditional blend fan', 'energetic city explorer', 'evolving city explorer', 'lively city explorer', 'green city enthusiast', 'cosmopolitan vibe seeker', 'port city explorer', 'colorful city explorer', 'friendly city seeker', 'mediterranean vibe seeker', 'day tripper from stockholm', 'charming village seeker', 'lively atmosphere seeker', 'charming town seeker', 'coastal town explorer', 'diverse region explorer', 'first-time paris visitor', 'london sightseer', 'berlin sightseer', 'prague sightseer', 'seasonal attraction seeker', 'venice visitor', 'unique attraction seeker', 'brussels visitor', 'budapest sightseer', 'edinburgh sightseer', 'istanbul sightseer', 'urban explorer', 'festive atmosphere seeker'],
    'history': ['history buff', 'modern history fan', 'tech & history blend seeker', 'castle lover', 'history buff (jurassic coast)', 'ancient history fan', 'wwii history fan', 'history buff (stately home)', 'roman history fan', 'history buff (steam train)', 'nostalgia seeker', 'history buff (wwi)', 'history buff (wwii)', 'history buff (water management)', 'industrial heritage enthusiast', 'medieval town enthusiast', 'ancient history enthusiast', 'greek mythology fan', 'archaeological site visitor', 'royal culture enthusiast', 'british history fan', 'german history fan', 'hungarian history fan', 'scottish history fan', 'spooky attraction seeker', 'medieval history fan', 'royal history fan', 'religious history fan', 'ottoman history fan', 'archaeological site enthusiast', 'unique historical experience seeker', 'somber reflection seeker', 'holocaust remembrance', 'dark tourism enthusiast'],
    'art_culture': ['art lover', 'culture seeker', 'literature lover', 'design lover', 'modern culture seeker', 'modern architecture fan', 'architecture lover', 'baltic charm seeker', 'swiss charm seeker', 'diplomacy & international affairs enthusiast', 'french culture fan', 'eu interest seeker', 'architecture enthusiast', 'unique culture seeker', 'swedish culture fan', 'culture seeker (celtic)', 'culture seeker (basque)', 'venetian influence fan', 'culture seeker (folklore)', 'monastery visitor', 'literary enthusiast', 'french & german culture fan', 'basque culture fan', 'traditional village seeker', 'culture seeker (welsh)', 'culture seeker (bavarian)', 'sound of music fan', 'austrian culture fan', 'culture seeker (gaelic)', 'european culture enthusiast', 'dutch culture fan', 'unesco site enthusiast', 'culture seeker (slovak wine)', 'culture seeker (folklore & saxon)', 'religious seeker', 'fairytale enthusiast', 'religious architecture fan', 'unique design seeker', 'art & faith enthusiast', 'game of thrones fan', 'pilgrimage seeker', 'folklore enthusiast', 'cultural significance seeker', 'cultural experience seeker', 'religious pilgrim', 'classic charm seeker', 'cultural event enthusiast', 'venetian culture fan', 'culture seeker (spanish tradition)', 'festival goer', 'british culture enthusiast', 'italian culture enthusiast'],
    'foodies': ['food', 'whiskey lover', 'food (chocolate & beer)', 'food (paella)', 'port wine lover', 'food (pizza)', 'gastronomy enthusiast', 'wine lover', 'seafood lover', 'food (cream tea)', 'beer lover', 'food (truffle, italian)', 'food (truffle)', 'wine lover (champagne)', 'wine lover (bordeaux)', 'wine tourism enthusiast', 'wine lover (rhône)', 'food (beer & chocolate)', 'food (southern italian)', 'food (spicy italian)'],
    'relaxation_wellness': ['relaxed traveler', 'relaxation seeker', 'sauna culture seeker', 'peaceful getaway seeker', 'relaxed getaway seeker', 'resort vacationer', 'relaxed vacation seeker', 'cruise enthusiast', 'spa & wellness seeker', 'spiritual seeker', 'river cruise enthusiast', 'spa & wellness enthusiast', 'wellness seeker', 'rail travel enthusiast', 'long journey fan'],
    'nightlife': ['nightlife seeker', 'celebration seeker'],
    'shopping_fashion': ['shopper', 'fashion enthusiast', 'diamond interest seeker'],
    'sports': ['golfer', 'sports enthusiast', 'tennis fan', 'sporting event attendee', 'motorsports fan'],
    'photography': ['photographer'],
    'music': ['classical music lover', 'music lover'],
    'wildlife_animals': ['wildlife enthusiast', 'birdwatcher']
}