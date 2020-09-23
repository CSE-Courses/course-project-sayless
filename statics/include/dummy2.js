$(document).ready(function () {
    $('#registerForm').submit(function () {
    
        const fname = $('#fname').val();
        const lname = $('#lname').val();
        const email = $('#emailInput').val();
        const password = $('#p').val();
        const requestData2 = {'email': email, 'password': password,'f':fname,'l':lname};
    
        $.ajax({
            type: "POST",
            url: "/signup",
            cache: false,
            data: requestData2,
            success: data => {    
                // check what kind of error is it. 
                if(data == None){
                    console.log("failureeeee.......")
                }else{
                    console.log("success");
            }
        }
        });
    
    
        preventDefault();  
    });
});