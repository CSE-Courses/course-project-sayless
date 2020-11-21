$(document).ready(function () {
    $('#del').submit(function () {
    
        $.ajax({
            type: "POST",
            url: "/delete",
            cache: false,
            data: {},
            success: data => {    
                // check what kind of error is it. 
                if (data == "success") {
                    console.log("Moulid yooo:.......")
                    window.location.pathname = "/login"
                }
            },
        });
    
    
        return false;
    });
});