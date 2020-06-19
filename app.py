import plotly.express as px
import pandas as pd
import pycountry
import pycountry_convert as pc
from datetime import datetime
import time
import dash
import dash_core_components as dcc
import dash_html_components as html


app = dash.Dash()

server = app.server

def country_name(x):
    country_codes = {
        "Bolivia": "BO",
        "Brunei": "BN",
        "Congo (Brazzaville)": "CG",
        "Congo (Kinshasa)": "CK",
        "Cote d'Ivoire": "CI",
        "Diamond Princess": "GB",
        "Holy See": "VA",
        "Iran": "IR",
        "Korea, South": "KR",
        "Moldova": "MD",
        "Russia": "RU",
        "Taiwan*": "TW",
        "Tanzania": "TZ",
        "US": "US",
        "Venezuela": "VE",
        "Vietnam": "VN",
        "Syria": "SY",
        "Laos": "LA",
        "West Bank and Gaza": "PS",
        "Kosovo": "XK",
        "Burma": "MM",
        "MS Zaandam": "NL",
        "US": "US"
    }
    if (pycountry.countries.get(name=x)):
        return pycountry.countries.get(name=x).alpha_2
    elif x in country_codes:
        return country_codes[x]
    else:
        return "None"

def country_name3(x):
    country_codes = {
        "Bolivia": "BOL",
        "Brunei": "BRN",
        "Congo (Brazzaville)": "COG",
        "Congo (Kinshasa)": "COK",
        "Cote d'Ivoire": "CIV",
        "Diamond Princess": "GBR",
        "Holy See": "VAT",
        "Iran": "IRN",
        "Korea, South": "KOR",
        "Moldova": "MDA",
        "Russia": "RUS",
        "Taiwan*": "TWN",
        "Tanzania": "TZA",
        "US": "USA",
        "Venezuela": "VEN",
        "Vietnam": "VNM",
        "Syria": "SYR",
        "Laos": "LAO",
        "West Bank and Gaza": "PSE",
        "Kosovo": "XKK",
        "Burma": "MMR",
        "MS Zaandam": "NLD",
        "US": "USA"
    }
    if (x in country_codes):
        return country_codes[x]
    elif (pycountry.countries.get(name=x)):
        return pycountry.countries.get(name=x).alpha_3
    else:
        return "None"

def continent_name(x):
    continents = {
        'NA': 'North America',
        'SA': 'South America',
        'AS': 'Asia',
        'OC': 'Australia',
        'AF': 'Africa',
        'AN': 'Antartica',
        'EU': 'Europe'
    }
    country_codes = {
        "VA" : "Europe"
    }
    if x in country_codes:
        return country_codes["VA"]
    elif x != "N/A":
        return continents[pc.country_alpha2_to_continent_code(x)]
    else:
        return continents["N/A"]



df = pd.read_csv("full-list-total-tests-for-covid-19.csv")

def timestampConversion(x):
    dt = datetime.datetime.strptime(x, "%Y-%m-%d")
    return time.mktime(dt.timetuple())

df['iso_alpha'] = df['Entity'].apply(lambda x: country_name(x))
df = df[df.iso_alpha != 'None']
df['Continent'] = df['iso_alpha'].apply(lambda x: continent_name(x))
df = df[df.Continent != 'None']
df['Date'] = df['Date'].astype(str)
del df['Code']

df["Da"] = pd.to_datetime(df.Date)
df['DOB1'] = df['Da'].dt.strftime('%m-%d-%Y')
del df['Da']
del df['Date']
df['iso_alpha'] = df['Entity'].apply(lambda x: country_name3(x))
df['DOB1'] = df['DOB1'].astype(str)
df['Totaltests'] = df['Total tests']
del df['Total tests']

fig = px.scatter_geo(df, locations="iso_alpha", color="Continent",
                        hover_name="Entity", size="Totaltests",
                        animation_frame="DOB1",
                        opacity=1,
                        projection="natural earth")

fig.show()

app.layout = html.Div([
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)