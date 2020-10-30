//Upon submitting an email, send it to the back end, if its valid (as in it is in the databse) send em an email
//if not just do nothing and display the same message
$(document).ready(function () {
    $('#resetForm').submit(function () {
        const email = $('#resetEmail').val();
        const requestData = {'email': email };
      
            $.ajax({
                type: "POST",
                url: "/reset_request",
                cache: false,
                data: requestData,
                success: data => {   
                    if(data == "Success"){
                  console.log(data);
                    const msgElem = $('#usrMsg');
                    msgElem.text("If email is valid,an email with instructions will be sent shortly");
                    msgElem.css("color", "green");
                 console.log(data);
                    }
                    else{
                        console.log(data)
                        const msgElem = $('#usrMsg');
                        msgElem.text("Unknown error.. please contact admin staff");
                        msgElem.css("color", "red");
                    }
                }
            })

    });
//FOR SOME REASON IT STILL FEELS THE NEED TO REFRESH THE PAGE ON SUBMIT
//REMOVES THE TEXT LETING THE USER KNOW ABOUT
document.getElementById('resetEmail').val = "";
return false;



});