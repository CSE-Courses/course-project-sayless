var socket = io.connect("https://sayless.azurewebsites.net");
const sessionId = socket.id;
socket.on( 'connect', function() {
socket.emit('join',{
    path_name : window.location.pathname
});

socket.emit("store",{sessionId});
} );

// message sends only when you hit send
$("#send").click(function() {
    let user_input = $( 'input.message' ).val()
    console.log(user_input);
    socket.emit( 'sending_message', {
    message : user_input,
    path_name : window.location.pathname
    } );
    $( 'input.message' ).val( '' ).focus()
} );

// this my response displays the messages a user sends
socket.on('message_received', function(data) {
    console.log(data);

    if(data.user.length != 0){
        $('#header').text(data.user);
    }else{
        $('#chat').val($('#chat').val() + data.msg + '\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);   
    }
});