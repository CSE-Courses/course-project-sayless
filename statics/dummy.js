$(document).ready(function () {
    $('#loginForm').submit(function () {
    
        const email = $('#emailInput').val();
        const password = $('#passwordInput').val();

        const requestData = {'email': email, 'password': password};
    
        $.ajax({
            type: "POST",
            url: "/login",
            cache: false,
            data: requestData,
            success: data => {    
                // check what kind of error is it. 
                if(data == "user_and_email_not_found"){
                    console.log("username or email not found");

                    const msgElem = $('#usrMsg');
                    msgElem.text("Email has not been registered. Please register the email address");
                    msgElem.css("color", "red");
    
                    document.getElementById("passwordInput").value = "";
    
                    // window.location.pathname = "/home/messages";
    
                }else if(data == "Success"){
                    console.log("Success");
                    window.location.pathname = "/";
    
                }else if(data == "invalid_password"){

                    console.log("Invalid Password");

                    const msgElem = $('#usrMsg');
                    msgElem.text("Invalid Password");
                    msgElem.css("color", "red");
    
                    document.getElementById("passwordInput").value = "";
                }else if(data == "error"){
                    console.log("Error! Please contact support");
                }
            },
            error: (jqXHR, textStatus, errorThrown) => {
                const message = jqXHR.responseJSON['message'];
                const msgElem = $('#usrMsg');
                msgElem.text(message);
                msgElem.css("color", "red");
            }
        });
    
    
        return false;
    });
});