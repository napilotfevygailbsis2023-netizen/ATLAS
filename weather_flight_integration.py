import sys, os, datetime, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import weather

# Weather conditions that affect flights
SEVERE_WEATHER_CONDITIONS = [
    'Thunderstorm', 'Heavy Rain', 'Snow', 'Blizzard', 
    'Hail', 'Tornado', 'Hurricane', 'Typhoon',
    'Severe Thunderstorm', 'Heavy Snow', 'Ice Storm'
]

MODERATE_WEATHER_CONDITIONS = [
    'Rain', 'Drizzle', 'Light Snow', 'Mist', 'Fog', 'Haze'
]

def check_flight_weather_impact(city, departure_time=None):
    """Check if weather conditions will impact flights"""
    try:
        # Get current weather
        current_weather = weather.fetch_weather(city)
        condition = current_weather.get('cond', '')
        visibility = current_weather.get('vis', '10')
        wind_speed = current_weather.get('wind', '0')
        
        # Extract wind speed numeric value
        try:
            wind_kmh = float(wind_speed.replace(' km/h', '').replace(' km/h', ''))
        except:
            wind_kmh = 0
        
        # Get forecast if departure time is provided
        forecast_impact = None
        if departure_time:
            forecast = weather.fetch_forecast(city)
            # Simple forecast impact assessment
            forecast_impact = assess_forecast_impact(forecast)
        
        # Determine impact level
        impact_level = determine_weather_impact(condition, wind_kmh, visibility)
        
        return {
            'current_condition': condition,
            'wind_speed': wind_kmh,
            'visibility': visibility,
            'impact_level': impact_level,
            'recommendation': get_weather_recommendation(impact_level, condition),
            'forecast_impact': forecast_impact,
            'alert_message': get_weather_alert(impact_level, condition)
        }
        
    except Exception as e:
        print(f"Error checking flight weather impact: {e}")
        return {
            'impact_level': 'unknown',
            'recommendation': 'Weather data unavailable. Check with airline.',
            'alert_message': 'Weather information temporarily unavailable.'
        }

def determine_weather_impact(condition, wind_speed, visibility):
    """Determine weather impact level on flights"""
    condition_lower = condition.lower()
    
    # Check for severe weather
    for severe in SEVERE_WEATHER_CONDITIONS:
        if severe.lower() in condition_lower:
            return 'severe'
    
    # Check for wind conditions
    if wind_speed > 60:  # High winds
        return 'severe'
    elif wind_speed > 40:  # Moderate winds
        return 'moderate'
    
    # Check for visibility
    try:
        visibility_km = float(visibility.replace(' km', '').replace(' km', ''))
        if visibility_km < 1:  # Very low visibility
            return 'severe'
        elif visibility_km < 3:  # Low visibility
            return 'moderate'
    except:
        pass
    
    # Check for moderate weather
    for moderate in MODERATE_WEATHER_CONDITIONS:
        if moderate.lower() in condition_lower:
            return 'moderate'
    
    # Check for clear conditions
    if 'clear' in condition_lower or 'sunny' in condition_lower:
        return 'good'
    
    return 'normal'

def assess_forecast_impact(forecast):
    """Assess weather forecast impact on flights"""
    if not forecast:
        return 'unknown'
    
    severe_count = 0
    moderate_count = 0
    
    for temp, desc, icon in forecast:
        desc_lower = desc.lower()
        
        for severe in SEVERE_WEATHER_CONDITIONS:
            if severe.lower() in desc_lower:
                severe_count += 1
                break
        
        for moderate in MODERATE_WEATHER_CONDITIONS:
            if moderate.lower() in desc_lower:
                moderate_count += 1
                break
    
    if severe_count > 0:
        return 'severe'
    elif moderate_count > 2:
        return 'moderate'
    elif moderate_count > 0:
        return 'light'
    
    return 'good'

def get_weather_recommendation(impact_level, condition):
    """Get weather-based flight recommendations"""
    recommendations = {
        'severe': f"&#9888; SEVERE WEATHER ALERT: {condition}. Expect significant delays or cancellations. Contact airline for updates.",
        'moderate': f"&#9888; MODERATE WEATHER: {condition}. Possible delays expected. Monitor flight status.",
        'normal': f"&#10003; Normal weather conditions. Flight operations expected to proceed normally.",
        'good': f"&#10003; Excellent weather conditions. Ideal for flight operations.",
        'unknown': "Weather information unavailable. Please check with your airline."
    }
    
    return recommendations.get(impact_level, recommendations['unknown'])

def get_weather_alert(impact_level, condition):
    """Get weather alert message"""
    if impact_level == 'severe':
        return f"SEVERE WEATHER WARNING: {condition} may cause flight disruptions. Check with airline before traveling to airport."
    elif impact_level == 'moderate':
        return f"Weather Advisory: {condition} conditions may cause minor delays. Allow extra travel time."
    
    return None

def check_flight_route_weather(origin, destination, departure_time=None):
    """Check weather for entire flight route"""
    # Map cities to weather locations
    city_weather_map = {
        'Manila': 'Manila',
        'Cebu': 'Manila',  # Use Manila as closest
        'Davao': 'Manila',  # Use Manila as closest
        'Baguio': 'Baguio',
        'Ilocos Norte': 'Ilocos Norte',
        'La Union': 'La Union',
        'Albay': 'Albay',
        'Bataan': 'Bataan',
        'Batangas': 'Batangas',
        'Pangasinan': 'Pangasinan',
        'Tagaytay': 'Tagaytay',
        'Vigan': 'Vigan'
    }
    
    origin_city = city_weather_map.get(origin, 'Manila')
    dest_city = city_weather_map.get(destination, 'Manila')
    
    origin_weather = check_flight_weather_impact(origin_city, departure_time)
    dest_weather = check_flight_weather_impact(dest_city, departure_time)
    
    # Determine overall route impact
    route_impact = determine_route_impact(origin_weather['impact_level'], dest_weather['impact_level'])
    
    return {
        'origin': {
            'city': origin,
            'weather': origin_weather
        },
        'destination': {
            'city': destination,
            'weather': dest_weather
        },
        'route_impact': route_impact,
        'overall_recommendation': get_route_recommendation(route_impact, origin_weather, dest_weather)
    }

def determine_route_impact(origin_impact, dest_impact):
    """Determine overall route impact based on origin and destination"""
    impact_levels = ['good', 'normal', 'moderate', 'severe', 'unknown']
    
    # Find the worse impact level
    for level in reversed(impact_levels):
        if origin_impact == level or dest_impact == level:
            return level
    
    return 'normal'

def get_route_recommendation(route_impact, origin_weather, dest_weather):
    """Get route-specific weather recommendation"""
    if route_impact == 'severe':
        return f"&#9888; SEVERE WEATHER ON ROUTE: {origin_weather['current_condition']} at origin, {dest_weather['current_condition']} at destination. High risk of delays/cancellations."
    elif route_impact == 'moderate':
        return f"&#9888; MODERATE WEATHER ON ROUTE: Weather conditions may cause delays. Monitor flight status."
    elif route_impact == 'good':
        return f"&#10003; Good weather conditions throughout route. Flight operations expected normally."
    
    return "Weather conditions appear normal for this route."

def render_weather_flight_alert(weather_data):
    """Render weather alert for flight display"""
    if not weather_data:
        return ""
    
    impact_level = weather_data.get('impact_level', 'normal')
    recommendation = weather_data.get('recommendation', '')
    alert_message = weather_data.get('alert_message', '')
    
    alert_colors = {
        'severe': ('#DC2626', '#FEF2F2'),
        'moderate': ('#D97706', '#FFFBEB'),
        'good': ('#059669', '#ECFDF5'),
        'normal': ('#0038A8', '#EFF6FF'),
        'unknown': ('#6B7280', '#F9FAFB')
    }
    
    color, bg = alert_colors.get(impact_level, alert_colors['normal'])
    
    alert_html = f"""
    <div style="background:{bg};border-left:4px solid {color};padding:12px 16px;border-radius:8px;margin-bottom:16px">
        <div style="font-weight:700;color:{color};margin-bottom:4px">Weather Advisory</div>
        <div style="font-size:13px;color:#374151;line-height:1.5">{recommendation}</div>
        {f'<div style="margin-top:8px;font-size:12px;color:{color};font-weight:600">{alert_message}</div>' if alert_message else ''}
    </div>"""
    
    return alert_html

def update_flight_status_due_to_weather(flight_id, weather_impact):
    """Update flight status based on weather conditions"""
    try:
        import flight_booking
        
        status_mapping = {
            'severe': 'cancelled',
            'moderate': 'delayed',
            'good': 'on_time',
            'normal': 'scheduled'
        }
        
        new_status = status_mapping.get(weather_impact, 'scheduled')
        
        # This would update the flight booking status
        # flight_booking.update_flight_status(flight_id, new_status)
        
        return new_status
        
    except Exception as e:
        print(f"Error updating flight status: {e}")
        return 'scheduled'
