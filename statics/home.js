var socket = io.connect({transports: ['websocket']});
const sessionId = socket.id;

   
$(document).ready(function () {
    var my_room_name = document.getElementById("note_username").textContent;
    socket.on( 'connect', function() {
        console.log("Connected");
        //Create your personal notification room for others to join to notify you
        socket.emit('create_notify', {
           username: my_room_name

        });
    });


    $.ajax({
        type: "POST",
        url: "/suggestedchats",
        cache: false,
        data: "",
        success: data => {   
            console.log(data);
            for(user in data){
                createlistSuggested(data[user]);
            }

            $('.suggestedchatsbutton').on('click',function() {
                console.log("Suggested chats Success");
                console.log(this.id);
                const sendingUser = {"username":this.id.split(':')[0]};
                callHomepage(sendingUser);
                this.remove();
            });
        },
        error: (jqXHR, textStatus, errorThrown) => {
           console.log("error");
        }
    });

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
                console.log("Open chats Success");

                $("#startachat").attr('style',"display:none;");

                $('#chatframe').attr('style', "width:700px;height:700px;overflow:hidden;visibility:visible;border:none;");

                var path_to_go = "/chat/"+this.id;
                
                $('#chatframe').attr('src', path_to_go);
                document.getElementById(this.id).style.backgroundColor = 'rgba(0, 128, 128, 0.9)';
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
                        minLength:2,   
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
    
        
        callHomepage(requestData);
        
        var elements = $('.suggestedchatsbutton');
        for(var i=0; i<elements.length; i++) {
            var text = elements[i].id.split(':')[0];
            if(name == text){
                elements[i].remove();
            }
        }

        return false;
    });

    socket.on('notification_received', function(data){
        //If you are the intended person create the button with said room id
        // and remove from suggested chats if needed
        if(data['receive_user'] == my_room_name){
            console.log("Correct Person Create Button")
            createlist(data['creating_user'] , data['room_id']);
            
            var elements = $('.suggestedchatsbutton');
            for(var i=0; i<elements.length; i++) {
            var text = elements[i].id.split(':')[0];
            if(data['creating_user'] == text){
                elements[i].remove();
            }
        }
        } else{
            console.log("You aren't the intended Person");
        }
        $('.openchatsbutton').on('click',function() {
            console.log("Success");
    
            $("#startachat").attr('style',"display:none;");
    
            $('#chatframe').attr('style', "width:700px;height:700px;overflow:hidden;visibility:visible;border:none;");
    
            var path_to_go = "/chat/"+this.id;
            
            $('#chatframe').attr('src', path_to_go);
            document.getElementById(this.id).style.backgroundColor = 'rgba(0, 128, 128, 0.9)';
        });

    });

    socket.on('new_message', function(data){
        var src = document.getElementById("chatframe").src;
        //If the chat frame isn't open whena message is received on the homepage for a chat
        //make the button show that
        console.log(src);
        if(src == null || src.indexOf(data) == -1){
        document.getElementById(data).style.backgroundColor = "red";
        }
        //Otherwise they already have the window open, no need to change the button
    });



});

function resizeIFrameToFitContent( iFrame ) {

    iFrame.width  = iFrame.contentWindow.document.body.scrollWidth;
    iFrame.height = iFrame.contentWindow.document.body.scrollHeight;
}

function createlist(elem, room_number){
    var ul = document.getElementById("openchats");
    var li = document.createElement("li");
    var button = document.createElement("button");
    button.setAttribute("class", "openchatsbutton");
    button.setAttribute("id", room_number);
    button.appendChild(document.createTextNode(elem));
    li.appendChild(button);
    ul.appendChild(li);
}

function createlistSuggested(elem){
    var ul = document.getElementById("suggestedchats");
    var li = document.createElement("li");
    var button = document.createElement("button");
    button.setAttribute("class", "suggestedchatsbutton");
    button.setAttribute("id", elem + ':' + makeid(elem.length));
    button.appendChild(document.createTextNode(elem));
    li.appendChild(button);
    ul.appendChild(li);
}

function makeid(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
       result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
 }

function callHomepage(requestData){
    $.ajax({
        type: "POST",
        url: "/homepage",
        cache: false,
        data: requestData,
        success: data => {    
            // check what kind of error is it. 
            if(data["Success"]){

                console.log("Success");

                $("#startachat").attr("style","display:none;");

                $('#chatframe').attr('style', "width:700px;height:700px;overflow-y:hidden;visibility:visible;border:none;");
                var path_to_go = "/chat/"+data["Success"];
                
                $('#chatframe').attr('src', path_to_go);

                var isPresent = false;

                $(".openchatsbutton").each(function() {
                    if(this.id == data["Success"]){
                        isPresent = True;
                    }
                });

                if(!isPresent){
                    createlist(requestData['username'], data["Success"]);
                     //emit notification
                     var my_room_name = document.getElementById("note_username").textContent;
                     //To have the other user create the button we need to give them some things
                     //Our username, the room id and for safety the person we wish to start a chat with
                     //This way incase someone else is in the room ,somehow, if they also receive this
                     //they can check if this was really meant for them or not
                     socket.emit('sending_notification', {
                        room : requestData['username'],
                        username : my_room_name,
                        chat_id : data["Success"]
                     });
                }

                $('.openchatsbutton').on('click',function() {
                    console.log("Success");
            
                    $("#startachat").attr('style',"display:none;");
            
                    $('#chatframe').attr('style', "width:700px;height:700px;overflow:hidden;visibility:visible;border:none;");
            
                    var path_to_go = "/chat/"+this.id;
                    
                    $('#chatframe').attr('src', path_to_go);
                    document.getElementById(this.id).style.backgroundColor = 'rgba(0, 128, 128, 0.9)';
                });

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
}

