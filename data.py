# data.py — All static data for ATLAS

FLIGHTS = [
    {"from": "NAIA (MNL)", "to": "Laoag (LAO)",      "airline": "Philippine Airlines", "dep": "06:00", "arr": "07:15", "price": "₱2,450", "seats": 12, "dur": "1h 15m"},
    {"from": "NAIA (MNL)", "to": "Baguio (BAG)",      "airline": "Cebu Pacific",        "dep": "08:30", "arr": "09:20", "price": "₱1,890", "seats": 5,  "dur": "50m"},
    {"from": "NAIA (MNL)", "to": "Puerto Princesa",   "airline": "AirAsia",             "dep": "10:00", "arr": "11:30", "price": "₱3,200", "seats": 20, "dur": "1h 30m"},
    {"from": "NAIA (MNL)", "to": "Legazpi (LGP)",     "airline": "Philippine Airlines", "dep": "13:45", "arr": "14:50", "price": "₱2,100", "seats": 8,  "dur": "1h 05m"},
    {"from": "NAIA (MNL)", "to": "Tuguegarao (TUG)",  "airline": "Cebu Pacific",        "dep": "16:00", "arr": "17:10", "price": "₱1,750", "seats": 3,  "dur": "1h 10m"},
    {"from": "NAIA (MNL)", "to": "Vigan (VGN)",       "airline": "Philippine Airlines", "dep": "07:20", "arr": "08:30", "price": "₱2,300", "seats": 9,  "dur": "1h 10m"},
]

WEATHER = {
    "Manila":       {"temp": "32°C", "feel": "38°C", "cond": "Partly Cloudy", "hum": "78%", "wind": "12 km/h", "uv": "High",      "press": "1012 hPa", "vis": "10 km", "tip": "Bring an umbrella. Hot and humid conditions expected."},
    "Baguio":       {"temp": "18°C", "feel": "16°C", "cond": "Foggy",         "hum": "92%", "wind": "6 km/h",  "uv": "Low",       "press": "890 hPa",  "vis": "2 km",  "tip": "Bring a jacket. Foggy on mountain roads."},
    "Ilocos Norte": {"temp": "29°C", "feel": "33°C", "cond": "Sunny",         "hum": "65%", "wind": "18 km/h", "uv": "Very High", "press": "1010 hPa", "vis": "15 km", "tip": "Very high UV. Apply sunscreen and stay hydrated."},
    "Vigan":        {"temp": "28°C", "feel": "31°C", "cond": "Clear Sky",     "hum": "70%", "wind": "10 km/h", "uv": "High",      "press": "1011 hPa", "vis": "12 km", "tip": "Great day for heritage walks and photography!"},
    "Batangas":     {"temp": "31°C", "feel": "36°C", "cond": "Hot & Humid",   "hum": "82%", "wind": "8 km/h",  "uv": "Very High", "press": "1009 hPa", "vis": "10 km", "tip": "Stay hydrated. Visit Taal Volcano early morning."},
    "Tagaytay":     {"temp": "23°C", "feel": "21°C", "cond": "Breezy & Cool", "hum": "75%", "wind": "20 km/h", "uv": "Moderate",  "press": "930 hPa",  "vis": "14 km", "tip": "Perfect weather for outdoor dining and sightseeing."},
}

SPOTS = [
    {"name": "Intramuros",      "city": "Manila",       "cat": "Historical", "rating": 4.7, "visits": "2.1M/yr", "entry": "₱75",  "hours": "8AM-6PM",  "desc": "The Walled City — a living museum of Spanish colonial heritage featuring Fort Santiago and Manila Cathedral."},
    {"name": "Burnham Park",    "city": "Baguio",       "cat": "Nature",     "rating": 4.5, "visits": "1.8M/yr", "entry": "Free", "hours": "24 hours", "desc": "Iconic park with the famous boating lake in the City of Pines. Perfect for morning jogs and picnics."},
    {"name": "Paoay Church",    "city": "Ilocos Norte", "cat": "Heritage",   "rating": 4.9, "visits": "800K/yr", "entry": "Free", "hours": "6AM-8PM",  "desc": "UNESCO World Heritage baroque church with massive coral stone buttresses and walls."},
    {"name": "Calle Crisologo", "city": "Vigan",        "cat": "Heritage",   "rating": 4.8, "visits": "900K/yr", "entry": "Free", "hours": "24 hours", "desc": "Cobblestone street lined with Spanish colonial mansions. Kalesa rides and heritage stores."},
    {"name": "Taal Volcano",    "city": "Batangas",     "cat": "Nature",     "rating": 4.6, "visits": "1.2M/yr", "entry": "₱150", "hours": "6AM-2PM",  "desc": "Volcano within a lake within a volcano — a geological marvel offering stunning views."},
    {"name": "Fort Santiago",   "city": "Manila",       "cat": "Historical", "rating": 4.6, "visits": "1.3M/yr", "entry": "₱75",  "hours": "8AM-6PM",  "desc": "Citadel of Manila where Rizal spent his last night. Houses the Rizal Shrine and museum."},
    {"name": "Mayon Volcano",       "city": "Albay",       "cat": "Nature",     "rating": 4.9, "visits": "1.5M/yr", "entry": "₱50",  "hours": "6AM-4PM",  "desc": "The world's most perfect cone volcano. Iconic symbol of Albay offering breathtaking views and trekking adventures."},
    {"name": "Cagsawa Ruins",        "city": "Albay",       "cat": "Historical", "rating": 4.7, "visits": "800K/yr", "entry": "₱20",  "hours": "6AM-6PM",  "desc": "Ruins of an 18th-century Franciscan church buried by Mayon's 1814 eruption. Stunning backdrop of the volcano."},
    {"name": "Sumlang Lake",         "city": "Albay",       "cat": "Nature",     "rating": 4.6, "visits": "300K/yr", "entry": "Free", "hours": "6AM-6PM",  "desc": "Serene lake with a perfect reflection of Mayon Volcano. Popular for kayaking and bamboo rafting."},
    {"name": "Hundred Islands",      "city": "Pangasinan",  "cat": "Nature",     "rating": 4.8, "visits": "1.2M/yr", "entry": "₱100", "hours": "6AM-5PM",  "desc": "National park with 124 islands and islets in Lingayen Gulf. Perfect for island hopping and snorkeling."},
    {"name": "Lingayen Gulf",        "city": "Pangasinan",  "cat": "Landmark",   "rating": 4.5, "visits": "500K/yr", "entry": "Free", "hours": "24 hours", "desc": "Historic gulf and beach destination with WWII significance. Long stretches of sandy shoreline."},
    {"name": "Bolinao Falls",        "city": "Pangasinan",  "cat": "Nature",     "rating": 4.7, "visits": "400K/yr", "entry": "₱50",  "hours": "7AM-5PM",  "desc": "Multi-tiered waterfalls in a lush forest setting. Crystal clear cool waters perfect for swimming."},
    {"name": "Mt. Samat Shrine",     "city": "Bataan",      "cat": "Historical", "rating": 4.8, "visits": "600K/yr", "entry": "Free", "hours": "7AM-5PM",  "desc": "WWII memorial atop Mt. Samat with a towering cross. Panoramic views and profound historical significance."},
    {"name": "Pawikan Conservation", "city": "Bataan",      "cat": "Nature",     "rating": 4.6, "visits": "200K/yr", "entry": "Free", "hours": "5AM-6PM",  "desc": "Sea turtle nesting ground and conservation center. Watch hatchlings make their way to the sea."},
    {"name": "Bataan Death March",   "city": "Bataan",      "cat": "Historical", "rating": 4.7, "visits": "350K/yr", "entry": "Free", "hours": "8AM-5PM",  "desc": "Historic trail commemorating the 1942 WWII death march. Marker trail with museums along the route."},
    {"name": "Mt. Pulag",       "city": "Benguet",      "cat": "Nature",     "rating": 4.8, "visits": "60K/yr",  "entry": "₱200", "hours": "4AM-12PM", "desc": "Third highest peak — famed for its breathtaking sea of clouds at sunrise."},
]

RESTAURANTS = [
    {"name": "Cafe Adriatico",       "city": "Manila",       "type": "Filipino",         "price": "P350-700", "rating": 4.5},
    {"name": "Ilustrado Restaurant", "city": "Manila",       "type": "Heritage Filipino", "price": "P400-900", "rating": 4.7},
    {"name": "Cafe by the Ruins",    "city": "Baguio",       "type": "Cafe",              "price": "P200-450", "rating": 4.6},
    {"name": "Herencia Cafe",        "city": "Ilocos Norte", "type": "Ilocano",           "price": "P150-350", "rating": 4.5},
    {"name": "Crisantos Cafe",       "city": "Vigan",        "type": "Local Heritage",    "price": "P180-380", "rating": 4.4},
    {"name": "Leslies Restaurant",   "city": "Batangas",     "type": "Bulalo",            "price": "P250-500", "rating": 4.6},
    {"name": "Bicol Express House",   "city": "Albay",      "type": "Bicolano",   "price": "P150-350", "rating": 4.7},
    {"name": "Kagay-anon Restaurant", "city": "Albay",      "type": "Filipino",   "price": "P200-450", "rating": 4.5},
    {"name": "Lemon & Olives",        "city": "Pangasinan", "type": "Seafood",    "price": "P300-600", "rating": 4.6},
    {"name": "Sizzling Plate",        "city": "Pangasinan", "type": "Filipino",   "price": "P180-380", "rating": 4.4},
    {"name": "Balanga Grill",         "city": "Bataan",     "type": "Grilled",    "price": "P200-400", "rating": 4.5},
    {"name": "Capas Cafe",            "city": "Bataan",     "type": "Cafe",       "price": "P150-300", "rating": 4.3},
    {"name": "Forest House",         "city": "Baguio",       "type": "Filipino",          "price": "P250-500", "rating": 4.3},
]

GUIDES = [
    {"name": "Maria Santos",   "city": "Manila",       "lang": "EN, FIL, ES", "rate": "P2,500/day", "rating": 4.9, "tours": 142, "spec": "Historical & Cultural",   "avail": "Mon-Sat", "bio": "Certified guide with 8 years in Intramuros and Rizal Park. Fluent in Spanish.",              "pkgs": ["Half Day City Tour - P1,200", "Full Day Heritage - P2,500", "Private Group - P4,000"]},
    {"name": "Jose Dela Cruz", "city": "Baguio",       "lang": "EN, FIL",     "rate": "P2,000/day", "rating": 4.7, "tours": 89,  "spec": "Nature & Trekking",        "avail": "Tue-Sun", "bio": "Adventure guide specializing in Cordillera trekking. Certified first aid responder.",        "pkgs": ["Mt. Pulag Trek - P1,800", "Highlands Tour - P1,500", "Strawberry Farm - P800"]},
    {"name": "Ana Reyes",      "city": "Ilocos Norte", "lang": "EN, FIL, IL", "rate": "P1,800/day", "rating": 4.8, "tours": 116, "spec": "Heritage & Food Tours",    "avail": "Mon-Sun", "bio": "Native Ilocana with deep knowledge of heritage and food culture. Speaks Ilocano.",           "pkgs": ["Vigan Heritage Walk - P1,200", "Ilocos Food Tour - P1,600", "Paoay Trip - P1,800"]},
    {"name": "Liza Fernandez", "city": "Vigan",        "lang": "EN, FIL",     "rate": "P1,600/day", "rating": 4.6, "tours": 74,  "spec": "Spanish Colonial Heritage", "avail": "Mon-Fri", "bio": "Historian-trained guide for Vigan UNESCO heritage zone. Expert in colonial architecture.",   "pkgs": ["Calle Crisologo Walk - P900", "Full Heritage Day - P1,600", "Kalesa Tour - P1,200"]},
    {"name": "Ramon Garcia",   "city": "Batangas",     "lang": "EN, FIL",     "rate": "P2,200/day", "rating": 4.5, "tours": 58,  "spec": "Volcano & Beach Tours",    "avail": "Thu-Tue", "bio": "Local Batangueno guide with expertise in Taal Volcano treks and coastal tours.",            "pkgs": ["Taal Volcano Trek - P2,000", "Beach Hopping - P1,800", "Full Day Batangas - P2,200"]},
]

TRANSPORT = [
    {"type": "Bus",   "name": "Victory Liner",    "route": "Manila to Baguio",          "duration": "5-6 hours",   "price": "P450-650",  "schedule": "Every 30 mins", "class": "Aircon / Deluxe"},
    {"type": "Bus",   "name": "Partas Bus",        "route": "Manila to Ilocos Norte",    "duration": "8-9 hours",   "price": "P700-950",  "schedule": "6AM and 9PM",   "class": "Aircon / Sleeper"},
    {"type": "Van",   "name": "Genesis Transport", "route": "Manila to Batangas",        "duration": "2-3 hours",   "price": "P280-380",  "schedule": "Every 1 hour",  "class": "Air-conditioned Van"},
    {"type": "Bus",   "name": "Dominion Bus",      "route": "Manila to Vigan",           "duration": "7-8 hours",   "price": "P600-850",  "schedule": "7AM and 9PM",   "class": "Aircon / Deluxe"},
    {"type": "Van",   "name": "Joy Bus",           "route": "Manila to Tagaytay",        "duration": "1.5-2 hours", "price": "P200-300",  "schedule": "Every 45 mins", "class": "Premium Van"},
    {"type": "Train", "name": "PNR North",         "route": "Tutuban to Calamba",        "duration": "1.5 hours",   "price": "P50-80",    "schedule": "Every 1 hour",  "class": "Standard"},
    {"type": "Ferry", "name": "FastCat",           "route": "Batangas to Puerto Galera", "duration": "1 hour",      "price": "P350-500",  "schedule": "Every 2 hours", "class": "Economy / Business"},
]

ITINERARIES = {
    "Manila": [
        {"day": "Day 1 - Arrival and Old Manila", "color": "#0038A8", "acts": [["08:00","Land at NAIA Terminal 1"],["10:00","Check-in at hotel in Ermita"],["13:00","Lunch at Cafe Adriatico"],["15:00","Intramuros walking tour"],["17:00","Fort Santiago sunset visit"],["19:00","Dinner at Barbaras Heritage Restaurant"]]},
        {"day": "Day 2 - Rizal Park and Bay Area", "color": "#CE1126", "acts": [["08:00","Rizal Park morning walk"],["10:00","National Museum of Fine Arts"],["12:30","Lunch at SM Mall of Asia"],["14:30","Bay City promenade"],["16:00","Manila Ocean Park"],["19:30","Night market at Roxas Blvd"]]},
        {"day": "Day 3 - Day Trip to Tagaytay",   "color": "#C8930A", "acts": [["06:00","Early departure to Tagaytay"],["09:00","Taal Volcano viewpoint"],["11:00","Sky Ranch amusement park"],["13:00","Lunch - Bulalo at Leslies"],["15:00","Peoples Park in the Sky"],["18:00","Return to Manila"]]},
    ],
    "Baguio": [
        {"day": "Day 1 - City of Pines",     "color": "#0038A8", "acts": [["09:00","Arrive in Baguio"],["11:00","Check-in at hotel"],["13:00","Lunch at Good Taste"],["15:00","Burnham Park boating"],["17:00","Mines View Park"],["19:00","Dinner at Session Road"]]},
        {"day": "Day 2 - Nature and Highlands","color": "#CE1126", "acts": [["06:00","Strawberry Farm, La Trinidad"],["09:00","Tam-awan Village art tour"],["12:00","Bulalo lunch"],["14:00","Baguio Cathedral"],["16:00","Camp John Hay"],["19:00","Pasalubong shopping"]]},
    ],
}

# Extended itineraries for remaining cities
ITINERARIES_EXTRA = {
    "Tagaytay": [
        {"day": "Day 1 - Taal & Sky Ranch",      "color": "#0038A8", "acts": [["08:00","Arrive in Tagaytay"],["09:00","Taal Volcano viewpoint"],["11:00","Sky Ranch amusement park"],["13:00","Bulalo lunch at Leslies"],["15:00","Peoples Park in the Sky"],["18:00","Dinner at Bag of Beans"]]},
        {"day": "Day 2 - Nature & Relaxation",   "color": "#CE1126", "acts": [["07:00","Morning jog at Picnic Grove"],["09:00","Tagaytay Highlands"],["12:00","Lunch at Antonio's"],["14:00","Mahogany Market"],["16:00","Twin Lakes"],["19:00","Night view at Ridge"]]},
        {"day": "Day 3 - Day Trip to Batangas",  "color": "#C8930A", "acts": [["07:00","Drive to Batangas"],["09:00","Taal Heritage Town"],["12:00","Lunch at Mang Inasal"],["14:00","Caleruega Church"],["16:00","Return to Tagaytay"],["18:00","Souvenir shopping"]]},
    ],
    "Vigan": [
        {"day": "Day 1 - Heritage Walk",         "color": "#0038A8", "acts": [["09:00","Arrive in Vigan"],["10:00","Calle Crisologo walking tour"],["12:00","Lunch at Cafe Leona"],["14:00","Vigan Cathedral"],["16:00","Syquia Mansion Museum"],["18:00","Kalesa ride at sunset"]]},
        {"day": "Day 2 - Pottery & Markets",     "color": "#CE1126", "acts": [["08:00","Burnay pottery workshop"],["10:00","Mindoro Street antiques"],["12:00","Lunch at Batchoy House"],["14:00","Plaza Salcedo"],["16:00","Plaza Burgos"],["19:00","Vigan longganisa dinner"]]},
        {"day": "Day 3 - Ilocos Sur Side Trip",  "color": "#C8930A", "acts": [["07:00","Drive to Bantay"],["09:00","Bantay Bell Tower"],["11:00","Santa Maria Church"],["13:00","Lunch at local carinderia"],["15:00","Paoay Lake"],["17:00","Return to Vigan"]]},
    ],
    "Ilocos Norte": [
        {"day": "Day 1 - Windmills & Pagudpud",  "color": "#0038A8", "acts": [["08:00","Bangui Windmills"],["10:00","Cape Bojeador Lighthouse"],["12:00","Lunch in Laoag"],["14:00","Paoay Church UNESCO"],["16:00","Malacañang of the North"],["19:00","Dinner at Saramsam"]]},
        {"day": "Day 2 - Sand Dunes & Beach",    "color": "#CE1126", "acts": [["07:00","La Paz Sand Dunes 4x4"],["10:00","Laoag City Hall"],["12:00","Batac empanada lunch"],["14:00","Marcos Museum"],["16:00","Pagudpud beach"],["19:00","Seafood dinner"]]},
        {"day": "Day 3 - Blue Lagoon",           "color": "#C8930A", "acts": [["08:00","Patapat Viaduct"],["10:00","Blue Lagoon Pagudpud"],["12:00","Picnic lunch at beach"],["14:00","Kapurpurawan Rock"],["16:00","Adams Village"],["18:00","Depart Ilocos Norte"]]},
    ],
    "Batangas": [
        {"day": "Day 1 - Heritage & Taal Town",  "color": "#0038A8", "acts": [["09:00","Arrive in Batangas"],["10:00","Taal Heritage Town tour"],["12:00","Lunch at local restaurant"],["14:00","Basilica de San Martin"],["16:00","Taal Lake viewpoint"],["18:00","Dinner at Lipa"]]},
        {"day": "Day 2 - Anilao Diving",         "color": "#CE1126", "acts": [["07:00","Drive to Anilao"],["09:00","Snorkeling at Sepoc Beach"],["11:00","Dive at Beatrice Rock"],["13:00","Seafood lunch"],["15:00","Del Monte Beach"],["18:00","Sunset at Mabini"]]},
        {"day": "Day 3 - Laiya Beach",           "color": "#C8930A", "acts": [["08:00","Drive to San Juan Laiya"],["10:00","White sand beach"],["12:00","Beach picnic lunch"],["14:00","Island hopping"],["16:00","Caleruega Church"],["18:00","Depart Batangas"]]},
    ],
    "Albay": [
        {"day": "Day 1 - Mayon Volcano",         "color": "#0038A8", "acts": [["08:00","Arrive in Legazpi"],["09:00","Mayon Volcano viewpoint"],["11:00","Cagsawa Ruins"],["13:00","Bicolano lunch - Laing"],["15:00","Sumlang Lake kayak"],["18:00","Dinner at Legazpi Boulevard"]]},
        {"day": "Day 2 - ATV & Lava Tour",       "color": "#CE1126", "acts": [["07:00","ATV Mayon Lava Trail"],["10:00","Ligñon Hill viewdeck"],["12:00","Pili nut shopping"],["14:00","Daraga Church"],["16:00","Embarcadero de Legazpi"],["19:00","Bicol Express dinner"]]},
        {"day": "Day 3 - Island Hopping",        "color": "#C8930A", "acts": [["08:00","Boat to Misibis Bay"],["10:00","Santo Domingo black sand beach"],["12:00","Seafood lunch"],["14:00","Quitinday Hills"],["16:00","Tabaco City market"],["18:00","Depart Albay"]]},
    ],
    "Pangasinan": [
        {"day": "Day 1 - Hundred Islands",       "color": "#0038A8", "acts": [["08:00","Arrive in Alaminos"],["09:00","Hundred Islands boat tour"],["11:00","Governor Island snorkel"],["13:00","Seafood lunch in Alaminos"],["15:00","Lingayen Gulf beach"],["18:00","Dinner at Dagupan"]]},
        {"day": "Day 2 - Bolinao Falls",         "color": "#CE1126", "acts": [["07:00","Drive to Bolinao"],["09:00","Bolinao Falls 1 & 2"],["11:00","Cape Bolinao Lighthouse"],["13:00","Lunch at Bolinao"],["15:00","Patar White Beach"],["18:00","Bangus dinner in Dagupan"]]},
        {"day": "Day 3 - Manaoag & Urdaneta",    "color": "#C8930A", "acts": [["08:00","Our Lady of Manaoag Shrine"],["10:00","Urdaneta City tour"],["12:00","Lunch at local resto"],["14:00","Calasiao puto factory"],["16:00","San Fabian beach"],["18:00","Depart Pangasinan"]]},
    ],
    "Bataan": [
        {"day": "Day 1 - Mt. Samat & History",   "color": "#0038A8", "acts": [["08:00","Arrive in Bataan"],["09:00","Mt. Samat National Shrine"],["11:00","Dambana ng Kagitingan"],["13:00","Lunch in Pilar"],["15:00","Death March marker sites"],["18:00","Dinner in Balanga"]]},
        {"day": "Day 2 - Pawikan & Forests",     "color": "#CE1126", "acts": [["07:00","Pawikan Conservation Center"],["09:00","Morong Beach"],["11:00","Las Casas Filipinas"],["13:00","Spanish colonial lunch"],["15:00","Bagac mangrove forest"],["18:00","Sunset at Bagac Bay"]]},
        {"day": "Day 3 - Corregidor Island",     "color": "#C8930A", "acts": [["07:00","Ferry to Corregidor"],["09:00","Malinta Tunnel tour"],["11:00","Pacific War Memorial"],["13:00","Lunch on the island"],["15:00","Battery Way viewpoint"],["17:00","Ferry back to Bataan"]]},
    ],
}
