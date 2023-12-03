from enum import Enum

class Airlines(Enum):
    AEROLINEAS_ARGENTINAS = "Aerolineas Argentinas"
    AEROMEXICO = "Aeromexico"
    AIR_CANADA = "Air Canada"
    AIR_FRANCE = "Air France"
    ALITALIA = "Alitalia"
    AMERICAN_AIRLINES = "American Airlines"
    AUSTRAL = "Austral"
    AVIANCA = "Avianca"
    BRITISH_AIRWAYS = "British Airways"
    COPA_AIR = "Copa Air"
    DELTA_AIR = "Delta Air"
    GOL_TRANS = "Gol Trans"
    GRUPO_LATAM = "Grupo LATAM"
    IBERIA = "Iberia"
    JETSMART_SPA = "JetSmart SPA"
    K_L_M = "K.L.M."
    LACSA = "Lacsa"
    LATIN_AMERICAN_WINGS = "Latin American Wings"
    OCEANAIR_LINHAS_AEREAS = "Oceanair Linhas Aereas"
    PLUS_ULTRA_LINEAS_AEREAS = "Plus Ultra Lineas Aereas"
    QANTAS_AIRWAYS = "Qantas Airways"
    SKY_AIRLINE = "Sky Airline"
    UNITED_AIRLINES = "United Airlines"

class FlightTypes(Enum):
    I = "I"
    N = "N"

class Months(Enum):
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    ELEVEN = "11"
    TWELVE = "12"

class DayTime(Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    NIGHT = "night"