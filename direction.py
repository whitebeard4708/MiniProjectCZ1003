import googlemaps
import datetime

gmaps = googlemaps.Client(key= 'AIzaSyD7UsgHTKortN9wRHK13_OFtiX9VRWf2ss')
now = datetime.datetime.now()
#convert from pixel on the NTU Campus map to latitudes and longitudes
def pixeltolatlng(x,y):
    lat = 1.356116549 - 0.000026134*y
    lng = 103.676118654 + 0.000015694*x
    return (lat,lng)

#get walking distance from address 1 to address 2
#def get_distance(address1, address2):
#    distance_matrix = gmaps.distance_matrix(address1, address2, 'walking')
#    elements = distance_matrix['rows'][0]['elements']
#    #get distance
#    distance = elements[0]['distance']['value'] #in meters
#    #get distance in kilometers
#    distance /= 1000
#    return distance

#get the directions from google map
#There are threee selected modes: 'walking', 'driving', 'transit' (meaning there are three ways to implement)
def get_directions(address1, address2, mode):
    directions_result = gmaps.directions(address1,\
    address2, mode = mode, departure_time = now)
    return directions_result

#get the steps(not transit) (meaning not using bus)
def get_steps_not_transit(directions):
    steps =  directions[0]['legs'][0]['steps']
    #create a list of [{'direction':....,'duration':...,'distance':...} ]
    lst_of_steps = []
    i = 0
    for step in steps:
        lst_of_steps.append({})
        lst_of_steps[i]['direction'] = step['html_instructions'].replace('</b>','').replace('<b>','').\
          replace('</div>','').replace('<div style="font-size:0.9em">','. ')
        #print the duration of the instructions
        lst_of_steps[i]['duration'] = str(step['duration']['value']//60) +' minutes ' + str(step['duration']['value']%60) +' seconds'
        #print the distance of the instructions
        lst_of_steps[i]['distance'] = step['distance']['text']
        i += 1
    return lst_of_steps

#get the steps (transit) (meaning maybe using bus (or not))
def get_steps_transit(directions):
    #in case there is no directions, but actually there are always directions!!!
    if directions != []:
        #create a list of [{'direction':....,'duration':...,'distance':...} ]
        lst_of_steps = []
        i = 0
        steps = directions[0]['legs'][0]['steps']
        for step in steps:
            lst_of_steps.append({})
            if step['travel_mode'] == 'TRANSIT':
                details = step['transit_details']
                lst_of_steps[i]['direction'] = 'Take ' + details['line']['agencies'][0]['name'] +' from'+\
                      details['departure_stop']['name']+' to'+ details['arrival_stop']['name']
            else:
                #just cleaning the data from google maps html
                lst_of_steps[i]['direction'] = step['html_instructions'].replace('</b>','').replace('<b>','').\
                      replace('</div>','').replace('<div style="font-size:0.9em">','. ')
            #print the duration of the instructions
            lst_of_steps[i]['duration'] = str(step['duration']['value']//60) + 'minutes ' + str(step['duration']['value']%60) +'seconds'
            #print the distance of the instructions
            lst_of_steps[i]['distance'] = step['distance']['text']
            i += 1
    return lst_of_steps
#x = float(input('x?: '))
#y = float(input('y?: '))
#geocode1 = pixeltolatlng(x,y)
#print(geocode1)
#print_directions_transit(directions)
#print_duration_and_time(directions)
