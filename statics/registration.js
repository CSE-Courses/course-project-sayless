$(document).ready(function () {
    $('#registerForm').on('submit',function (event) {
        console.log("button work");
        const fname = $('#fname').val();
        const lname = $('#lname').val();
        const email = $('#emailInput').val();
        const password = $('#password').val();
        const username = $('#username').val();
        const confirm = $('#password2').val();
    
        $.ajax({
           cache:false,
            data: {
                'email': email, 
                'password': password,
                'fname':fname,
                'lname':lname,
                'username':username,
                'confirm' :confirm
            },
            type: 'POST',
            url: '/signup',
            success: data => {
                // check what kind of error is it. 
                if (data == "email exists"){
                    const msgElem = $('#usrMsg');
                    msgElem.text("Email already exists");
                    msgElem.css("color", "red");
                }else if(data == "password too short"){
                    const msgElem = $('#usrMsg');
                    msgElem.text("Password Must be 8 characters or longer");
                    msgElem.css("color", "red");
                }else if( data == "username exists"){
                    const msgElem = $('#usrMsg');
                    msgElem.text("Username already exists");
                    msgElem.css("color", "red");
                }else if( data == "password does not match"){
                    const msgElem = $('#usrMsg');
                    msgElem.text("Password does not match");
                    msgElem.css("color", "red");
                }
                else if(data == "success"){
                    window.location.pathname = "/";
                    console.log(data);
                }else if(data == "Please fill out every field"){
                    const msgElem = $('#usrMsg');
                    msgElem.text("You are required to fill out every field");
                    msgElem.css("color", "red");
                }else if(data == "Invalid email"){
                    const msgElem = $('#usrMsg');
                    msgElem.text("Invalid email");
                    msgElem.css("color", "red");
                }else{
                    console.log(data);
                    const msgElem = $('#usrMsg');
                    msgElem.text("Unknown error.. please contact admin staff");
                    msgElem.css("color", "red");
                }
            },
            error: (jqXHR, textStatus, errorThrown) => {
               console.log("error");
            }
        });
        event.preventDefault();  
    });
});