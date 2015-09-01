#! /usr/bin/python
import json, time
import phue

def application(environ, start_response):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    body = environ['wsgi.input'].read(request_body_size)
    # extract the id. Currently this is done positionally
    id = str(body)[6:22]

    b = phue.Bridge('hueBridge')

    # If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
    b.connect()

    # lights = b.lights

    f = open("/home/jkeane/bin/huePy/dash_request.txt", "w")
    # f.write(str(body)+"\n")

    f.write("id: "+id+"\n")


    if id == "G030G00552625062":
        lights = {"Living northeast": None,
                  "Living southwest": None,
                  "Living northwest": None,
                  "Living southeast": None,
                  "Front door": None}

        for light in lights:
            if b.get_light(light, 'on') == True and b.get_light(light, 'bri') > 100:
                lights[light] = "bright"
            elif b.get_light(light, 'on') == False:
                lights[light] = "off"
            else:
                lights[light] = "dark"

        numBright = sum(lightState == "bright" for lightState in lights.values())
        numOff = sum(lightState == "off" for lightState in lights.values())

        f.write(str(lights)+"\n")
        if time.localtime().tm_hour > 3  and time.localtime().tm_hour < 22:
        # Day: if the time is between 3.00 and 22.00, brighten the lights if less than 3 of them are bright. Otherwise turn lights off.
            if numBright < 3:
                b.set_light(lights, 'on', True)
                b.set_light(lights, 'bri', 254)
                b.set_light(lights, 'sat', 0)
            else:
                b.set_light(lights, 'on', False)
                # If this is set (or a transition time is set) The brightness behaves erratically
                # b.set_light(lights, 'bri', 1)
        else:
        # Overnight: if the time is between 22.00 and 3.00, brighten the lights more than 4 of them are off. Otherwise turn lights off.
            if numOff > 4:
                b.set_light(lights, 'on', True)
                b.set_light(lights, 'bri', 254)
                b.set_light(lights, 'sat', 0)
            else:
                b.set_light(lights, 'on', False)
                # If this is set (or a transition time is set) The brightness behaves erratically
                # b.set_light(lights, 'bri', 1)

    if id == "G030G00553170740":
        lights = {"Iris bedroom": None,
                  "Bedroom hall": None}

        # currently bright isn't used here, maybe thi shsould be separated out to a generic function
        for light in lights:
            if b.get_light(light, 'on') == True and b.get_light(light, 'bri') > 100:
                lights[light] = "bright"
            elif b.get_light(light, 'on') == False:
                lights[light] = "off"
            else:
                lights[light] = "dark"

        numBright = sum(lightState == "bright" for lightState in lights.values())
        numOff = sum(lightState == "off" for lightState in lights.values())

        f.write(str(lights)+"\n")
        if numOff >= 2:
            # if both are off, only turn on the iris.
            b.set_light("Iris bedroom", 'on', True)
            b.set_light("Iris bedroom", 'bri', 103)
            # b.set_light(lights, 'sat', 0)
        else:
            # if either are on, turn both off.
            b.set_light(lights, 'on', False)
            # If this is set (or a transition time is set) The brightness behaves erratically
            # b.set_light(lights, 'bri', 1)


    f.close()

    start_response('200 OK', [('Content-Type', 'text/html')])
    return ["<h1>This should be sent to a dash!</h1>"]
