//Function for search Bar, on key press by user will
//Contact database and get results that match with the users input

$(document).ready(function () {
$('#automplete-3').on('input', function() {
  
  const username = $('#automplete-3').val();
  const requestData = {'username': username };

  if(username != ""){
  $.ajax({
    type: "POST",
    url: "/",
    cache: false,
    data: requestData,
    success: data => {   
      $( "#automplete-3" ).autocomplete({
        //can change this to what we want. 1 DOES NOT DO ANYTHING
        minLength:0,   
        delay:500,   
        source: data
     });
    }
})
}
});

//On submit of username to start chat, if the user name is valid start the chat stuff
  $('#search_form').submit(function (e) {
    e.preventDefault();

    const username = $('#automplete-3').val();
    const requestData = {'username': username };

  $.ajax({
    type: "POST",
    url: "/username_validity",
    cache: false,
    data: requestData,
    success: data => {   
    if(data == "invalid_username"){
      //change if you dont like alerts
      alert("Username is not valid, Please enter a valid username!")
    }
    else if(data == "valid_username"){
      // Here is where the chat stuff would take over
      console.log("valid");
    }
    else{
      alert("Unknown error.. please contact admin staff");
    }
  }
  });

  });
});