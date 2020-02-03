from flask import Flask, request
from math import radians, cos, sin, asin, sqrt

app = Flask(__name__)


@app.route('/countsTweets', methods=['GET', 'POST'])
def countsTweets():

    # Se obtendra como parametro el tiempo de consulta, este servira para ocnsumir el historial de tweets, por default será el dia actual.
    consulTime = request.get_json()["historyTime"] # dias

    #Se obtendra como parametro la cordenada centro que determinara de donde parten los tweets.
    center_point = request.get_json()["cordinate"]

    #Se obtendra como parametro la distancia a considerar despues del punto, por default será de 1 km
    radius = request.get_json()["radius"]  # in kilometer

    print("consulTime: ", consulTime)
    print("cordinate: " , center_point)
    print("radius: " , radius)


    #En esta sección se obtendran todos los datos de los tweets, se considera una base de datos no SQL, por el tipo de formato de los tweets (Propuesta MongoDB)
    #Ejemplo de coordenadas (se debe obtener de la base de datos no sql )
    test_point = [{'lat': -17.79457, 'lng': 110.36563},
                  {'lat': 8.79457, 'lng': 14.36563},
                  {'lat': -7.79457, 'lng': 120.36563},
                  {'lat':-10.79456, 'lng':  11.36562},
                  {'lat': 7.79457, 'lng': 10.36563},
                  {'lat':-10.79457, 'lng':  11.36563},
                  {'lat': 17.79457, 'lng': 9.36563},
                  {'lat': -7.79457, 'lng': 110.36563}]

    #En este proceso se usara concurrencia para obtener la cantidad de tweets , por tiempo solo se utilizara un loop

    lat1 = center_point[0]['lat']
    lon1 = center_point[0]['lng']

    listTweets = []

    for coordinateExample in test_point:
        lat2 = coordinateExample['lat']
        lon2 = coordinateExample['lng']
        inside, idTweet = isInside(lon1, lat1, lon2, lat2,radius)
        if inside:
            listTweets.append(idTweet)


    return "Los tweets a 1 km son: "+str(len(listTweets))




def isInside(lon1, lat1, lon2, lat2, radius = 1, idTweet = "xx"):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles

    a = c * r

    print('Distance (km) : ', a)

    if a <= radius:
        print("inside of area")
        return (True, idTweet)
    else:
        # print("outside of area")
        return (False, idTweet)



if __name__ == '__main__':
    app.run()
