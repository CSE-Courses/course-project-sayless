$(document).ready(function () {
    $('#registerForm').on('submit',function (event) {
    
        const fname = $('#fname').val();
        const lname = $('#lname').val();
        const email = $('#emailInput').val();
        const password = $('#p').val();
    
        $.ajax({
           cache:false,
            data: {
                'email': email, 
                'password': password,
                'fname':fname,
                'lname':lname
            },
            type: 'POST',
            url: '/signup'
        })
        .done(function(data){    
                // check what kind of error is it. 
                if (data == "email exists"){
                    const msgElem = $('#usrMsg');
                    msgElem.text("email already exists");
                    msgElem.css("color", "red");
                }else{
                window.location.pathname = "/";
                console.log(data);
                }
        
        });
    
    
        event.preventDefault();  
    });
});