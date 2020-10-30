$(document).ready(function () {
    $('#update').on('click',function (event) {
        console.log("Updating...");

        const fname = $('#fn').val();
        const lname = $('#ln').val();
        const password = $('#new-pw').val();

        const username = $('#username').val();
        
        $.ajax({
            cache:false,
            data: {
                 'firstname': fname, 
                 'lastname': lname,
                 'password':password,
                 'username':username
             },
             type: 'POST',
             url: '/profile',
             success: data => {
                console.log(data);
                
                if(data == "Nothing Updated"){
                    const msgElem = $('#usrMsg');
                    msgElem.text("Nothing has been updated");
                    msgElem.css("color", "red");
                }else if(data == "Undefined"){
                    const msgElem = $('#usrMsg');
                    msgElem.text("Undefined error, Please contant support");
                    msgElem.css("color", "red");
                }else if(data =="password too short"){
                    const msgElem = $('#usrMsg');
                    msgElem.text("Password Must be 8 characters or longer");
                    msgElem.css("color", "red");
                }else{
                    const msgElem = $('#usrMsg');
                    msgElem.text("Updated " + data + "Successfully!");
                    msgElem.css("color", "green");
                }
             },
             error: (jqXHR, textStatus, errorThrown) => {
                console.log("error");
             }
         });
         event.preventDefault();  
    });
});