$(document).ready(function () {
    $('#usersearch').submit(function () {
    
        const name = $('#search').val();

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
