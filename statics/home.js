$(document).ready(function () {

    $.ajax({
        type: "POST",
        url: "/openchats",
        cache: false,
        data: "",
        success: data => {   
            //console.log(data);

            Object.entries(data).forEach(([key, value]) => {
                //console.log(key, value);
                createlist(key, value);
            });

            $('.openchatsbutton').on('click',function() {
                console.log("Success");

                    $('#chatframe').attr('style', "width:700px;height:600px;overflow-y:hidden;border=none;");

                    var path_to_go = "/chat/"+this.id;
                    
                    $('#chatframe').attr('src', path_to_go);
            });
        },
        error: (jqXHR, textStatus, errorThrown) => {
           console.log("error");
        }
    });

    $('#autocomplete-3').on('input', function() {
  
        const username = $('#autocomplete-3').val();
        const requestData = {'username': username };
      
        if(username != ""){
            $.ajax({
                type: "POST",
                url: "/search",
                cache: false,
                data: requestData,
                success: data => {   
                    $( "#autocomplete-3" ).autocomplete({
                        //can change this to what we want. 1 DOES NOT DO ANYTHING
                        minLength:0,   
                        delay:500,   
                        source: data
                    });
                }
            })
        }
    });

    $('#usersearch').submit(function () {
    
        const name = $('#autocomplete-3').val();

        const requestData = {'username': name};
    
        $.ajax({
            type: "POST",
            url: "/homepage",
            cache: false,
            data: requestData,
            success: data => {    
                // check what kind of error is it. 
                if(data["Success"]){
                    console.log("Success");

                    $('#chatframe').attr('style', "width:700px;height:600px;overflow-y:hidden;border=none;");

                    var path_to_go = "/chat/"+data["Success"];
                    
                    $('#chatframe').attr('src', path_to_go);

                    // var iFrame = document.getElementById( 'chatframe' );
                    // resizeIFrameToFitContent( iFrame );
                } else if(data["Invalid_user"] ){

                    console.log("Invalid user");

                    const msgElem = $('#truth');
                    msgElem.text("username does not exist");
                    msgElem.css("color", "red");
    
                    document.getElementById("search").value = "";
                 }else if(data["Cannot_Talk"] ){

                    console.log("Talking to user: " + data['Cannot_Talk'] + " Failed.");

                    const msgElem = $('#truth');
                    msgElem.text("Cannot talk to user: " + data['Cannot_Talk']);
                    msgElem.css("color", "red");
    
                    document.getElementById("search").value = "";
                 }else{
                    console.log("Error! Please contact support");
                }
            },
            error: (jqXHR, textStatus, errorThrown) => {
               console.log("error");
            }
        });
    
    
        return false;
    });


});

function resizeIFrameToFitContent( iFrame ) {

    iFrame.width  = iFrame.contentWindow.document.body.scrollWidth;
    iFrame.height = iFrame.contentWindow.document.body.scrollHeight;
}

function createlist(elem, room_number){
    var ul = document.getElementById("openchats");
    var li = document.createElement("button");
    li.setAttribute("class", "openchatsbutton");
    li.setAttribute("id", room_number);
    li.appendChild(document.createTextNode(elem));
    ul.appendChild(li);
}
