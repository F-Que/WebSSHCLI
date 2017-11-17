jQuery(
  function loadPage(){
    alert('load');

    var ws_url = 'ws://' + $('#ws_server').val() + '/' + 'ws',
        args = '?host=' + $('#host').val() + '&port=' + $('#port').val()  + '&username=' + $('#username').val() + '&password=' + $('#password').val(),
        url = ws_url + args,
        socket = new WebSocket(url),
        terminal = document.getElementById('#terminal'),
        term = new Terminal({cursorBlink: true});
        alert(url);
    console.log(url);

    term.on('data', function(data) {
      // console.log(data);
      socket.send(data);
    });
    socket.onopen = function(e){
    $('#temp').hide();
      term.open(terminal, true);
      term.attach(socket);
      term._initialized = true;
    };

    socket.onmessage = function(msg){
      // console.log(msg);
      term.write(msg.data);
    };

    socket.onerror = function(e){
      console.log(e);
    };

    socket.onclose = function(e){
      console.log(e);
      term.destroy();
    };
  }
);
