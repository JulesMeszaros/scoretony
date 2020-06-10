/*QUIZZTHONTY SCORETANO
A QUARANTINE PROJECT BY JULES MESZAROS (@DJNETSCAPE_)*/


var score
var nbr_vies
//On récupère les données du document JSON dans un array "reviews"
//pour pouvoir les exploiter plus tard
reviews = []
//On créé un autre array qui ne contiendra qu'une review et qui sera à chaque
//fois tirée au hasard
current_review = []

$( document ).ready(function() {

});

$.getJSON( "data/datas.json", function( data ) {
  reviews = data["reviews"]
  initGame()
});

$(document).on ("click", ".choix-bouton", function () {
  answer = $(this).attr("answer")
  //Verifie si la réponse est bonne puis déclanche une fonction dépendante du résultat
  if(answer == current_review[2]){
    winRound()
  } else {
    looseRound()
  }
});

function initGame(){
  score = 0
  nbr_vies = 10
  updateInfos()
  newRound()
}

function getRandomReview(){
  var item = reviews[Math.floor(Math.random() * reviews.length)];
  current_review = [item["titre"], item["artiste"], item["note"], item["vignette"]]

  $('#album-title').text(current_review[0]);
  $('#album-artist').text(current_review[1]);

  vignette_path = "data/vignettes/" + current_review[3] + ".png"

  $("#vignette-image").attr("src", vignette_path);
}

function updateInfos(){
  $("#points-info").html(score)
  $("#vies-info").html(nbr_vies)
}

function winRound(){
  score +=1
  console.log("vrai")
  updateInfos()
  newRound()
}

function looseRound(){
  nbr_vies -=1
  console.log("faux")
  if(nbr_vies == 0){
    //Déclanche le game over
    newRound()
    updateInfos()

  } else {
    //Commence un nouveau round
    newRound()
    updateInfos()
  }
}

function newRound(){
  //Prend une review au hasard
  getRandomReview()

  //Choisis 4 notes dont 3 au hasard et une juste, les randomize
  possible_choices = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
  possible_choices.splice(possible_choices.indexOf(current_review[2]), 1)
  choices = [current_review[2]]

  for (i = 0; i < 3; i++){
    //prend un element random de la liste possible_choices
    random_el = possible_choices[Math.floor(Math.random() * possible_choices.length)];
    choices.push(random_el)
    //retire l'element choisis
    possible_choices.splice(possible_choices.indexOf(random_el), 1)
  }
  //randomize l'array
  shuffle(choices)

  //pour chaqun des boutons, on modifie le text ainsi que la valeur de l'attribu 'answer'
  $("#bouton-1").attr("answer", choices[0])
  $("#bouton-2").attr("answer", choices[1])
  $("#bouton-3").attr("answer", choices[2])
  $("#bouton-4").attr("answer", choices[3])

  //on change maintenant le contenu du bouton (le text)
  $("#bouton-1").html(choices[0])
  $("#bouton-2").html(choices[1])
  $("#bouton-3").html(choices[2])
  $("#bouton-4").html(choices[3])


}

function shuffle(array) {
  //Viens de stack overflow mdr
  var currentIndex = array.length, temporaryValue, randomIndex;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {

    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array;
}
