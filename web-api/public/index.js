$.getJSON("walletData.json", (data) => {   
    document.getElementById("toWrite").innerHTML += "<ul> ";
    for(var i = 0; i < data.users.length; i++){
        var row = '<li><a href="/users/' + data.users[i].name + '">'  + data.users[i].name + '</a>, ' + data.users[i].balance + ' ' + data.users[i].hashValue + ' ' + '</li>';
        document.getElementById("toWrite").innerHTML += row;
    }
    document.getElementById("toWrite").innerHTML += "</ul>";
}
);

/* <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js" type="text/javascript"></script>
    <script type="text/javascript" src="index.js"></script>*/