//Upon submitting an email, send it to the back end, if its valid send em an email
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
                    }
                }
            })

    });

document.getElementById('resetEmail').val = "";
return false;



});