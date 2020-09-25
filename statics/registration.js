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
            url: '/signup'
        })
        .done(function(data){    
                // check what kind of error is it. 
                console.log("hdhdhd");
                if (data == "email exists"){
                    const msgElem = $('#usrMsg');
                    msgElem.text("email already exists");
                    msgElem.css("color", "red");
                }else if(data == "password too short"){
                    const msgElem = $('#usrMsg');
                    msgElem.text("password Must be 8 characters or longer");
                    msgElem.css("color", "red");
                }else if( data == "username exists"){
                    const msgElem = $('#usrMsg');
                    msgElem.text("Username already exists");
                    msgElem.css("color", "red");
                }else if( data == "password does not match"){
                    const msgElem = $('#usrMsg');
                    msgElem.text("password does not match");
                    msgElem.css("color", "red");
                }
                else{
                window.location.pathname = "/";
                console.log(data);
                }
        
        });
    
    
        event.preventDefault();  
    });
});