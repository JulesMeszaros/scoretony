import json
import requests
from googleapiclient.discovery import build

api_key = "AIzaSyCvy97f3FqXlH90PHQ5wK4y4EDRQvoVwm4"
jsonpath = ""

youtube = build('youtube', 'v3', developerKey=api_key)
uploadsID = "UUkUq-s6z57uJFUBvZIVTyg" 

def parsePage(data):
    """Prend en paramètre un dictionnaire et retourne une liste. 
    S'applique pour chaque pages et determine pour chaque video de la page si elle doit etre gardée (cad telecharger 
    la vignette, et ajouter les informations de la video à un dossier JSON"""
    
    #Liste qui contiendra des dictionnaires comportant des informations sur les reviews de la page sur laquelle on travaille.
    #Cette liste sera ensuite fusionnée avec une liste globale qui contiendra les dictionnaires de tous les albums.
    
    pageData = []
    
    videos = data["items"]
    
    for video in videos:
        title = video["snippet"]["title"]
        if (title.endswith('ALBUM REVIEW')):
            newdata = parseVideo(video)
            if newdata != {}:
                pageData.append(newdata)
            
    return(pageData)

def parseVideo(data):
    """Prend en paramètre un dictionnaire et retourne un dictionnaire.
    Traite les données d'un album pour l'ajouter à la database de reviews"""
    videoTitle = data["snippet"]["title"]
    cleanTitle = videoTitle[:-13]
    
    albumTitle = ""
    albumArtist = ""
    
    #on créé un dictionnaire propre à cette review, qui contient ses informations et 
    #qui sera ensuite ajouté à une liste dans la fonction parsePage
    
    datas = {}
    
    if(len(cleanTitle.split('- ')) == 2):
        albumTitle = cleanTitle.split('- ')[1]
        albumArtist = cleanTitle.split('- ')[0]
        while(albumTitle.endswith(" ")):
            albumTitle = albumTitle[:-1]
        while(albumArtist.endswith(" ")):
            albumArtist = albumArtist[:-1]
           
        score = getScore(data["snippet"]["description"])
        
        if(score in "12345678910" and score != ""):
        
            
            #Ici on utilise les données données par l'API pour creer des variables du dictionnaire de la review
            datas['titre'] = albumTitle
            datas['artiste'] = albumArtist
            datas['note'] = score
            #Cette variable sera le nom du fichier image contenant la vignette de la vidéo. On utilise l'ID de la vidéo car celui-ci est
            #Simple à formatter et est unique donc ne posera pas de problèmes de doublons. (j'écrie ces lignes défoncé désolé si c'est pas clair)
            datas['vignette'] = data["snippet"]["resourceId"]["videoId"]
            
            imgpath = "data/vignettes/{}.png".format(data["snippet"]["resourceId"]["videoId"])
           
            img_data = ""
            
            if("standard" in data["snippet"]["thumbnails"]):
            
                img_data = requests.get(data["snippet"]["thumbnails"]["standard"]["url"]).content
            
            else:
            
                img_data = requests.get(data["snippet"]["thumbnails"]["high"]["url"]).content
            
            with open(imgpath, 'wb') as handler:
                handler.write(img_data)
            
            print(albumTitle)
        
        else:
            
            print(score)
        
        
        #print(datas)
        return(datas)

def getScore(description):
    descriptionSplit = description.split("/10")
    score = ""
    if(len(descriptionSplit) == 2):
        #On split la première partie pour prendre le dernier mot qui est normalement la note sur 10
        firstpart = descriptionSplit[0].split("\n")
        score = firstpart[len(firstpart) -1]
        
        
    return score


"""Début du script:
On créé d'abord une variable de data qui sera envoyée dans le fichier JSON, puis on effectue une première requette pour la premiere
page de resultats. Une boucle est ensuite effectuée pour chaque pages de resultats.
A chaque occurence de la boucle on ajoute les données récupérées à la variable jsonData avant finalement de l'envoyer au fichier datas.json
"""
jsonData = {}
jsonData['reviews'] = []

request = youtube.playlistItems().list(
        part="snippet",
        maxResults=50,
        playlistId="UUt7fwAhXDy3oNFTAzF2o8Pw",
    )

jsonData['reviews'] += parsePage(request.execute()) 

resultPageToken = request.execute()['nextPageToken']

while("nextPageToken" in request.execute()):
    request = youtube.playlistItems().list(
        part="snippet",
        maxResults=50,
        pageToken=resultPageToken,
        playlistId="UUt7fwAhXDy3oNFTAzF2o8Pw"
    )
    
    jsonData['reviews'] += parsePage(request.execute()) 
    
    if("nextPageToken" in request.execute()):
        resultPageToken = request.execute()['nextPageToken']

with open('data/datas.json', 'w') as outfile:
    json.dump(jsonData, outfile)