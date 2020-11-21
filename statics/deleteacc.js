$(document).ready(function () {
    $('#del').submit(function () {
    
        $.ajax({
            type: "POST",
            url: "/deleteacc",
            cache: false,
            data: {},
            success: data => {    
                // check what kind of error is it. 
                if (data == "success") {
                    window.location.pathname = "/login"
                }
            },
        });
    
    
        return false;
    });
});