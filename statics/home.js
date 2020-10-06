window.onload = function() {
  
  const email = localStorage.getItem("Email");
  const requestData = {'email': email };

  $.ajax({
    type: "POST",
    url: "/",
    cache: false,
    data: requestData,
    success: data => {   
      //Upon Return success, we should have all other CURRENT usernames in an array
      //Now we can use them to load into the page allowing users to select who to start a chat with
      console.log(data);
    }

})

}