'''

This module takes an City and Queries open-meteo.com for a temperature, Weather Code And Pressure

January 2026, Skadi Wiesemann

'''

import requests
import json

from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype

code = {
    0: 'Klarer Himmel',
    1: 'Überwiegend Klarer Himmel',
    2: 'Partiell Bewölkt',
    3: 'Bewölkt',
    45: 'Nebel',
    48: 'Überfrierender Nebel',
    51: 'Leichter Nieselregen',
    53: 'Mittlerer Nieselregen',
    55: 'Schwerer Nieselregen',
    56: 'Leichter überfrierender  Nieselregen',
    57: 'Schwerer überfrierender  Nieselregen',
    61: 'Leichter Regen',
    63: 'Mitterer Regen',
    65: 'Schwerer Regen',
    66: 'Leichter frierender  Regen',
    67: 'Schwerer frierender  Regen',
    71: 'Leichter Schneefall',
    73: 'Mittlerer Schneefall',
    75: 'Schwerer Schneefall',
    77: 'Graupel',
    80: 'Leichter Regenschauer',
    81: 'Mittlerer Regenschauer',
    82: 'Schwerer Regenschauer',
    85: 'Leichtes Schneegestöber',
    86: 'Schweres Schneegestöber',
    95: 'Gewitter',
    96: 'Gewitter',
    99: 'Gewitter',
}

land = {
    'AF': 'Afghanistan',
    'EG': 'Ägypten',
    'AX': 'Ålandinseln',
    'AL': 'Albanien',
    'DZ': 'Algerien',
    'AS': 'Amerikanisch Samoa',
    'AD': 'Andorra',
    'AO': 'Angola',
    'AI': 'Anguilla',
    'AQ': 'Antarktis',
    'AG': 'Antigua und Barbuda',
    'GQ': 'Äquatorialguinea',
    'AR': 'Argentinien',
    'AM': 'Armenien',
    'AW': 'Aruba',
    'AZ': 'Aserbaidschan',
    'ET': 'Äthiopien',
    'AU': 'Australien',
    'BS': 'Bahamas',
    'BH': 'Bahrain',
    'BD': 'Bangladesch',
    'BB': 'Barbados',
    'BY': 'Belarus',
    'BE': 'Belgien',
    'BZ': 'Belize',
    'BJ': 'Benin',
    'BM': 'Bermuda',
    'BT': 'Bhutan',
    'BO': 'Bolivien',
    'BA': 'Bosnien und Herzegowina',
    'BW': 'Botswana',
    'BV': 'Bouvetinsel',
    'BR': 'Brasilien',
    'IO': 'Britisches Territorium im Indischen Ozean',
    'BN': 'Brunei',
    'BG': 'Bulgarien',
    'BF': 'Burkina Faso',
    'BI': 'Burundi',
    'CL': 'Chile',
    'CN': 'China',
    'CK': 'Cookinseln',
    'CR': 'Costa Rica',
    'CW': 'Curaçao',
    'DK': 'Dänemark',
    'CD': 'Demokratische Republik Kongo',
    'DE': 'Deutschland',
    'DM': 'Dominica',
    'DO': 'Dominikanische Republik',
    'DJ': 'Dschibuti',
    'EC': 'Ecuador',
    'SV': 'El Salvador',
    'CI': 'Elfenbeinküste',
    'ER': 'Eritrea',
    'EE': 'Estland',
    'SZ': 'Eswatini',
    'FK': 'Falklandinseln',
    'FO': 'Färöer-Inseln',
    'FJ': 'Fidschi',
    'FI': 'Finnland',
    'FM': 'Föderierte Staaten von Mikronesien',
    'FR': 'Frankreich',
    'GF': 'Französisch-Guayana',
    'PF': 'Französisch-Polynesien',
    'TF': 'Französische Süd- und Antarktisgebiete',
    'MC': 'Fürstentum Monaco',
    'GA': 'Gabun',
    'GM': 'Gambia',
    'GE': 'Georgien',
    'GH': 'Ghana',
    'GI': 'Gibraltar',
    'GD': 'Grenada',
    'GR': 'Griechenland',
    'GL': 'Grönland',
    'GP': 'Guadeloupe',
    'GU': 'Guam',
    'GT': 'Guatemala',
    'GG': 'Guernsey',
    'GN': 'Guinea',
    'GW': 'Guinea-Bissau',
    'GY': 'Guyana',
    'HT': 'Haiti',
    'HM': 'Heard und McDonald Inseln',
    'HN': 'Honduras',
    'HK': 'Hongkong',
    'IN': 'Indien',
    'ID': 'Indonesien',
    'IM': 'Insel Man',
    'IQ': 'Irak',
    'IR': 'Iran',
    'IE': 'Irland',
    'IS': 'Island',
    'IL': 'Israel',
    'IT': 'Italien',
    'JM': 'Jamaika',
    'JP': 'Japan',
    'YE': 'Jemen',
    'JE': 'Jersey',
    'JO': 'Jordanien',
    'VG': 'Britische Jungferninseln',
    'VI': 'Amerikanische Jungferninseln',
    'KY': 'Kaimaninseln',
    'KH': 'Kambodscha',
    'CM': 'Kamerun',
    'CA': 'Kanada',
    'CV': 'Kap Verde',
    'BQ': 'Karibische Niederlande',
    'KZ': 'Kasachstan',
    'QA': 'Katar',
    'KE': 'Kenia',
    'KG': 'Kirgisistan',
    'KI': 'Kiribati',
    'UM': 'Inseln der Vereinigten Staaten',
    'CC': 'Kokosinseln',
    'CO': 'Kolumbien',
    'KM': 'Komoren',
    'XK': 'Kosovo',
    'HR': 'Kroatien',
    'CU': 'Kuba',
    'KW': 'Kuwait',
    'LA': 'Laos',
    'LS': 'Lesotho',
    'LV': 'Lettland',
    'LB': 'Libanon',
    'LR': 'Liberia',
    'LY': 'Libyen',
    'LI': 'Liechtenstein',
    'LT': 'Litauen',
    'LU': 'Luxemburg',
    'MO': 'Macau',
    'MG': 'Madagaskar',
    'MW': 'Malawi',
    'MY': 'Malaysia',
    'MV': 'Malediven',
    'ML': 'Mali',
    'MT': 'Malta',
    'MA': 'Marokko',
    'MH': 'Marshallinseln',
    'MQ': 'Martinique',
    'MR': 'Mauretanien',
    'MU': 'Mauritius',
    'YT': 'Mayotte',
    'MX': 'Mexiko',
    'MD': 'Moldawien',
    'MN': 'Mongolei',
    'ME': 'Montenegro',
    'MS': 'Montserrat',
    'MZ': 'Mosambik',
    'MM': 'Myanmar',
    'NA': 'Namibia',
    'NR': 'Nauru',
    'NP': 'Nepal',
    'NC': 'Neukaledonien',
    'NZ': 'Neuseeland',
    'NI': 'Nicaragua',
    'NL': 'Niederlande',
    'NE': 'Niger',
    'NG': 'Nigeria',
    'NU': 'Niue',
    'KP': 'Nordkorea',
    'MP': 'Nördliche Marianen',
    'MK': 'Nordmazedonien',
    'NF': 'Norfolkinsel',
    'NO': 'Norwegen',
    'OM': 'Oman',
    'AT': 'Österreich',
    'TL': 'Osttimor',
    'PK': 'Pakistan',
    'PS': 'Palästina',
    'PW': 'Palau',
    'PA': 'Panama',
    'PG': 'Papua-Neuguinea',
    'PY': 'Paraguay',
    'PE': 'Peru',
    'PH': 'Philippinen',
    'PN': 'Pitcairninseln',
    'PL': 'Polen',
    'PT': 'Portugal',
    'PR': 'Puerto Rico',
    'CG': 'Republik Kongo',
    'RE': 'Réunion',
    'RW': 'Ruanda',
    'RO': 'Rumänien',
    'RU': 'Russland',
    'MF': 'Saint Martin',
    'SB': 'Salomonen',
    'ZM': 'Sambia',
    'WS': 'Samoa',
    'SM': 'San Marino',
    'BL': 'Sankt Bartholomäus',
    'ST': 'São Tomé und Príncipe',
    'SA': 'Saudi-Arabien',
    'SE': 'Schweden',
    'CH': 'Schweiz',
    'SN': 'Senegal',
    'RS': 'Serbien',
    'SC': 'Seychellen',
    'SL': 'Sierra Leone',
    'ZW': 'Simbabwe',
    'SG': 'Singapur',
    'SX': 'Sint Maarten',
    'SK': 'Slowakei',
    'SI': 'Slowenien',
    'SO': 'Somalia',
    'ES': 'Spanien',
    'LK': 'Sri Lanka',
    'SH': 'St. Helena, Ascension und Tristan da Cunha',
    'KN': 'St. Kitts und Nevis',
    'LC': 'St. Lucia',
    'PM': 'St. Pierre und Miquelon',
    'VC': 'St. Vincent und die Grenadinen',
    'ZA': 'Südafrika',
    'SD': 'Sudan',
    'GS': 'Südgeorgien und die Südlichen Sandwichinseln',
    'KR': 'Südkorea',
    'SS': 'Südsudan',
    'SR': 'Suriname',
    'SJ': 'Svalbard und Jan Mayen',
    'SY': 'Syrien',
    'TJ': 'Tadschikistan',
    'TW': 'Taiwan',
    'TZ': 'Tansania',
    'TH': 'Thailand',
    'TG': 'Togo',
    'TK': 'Tokelau',
    'TO': 'Tonga',
    'TT': 'Trinidad und Tobago',
    'TD': 'Tschad',
    'CZ': 'Tschechien',
    'TN': 'Tunesien',
    'TR': 'Türkei',
    'TM': 'Turkmenistan',
    'TC': 'Turks und Caicosinseln',
    'TV': 'Tuvalu',
    'UG': 'Uganda',
    'UA': 'Ukraine',
    'HU': 'Ungarn',
    'UY': 'Uruguay',
    'UZ': 'Usbekistan',
    'VU': 'Vanuatu',
    'VA': 'Vatikanstadt',
    'VE': 'Venezuela',
    'AE': 'Vereinigte Arabische Emirate',
    'US': 'Vereinigte Staaten von Amerika',
    'GB': 'Vereinigtes Königreich',
    'VN': 'Vietnam',
    'WF': 'Wallis und Futuna',
    'CX': 'Weihnachtsinsel',
    'EH': 'Westsahara',
    'CF': 'Zentralafrikanische Republik',
    'CY': 'Zypern'
}

class WeatherObserver(PrivMsgObserverPrototype):

    @staticmethod
    def cmd():
        return ['.wetter']

    @staticmethod
    def help():
        return '.wetter <Stadt> - Befragt open-meteo.com nach einer Temperatur, Wettercode und Luftdruck am spezifizierten Ort'

    def update_on_priv_msg(self, data, connection: Connection):

        # Hoisting of variables
        global lat
        global long
        global City
        global country
        global temperature

        if data['message'].find('.wetter') == -1:
            return

        if data['message'].startswith('.wetter'):

            # split incoming message in '<City>'
            message = str(data['message'])
            city = message.replace('.wetter ', '')
            city = city.replace(' ', '+')

            # Get Coordinates for Specified City
            url = f'https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json'
            contents = requests.get(url)
            status = contents.status_code

            if status == 200:
                data1 = json.loads(contents.content)
                try:
                    dictLoc = data1['results'][0]
                except KeyError:
                    connection.send_back('Stadt nicht Gefunden', data)
                    return
                lat = dictLoc['latitude']
                long = dictLoc['longitude']
                City = dictLoc['name']
                country = dictLoc['country_code']

                # Get Weather info
                urlWeather = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&models=icon_seamless&current=weather_code,temperature_2m,surface_pressure&timezone=Europe%2FBerlin'
                contentsWeather = requests.get(urlWeather)
                statusWeather = contentsWeather.status_code

                if statusWeather == 200:
                    dataWeather = json.loads(contentsWeather.content)
                    dictWeather = dataWeather['current']
                    temperature = dictWeather['temperature_2m']
                    weather_code = dictWeather['weather_code']
                    pressure = dictWeather['surface_pressure']

                    connection.send_back(f'Die Temperatur in {City}, {land[country]} beträgt im Moment {temperature} °C. Die Witterung ist {code[weather_code]}. Der Luftdruck beträgt {pressure} hPa', data)

                else:
                    connection.send_back(f'Fehler: Get Temp: Statuscode:{status}', data)

            else:
                connection.send_back(f'Fehler: Get Coords: Statuscode:{status}', data)


