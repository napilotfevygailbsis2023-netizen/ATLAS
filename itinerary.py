import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell
from data import ITINERARIES, ITINERARIES_EXTRA

ALL_ITINERARIES = {**ITINERARIES, **ITINERARIES_EXTRA}

CITY_HIGHLIGHTS = {
    "Manila":       ["Intramuros walking tour","Rizal Park","National Museum","Manila Ocean Park","Fort Santiago","Binondo Chinatown food trip","BGC art walk","Malate nightlife","San Agustin Church","Manila Bay sunset","Divisoria shopping","Luneta concert"],
    "Baguio":       ["Burnham Park boating","Mines View Park","Strawberry Farm La Trinidad","Tam-awan Village","Baguio Cathedral","Camp John Hay","BenCab Museum","Wright Park horse riding","Botanical Garden","Night market Session Road","Baguio Public Market","Manor Hotel viewpoint"],
    "Tagaytay":     ["Taal Volcano viewpoint","Sky Ranch amusement park","Peoples Park in the Sky","Picnic Grove","Twin Lakes","Tagaytay Highlands","Bulalo lunch at Leslies","Bag of Beans cafe","Mahogany Market","Caleruega Church","Antonio's restaurant","Ridge viewpoint"],
    "Vigan":        ["Calle Crisologo walking tour","Vigan Cathedral","Syquia Mansion Museum","Kalesa ride","Burnay pottery workshop","Mindoro Street antiques","Plaza Salcedo","Plaza Burgos","Bantay Bell Tower","Santa Maria Church","Paoay Lake","Vigan longganisa dinner"],
    "Ilocos Norte": ["Bangui Windmills","Cape Bojeador Lighthouse","Paoay Church UNESCO","Malacañang of the North","La Paz Sand Dunes 4x4","Batac empanada lunch","Marcos Museum","Pagudpud beach","Blue Lagoon Pagudpud","Patapat Viaduct","Kapurpurawan Rock","Adams Village"],
    "Batangas":     ["Taal Heritage Town","Basilica de San Martin","Taal Lake viewpoint","Anilao snorkeling","Del Monte Beach","Laiya white sand beach","Island hopping Mabini","Caleruega Church","Dive at Beatrice Rock","Lipa City tour","San Juan market","Tingloy Island"],
    "Albay":        ["Mayon Volcano viewpoint","Cagsawa Ruins","Sumlang Lake kayak","ATV Mayon Lava Trail","Ligñon Hill viewdeck","Daraga Church","Embarcadero de Legazpi","Misibis Bay","Santo Domingo black sand beach","Quitinday Hills","Tabaco City market","Bicol Express dinner"],
    "Pangasinan":   ["Hundred Islands boat tour","Governor Island snorkel","Lingayen Gulf beach","Bolinao Falls","Cape Bolinao Lighthouse","Patar White Beach","Our Lady of Manaoag Shrine","Bangus festival Dagupan","Calasiao puto factory","San Fabian beach","Urdaneta City tour","Alaminos City market"],
    "Bataan":       ["Mt. Samat National Shrine","Dambana ng Kagitingan","Death March marker sites","Pawikan Conservation Center","Morong Beach","Las Casas Filipinas de Acuzar","Bagac mangrove forest","Corregidor Island tour","Malinta Tunnel","Pacific War Memorial","Battery Way viewpoint","Balanga City tour"],
}

MEAL_IDEAS = {
    "Manila":       ["Cafe Adriatico","Barbaras Heritage Restaurant","Aristocrat Restaurant","Max's Restaurant","Toyo Eatery","Manam Comfort Filipino"],
    "Baguio":       ["Good Taste Restaurant","Cafe by the Ruins","Vizco's Restaurant","Forest House","Canto Bogchi","Hill Station"],
    "Tagaytay":     ["Leslies Restaurant","Bag of Beans","Antonio's","Josephine Restaurant","Verbena","The Cellar"],
    "Vigan":        ["Cafe Leona","Batchoy House","Cafe Uno","Kusina ni Inang","Florentina Homes","Grandpa's Inn Restaurant"],
    "Ilocos Norte": ["Saramsam Ylocano Restaurant","Fort Ilocandia","La Preciosa","Herencia Cafe","Marco's Restaurant","El Patio"],
    "Batangas":     ["Mang Inasal Lipa","Bulaluhan sa Batangas","Felicidad Seafoods","D'Rough Riders","Gerry's Grill Batangas","Robinsons Lipa food court"],
    "Albay":        ["Legazpi Boulevard restaurants","Bob Marlin Restaurant","Waway's","Bigg's Diner","Old House Cafe","1st Colonial Grill"],
    "Pangasinan":   ["Sizzling Plate Dagupan","Seven Suites Hotel resto","Blackbeard's Seafood","Bonuan Blue Beach resto","Oyster Plaza","Dagupan bangus grills"],
    "Bataan":       ["Balanga food strip","Tatang's Carinderia","Wharton Hotel resto","Mariveles seafood market","Orani local eateries","Bagac Bay restaurants"],
}

DAY_COLORS = ["#0038A8","#CE1126","#C8930A","#065F46","#6B21A8","#0077B6","#B45309","#047857","#9D174D"]

def generate_days(dest, num_days):
    highlights = CITY_HIGHLIGHTS.get(dest, CITY_HIGHLIGHTS["Manila"])
    meals = MEAL_IDEAS.get(dest, MEAL_IDEAS["Manila"])
    days = []
    hi_index = 0
    meal_index = 0
    for d in range(num_days):
        color = DAY_COLORS[d % len(DAY_COLORS)]
        acts = []
        if d == 0:
            acts.append(("08:00", f"Arrive in {dest}, check in to hotel"))
        else:
            acts.append(("07:00", "Breakfast at hotel"))
        # Morning activity
        acts.append(("09:00", highlights[hi_index % len(highlights)])); hi_index += 1
        acts.append(("11:00", highlights[hi_index % len(highlights)])); hi_index += 1
        # Lunch
        acts.append(("13:00", f"Lunch at {meals[meal_index % len(meals)]}"))
        meal_index += 1
        # Afternoon activities
        acts.append(("15:00", highlights[hi_index % len(highlights)])); hi_index += 1
        acts.append(("17:00", highlights[hi_index % len(highlights)])); hi_index += 1
        # Dinner or last activity
        if d == num_days - 1:
            acts.append(("19:00", f"Farewell dinner at {meals[meal_index % len(meals)]}"))
            acts.append(("21:00", f"Depart {dest}"))
        else:
            acts.append(("19:00", f"Dinner at {meals[meal_index % len(meals)]}"))
        meal_index += 1
        days.append({"day": f"Day {d+1} - {dest} Adventure", "color": color, "acts": acts})
    return days

def render(dest="Manila", days=None, user=None):
    if dest not in CITY_HIGHLIGHTS:
        dest = "Manila"
    try:
        num_days = max(1, min(int(days), 14))
    except:
        num_days = 3

    generated = generate_days(dest, num_days)

    dest_opts = "".join(
        f'<option {"selected" if d == dest else ""}>{d}</option>'
        for d in sorted(CITY_HIGHLIGHTS.keys())
    )

    day_cards = ""
    for day in generated:
        acts = "".join(
            f'<div class="act-row" style="display:flex;gap:12px;padding:7px 0;border-bottom:1px solid #F3F4F6">'
            f'<div style="font-size:12px;color:#9CA3AF;min-width:50px;font-weight:600;padding-top:1px">{a[0]}</div>'
            f'<div style="font-size:13px;color:#374151">{a[1]}</div>'
            f'</div>'
            for a in day["acts"]
        )
        day_cards += (
            f'<div style="margin-bottom:16px;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.08)">'
            f'<div style="background:{day["color"]};padding:12px 18px;color:#fff;font-weight:700;font-size:15px">{day["day"]}</div>'
            f'<div style="padding:4px 18px 10px;background:#fff">{acts}</div>'
            f'</div>'
        )

    body = f"""
    <div class="page-wrap">
      <div style="margin-bottom:22px">
        <div class="section-title">Itinerary Planner</div>
        <div class="section-sub">Customize your travel plan — choose your destination and how many days you're staying</div>
      </div>
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#0038A8"><span>Plan Your Trip</span></div>
        <div class="card-body">
          <form method="get" style="display:flex;gap:14px;flex-wrap:wrap;align-items:flex-end">
            <div style="flex:1;min-width:160px">
              <label class="lbl">Destination</label>
              <select class="inp" name="dest">{dest_opts}</select>
            </div>
            <div style="min-width:140px">
              <label class="lbl">Number of Days (1–14)</label>
              <input class="inp" type="number" name="days" min="1" max="14" value="{num_days}" style="width:100%"/>
            </div>
            <button class="btn" style="background:#CE1126;color:#fff;padding:10px 24px" type="submit">Generate Itinerary</button>
          </form>
        </div>
      </div>
      <div style="margin-bottom:18px;display:flex;align-items:center;gap:12px;flex-wrap:wrap">
        <div>
          <div class="section-title" style="font-size:18px">{dest} — {num_days}-Day Itinerary</div>
          <div class="section-sub">Your personalized travel plan</div>
        </div>
        <span style="background:#0038A8;color:#fff;padding:5px 16px;border-radius:20px;font-size:13px;font-weight:700">{num_days} Day{"s" if num_days > 1 else ""}</span>
      </div>
      {day_cards}
    </div>"""
    return build_shell("Itinerary", body, "itinerary", user=user)
