import json
import urllib.request

from sys import exit

def getLongWeather():
  forecastJson = urllib.request.urlopen("https://api.weather.gov/gridpoints/BMX/86,27/forecast").read() 

  forecastParsed = json.loads(forecastJson)
  #print(forecastParsed)
  forecastPeriods = forecastParsed["properties"]["periods"]
  #print(forecastPeriods)

  longWeather = ""

  for period in forecastPeriods:
  # each period has:
  #  number, name, startTime, endTime, isDaytime, temperature, temperatureUnit,
  #  temperatureTrend, windSpeed, windDirection, icon, shortForecast, 
  #  and detailedForecast
    #print(period)
    name = period["name"] + ": "
    temperature = str(period["temperature"]) + period["temperatureUnit"] + ", "
    wind = "wind " + period["windSpeed"] + " " + period["windDirection"] + ", "
    shortForecast = period["shortForecast"] + " "
    periodWeather = name + temperature + wind + "\n" + shortForecast + "\n"
    longWeather = longWeather + periodWeather

  return longWeather

def getShortWeather():
  forecastJson = urllib.request.urlopen("https://api.weather.gov/gridpoints/BMX/86,27/forecast").read()

  forecastParsed = json.loads(forecastJson)
  #print(forecastParsed)
  forecastPeriods = forecastParsed["properties"]["periods"]
  #print(forecastPeriods)

  weatherCurrent = forecastPeriods[0]
  name = weatherCurrent["name"]
  temperature = str(weatherCurrent["temperature"]) + weatherCurrent["temperatureUnit"]
  shortForecast = weatherCurrent["shortForecast"]
  
  shortWeather = name + ": " + temperature + " high, " + shortForecast
  return shortWeather

def main():
  print(getLongWeather())
  print(getShortWeather())

if __name__ == "__main__":
  import sys
  try: 
    main()

  except Exception as e:
    sys.stderr.write("unexpected error %s" % e)
    sys.exit(1)

  except:
    sys.exit(0)

