import requests
import json
import time

#keuze om hard coded access token te gebruiken of user zelf 1 laten ingeven
keuze = input("Gebruik de hard-coded Webex access token of niet? (y/n)")

if keuze == "n" or keuze == "N":
    accessToken = input("Geef uw token in: ")
    accessToken = "Bearer " + accessToken
else:
    accessToken = "Bearer YmRiOTI1OGQtOThhZC00N2Y3LTlmNzItOTM2MzU0ZDQ2NzZkODBmMTNhODAtMWI4_PF84_consumer"

#get request om de rooms op te vragen vanuit webex teams        
r = requests.get(   "https://api.ciscospark.com/v1/rooms",
                    headers = {"Authorization": accessToken}
                )
#controle op de statuscode
if not r.status_code == 200:
    raise Exception("Incorrect reply from Webex Teams API. Status code: {}. Text: {}".format(r.status_code, r.text))

#lijst van de rooms tonen
print("List of rooms:")
rooms = r.json()["items"]
for room in rooms:
    print (room["title"])

#zoeken van de roomnaam
while True:
    roomNameToSearch = input("In welke kamer wil u BlackJack spelen: ")

    roomIdToGetMessages = None
    
    for room in rooms:
        if(room["title"].find(roomNameToSearch) != -1):

            print ("Gevonden rooms met het woord " + roomNameToSearch)
            print(room["title"])

            roomIdToGetMessages = room["id"]
            roomTitleToGetMessages = room["title"]
            print("Gevonden room : " + roomTitleToGetMessages)
            break

    if(roomIdToGetMessages == None):
        print("Sorry, Ik heb geen room gevonden die" + roomNameToSearch + " bevat.")
        print("Probeer opnieuw aub...")
    else:
        break

# run the "bot" loop until manually stopped or an exception occurred
while True:
    # always add 1 second of delay to the loop to not go over a rate limit of API calls
    time.sleep(1)

    # the Webex Teams GET parameters
    #  "roomId" is is ID of the selected room
    #  "max": 1  limits to get only the very last message in the room
    GetParameters = {
                            "roomId": roomIdToGetMessages,
                            "max": 1
                         }
    # run the call against the messages endpoint of the Webex Teams API using the HTTP GET method
    r = requests.get("https://api.ciscospark.com/v1/messages", 
                         params = GetParameters, 
                         headers = {"Authorization": accessToken}
                    )
    # verify if the retuned HTTP status code is 200/OK
    if not r.status_code == 200:
        raise Exception( "Incorrect reply from Webex Teams API. Status code: {}. Text: {}".format(r.status_code, r.text))

    # get the JSON formatted returned data
    json_data = r.json()
    # check if there are any messages in the "items" array
    if len(json_data["items"]) == 0:
        raise Exception("There are no messages in the room.")

    # store the array of messages
    messages = json_data["items"]
    # store the text of the first message in the array
    message = messages[0]["text"]
    print("Received message: " + message)

    if message == "/blackjack":
        
        #url voor deck of cards api met 6 decks
        deck_url = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=6"

        #variabele voor get request
        deck_count = requests.get(deck_url)
        print("statuscode deck opvragen: " + str(deck_count))

        #json response in een variabele meegeven
        response_json_deck = deck_count.json()
        #print(response_json_deck)

        #deck id uit het antwoord halen en in een variabele meegeven
        deck_id = response_json_deck["deck_id"]
        #print(deck_id)
        #print("Hoeveel kaarten nog: " + str(response_json_deck["remaining"]))

        #variabele om 2 kaarten te trekken gebruik maken van het deck id
        deck_id_url = "https://deckofcardsapi.com/api/deck/"+deck_id+"/draw/?count=2"
        deck_draw = requests.get(deck_id_url)
        print("statuscode 2 kaarten opvragen: " + str(deck_draw))

        #json response in een variabele meegeven
        response_json_draw= deck_draw.json()
        #print(response_json_draw)

        #kaarten uit antwoord halen
        kaarten = []

        #alle waardes overlopen in cards en toevoegen aan de list kaarten
        for i in response_json_draw["cards"]:
            kaart = [
                i["image"],
                i["value"],
                i["suit"],
                i["code"]
                ]

            kaarten.append(kaart)

        #initiele waarde van de kaarten meegeven en bekijken
        print("Kaart A: " + kaarten[0][1])
        kaartA = kaarten[0][1]
        print("Kaart B: " + kaarten[1][1])
        kaartB = kaarten[1][1]

        waardeKaart1 = 0
        waardeKaart2 = 0

        #bekijken welke kaart het is en de waarde eraan toevoegen
        if str(kaartA) == "KING":
            waardeKaart1 = 10
        elif str(kaartA) == "QUEEN":
            waardeKaart1 = 10
        elif str(kaartA) == "JACK":
            waardeKaart1 = 10
        elif str(kaartA) == "ACE":
            waardeKaart1 = 11
        else:
            waardeKaart1 = kaartA

        #bekijken welke kaart het is en de waarde eraan toevoegen
        if str(kaartB) == "KING":
            waardeKaart2 = 10
        elif str(kaartB) == "QUEEN":
            waardeKaart2 = 10
        elif str(kaartB) == "JACK":
            waardeKaart2 = 10
        elif str(kaartB) == "ACE":
            waardeKaart2 = 11
        else:
            waardeKaart2 = kaartB

        print("Waarde van de kaarten na controle:")    
        print("Kaart 1: " + str(waardeKaart1))
        print("Kaart 2: " + str(waardeKaart2))

        #optellen waarde van de kaarten
        totaleWaarde = int(waardeKaart1) + int(waardeKaart2)
        print("Totale waarde: " + str(totaleWaarde))

        #commando's uitleg voor blackjack
        welkom = "Welkom bij de versie van BlackJack gemaakt door Gianni Bouckaert. \n\n"
        blackjack = "Typ /blackjack om opnieuw te starten. \n"
        trekkaart = "Typ /trekkaart om een nieuwe kaart te trekken. \n"
        shuffle = "Typ /shuffle om een shuffle van de decks uit te voeren. \n\n"

        #totale waarde controleren en sturen naar de chat
        if totaleWaarde == 21:
            print("BLACKJACK!")
            responseMessage = welkom + blackjack + trekkaart + shuffle + "De waarde van uw kaarten is " + str(totaleWaarde) + ". BLACKJACK!"
        elif totaleWaarde > 21:
            print("U hebt verloren")
            responseMessage = welkom + blackjack + trekkaart + shuffle + "De waarde van uw kaarten is " + str(totaleWaarde) + ". U hebt verloren."
        elif totaleWaarde < 21:
            print("Trek nog een kaart of stop met spelen")
            responseMessage = welkom + blackjack + trekkaart + shuffle + "De waarde van uw kaarten is " + str(totaleWaarde) + ". Trek nog een kaart of stop met spelen."

        HTTPHeaders = { 
                             "Authorization": accessToken,
                             "Content-Type": "application/json"
                           }
        PostData = {
                            "roomId": roomIdToGetMessages,
                            "text": responseMessage
                        }

        r = requests.post( "https://api.ciscospark.com/v1/messages", 
                              data = json.dumps(PostData), 
                              headers = HTTPHeaders
                         )
        if not r.status_code == 200:
            raise Exception("Incorrect reply from Webex Teams API. Status code: {}. Text: {}".format(r.status_code, r.text))

    elif message == "/trekkaart":
        #variabele om 2 kaarten te trekken gebruik maken van het deck id
        deck_id_url = "https://deckofcardsapi.com/api/deck/"+deck_id+"/draw/?count=1"
        deck_draw = requests.get(deck_id_url)
        print("statuscode 1 kaart opvragen: " + str(deck_draw))

        #json response in een variabele meegeven
        response_json_draw= deck_draw.json()
        #print(response_json_draw)

        #kaarten uit antwoord halen
        kaarten = []

        #alle waardes overlopen in cards en toevoegen aan de list kaarten
        for i in response_json_draw["cards"]:
            kaart = [
                i["code"],
                i["image"],
                i["images"],
                i["value"],
                i["suit"]
                ]

            kaarten.append(kaart)

        #initiele waarde van de kaarten meegeven en bekijken
        print("Kaart C: " + kaarten[0][3])
        kaartA = kaarten[0][3]

        waardeKaart1 = 0

        #bekijken welke kaart het is en de waarde eraan toevoegen
        if str(kaartA) == "KING":
            waardeKaart1 = 10
        elif str(kaartA) == "QUEEN":
            waardeKaart1 = 10
        elif str(kaartA) == "JACK":
            waardeKaart1 = 10
        elif str(kaartA) == "ACE":
            if totaleWaarde == 11:
                waardeKaart1 = 1
            else:
                waardeKaart1 = 11
        else:
            waardeKaart1 = kaartA

        print("Waarde van de kaarten na controle:")    
        print("Kaart 1: " + str(waardeKaart1))

        #optellen waarde van de kaarten
        totaleWaarde = totaleWaarde + int(waardeKaart1)
        print("Totale waarde: " + str(totaleWaarde))

        #totale waarde controleren en sturen naar de chat
        if totaleWaarde == 21:
            print("BLACKJACK!")
            responseMessage = "De waarde van uw kaarten is " + str(totaleWaarde) + ". BLACKJACK!"
        elif totaleWaarde > 21:
            print("U hebt verloren")
            responseMessage = "De waarde van uw kaarten is " + str(totaleWaarde) + ". U hebt verloren."
        elif totaleWaarde < 21:
            print("Trek nog een kaart of stop met spelen")
            responseMessage = "De waarde van uw kaarten is " + str(totaleWaarde) + ". Trek nog een kaart of stop met spelen."

        HTTPHeaders = { 
                             "Authorization": accessToken,
                             "Content-Type": "application/json"
                           }
        PostData = {
                            "roomId": roomIdToGetMessages,
                            "text": responseMessage
                        }

        r = requests.post( "https://api.ciscospark.com/v1/messages", 
                              data = json.dumps(PostData), 
                              headers = HTTPHeaders
                         )
        if not r.status_code == 200:
            raise Exception("Incorrect reply from Webex Teams API. Status code: {}. Text: {}".format(r.status_code, r.text))
        
    elif message == "/shuffle":
        #shuffle link
        shuffle_url = "https://deckofcardsapi.com/api/deck/"+deck_id+"/shuffle/"

        deck_shuffle = requests.get(shuffle_url)
        print("shuffle van het deck: " + str(deck_shuffle))

        #json response in een variabele meegeven
        response_json_shuffle= deck_shuffle.json()
        print(response_json_shuffle)

        
        
        

    




