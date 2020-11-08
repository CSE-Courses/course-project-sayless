
$(document).ready(function () {
    var x = document.getElementsByClassName("token")[0].id;
    var u = document.getElementsByClassName("user")[0].id;
    $('#reset').on('submit',function (event) {
        const password = $('#password').val();
        const confirm = $('#password2').val();
        const user_id= u;
        
        $.ajax({
            cache:false,
             data: {
                 'password': password,
                 'confirm' :confirm,
                 'user_id' :user_id
             },
             type: 'POST',
             url: '/reset_pass/' + x,
             success: data => {
                if(data == "Success"){ 
                    const msgElem = $('#usrMsg');
                    msgElem.text("Password Has Been Changed, Please return to login page.");
                    msgElem.css("color", "green");
                 console.log(data);
                 }else if(data == "password does not match"){
                    const msgElem = $('#usrMsg');
                    msgElem.text("Password does not match");
                    msgElem.css("color", "red");
                 }else if(data == "password too short"){
                    const msgElem = $('#usrMsg');
                    msgElem.text("Password Must be 8 characters or longer");
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
        return false; 
    });
});