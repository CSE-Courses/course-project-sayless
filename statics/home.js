$(document).ready(function () {
    $('#autocomplete-3').on('input', function() {
  
        const username = $('#autocomplete-3').val();
        const requestData = {'username': username };
      
        if(username != ""){
            $.ajax({
                type: "POST",
                url: "/search",
                cache: false,
                data: requestData,
                success: data => {   
                    $( "#autocomplete-3" ).autocomplete({
                        //can change this to what we want. 1 DOES NOT DO ANYTHING
                        minLength:0,   
                        delay:500,   
                        source: data
                    });
                }
            })
        }
    });

    $('#usersearch').submit(function () {
    
        const name = $('#autocomplete-3').val();

        const requestData = {'username': name};
    
        $.ajax({
            type: "POST",
            url: "/homepage",
            cache: false,
            data: requestData,
            success: data => {    
                // check what kind of error is it. 
                if(data["Success"]){
                    console.log("Success");
                    window.location.pathname = "/chat/"+data["Success"];
    
                } else if(data["Invalid_user"] ){

                    console.log("Invalid user");

                    const msgElem = $('#truth');
                    msgElem.text("username does not exist");
                    msgElem.css("color", "red");
    
                    document.getElementById("search").value = "";
                 }else if(data["Cannot_Talk"] ){

                    console.log("Talking to user: " + data['Cannot_Talk'] + " Failed.");

                    const msgElem = $('#truth');
                    msgElem.text("Cannot talk to user: " + data['Cannot_Talk']);
                    msgElem.css("color", "red");
    
                    document.getElementById("search").value = "";
                 }else{
                    console.log("Error! Please contact support");
                }
            },
            error: (jqXHR, textStatus, errorThrown) => {
               console.log("error");
            }
        });
    
    
        return false;
    });
});
