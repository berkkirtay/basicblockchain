const express = require('express');
const spawn = require('child_process').spawn;

const app = express();

const fetch = require("node-fetch");

app.use(express.static('public'));

app.use(express.urlencoded({ extended: true }));

app.use(express.json());

var path = require('path');

// To keep using html files with ejs engine.
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');
app.set('views', path.join(__dirname, 'views'));

var fs = require('fs');
var wallets;

function readWallet() {
    fs.readFile('./public/walletData.json', 'utf8', (err, data) => {
        if (err){
            throw err;
        }
        wallets = JSON.parse(data);
    });
}

readWallet();

var isUserSpecified = false;
var currentUser = "undefined";
var currentUserID = 0;

function refreshCurrentUser(userID){
    currentUser = wallets.users[userID];
    currentUserID = userID;
}

//Home page

app.get('/', (req, res) => {
    readWallet();
    if(isUserSpecified){
        res.render("index", {title: "Home", isUserSpecified, user: currentUser, alert: false});
    }
    else{
        res.render("index", {title: "Home", isUserSpecified, user: currentUser, alert: false });
    }
})

app.post('/', (req, res) => {
    const publicName = req.body.wallet.publicName;
    const publicPass = req.body.wallet.publicPass;
    for(var i = 0; i < wallets.users.length; i++){
        if(wallets.users[i].name === publicName){
            isUserSpecified = true;
            refreshCurrentUser(i);
            return res.redirect('/');
        }
    }
    return res.render("index", {title: "Home", isUserSpecified, alert: true});
})

app.get('/exit', (req, res) => {
    isUserSpecified = false;
    return res.redirect('/');
})

// Users and wallet operations.
app.get('/users', (req, res) => {
    readWallet();
    res.render("users", { title : "Users", users: wallets.users, isUserSpecified, user: currentUser });
})

app.get('/createWallet', (req, res) => {
    res.render("createWallet", {title : "Create wallet", isUserSpecified: false, user: currentUser });
})

app.post('/createWallet', (req, res) => {
    const publicName = req.body.createWallet.publicName;
    const publicPass = req.body.createWallet.publicPass;
    const python = spawn('python', ['api-scripts/createWallet.py', publicName, publicPass]);
    python.stdout.on('data', function (data) {
        console.log(data.toString());
    })
    console.log("New wallet created-> " + publicName);
  
    readWallet();

    if(isUserSpecified === true){
        return res.redirect('/');
    }
    // IO method should be changed to get a better performance.
    for(var i = 0; i < wallets.users.length; i++){
        if(wallets.users[i].name === publicName){
            isUserSpecified = true;
            refreshCurrentUser(i);
            return res.redirect('/');
        }
    }
    return res.redirect('/');
})

app.get('/users/:id', (req, res) => {
    const id = req.params.id;
    wallets.users.filter((user) => {
        if(user.name === id){   
           return res.render('users', { title: id, users: [], user: user, isUserSpecified });
        } 
    });  
})

app.get('/users/:id/delete', (req, res) => {
    const id = req.params.id;
    const python = spawn('python', ['api-scripts/deleteWallet.py', id]);
    console.log("Wallet " + id + " is deleted.");
    return res.redirect('/users');
})


//Transactions
app.get('/transactions', (req, res) => {
    if(isUserSpecified){
        readWallet();
        refreshCurrentUser(currentUserID);
        var coins = currentUser.balance;
        res.render("transactions", {title: "Transactions", isUserSpecified, user: currentUser, coins });
    }
    else{
        res.redirect("/");
    } 
})

app.post('/transactions', (req, res) => {
    const publicAddress = req.body.transactions.publicAddress;
    const coinAmount = req.body.transactions.coinAmount;
    const python = spawn('python', ['api-scripts/handleTransaction.py', currentUser.name, publicAddress, coinAmount]);
    python.stdout.on('data', function (data) {
        console.log(data.toString());
    })
    return res.redirect('/transactions');
})

 // If server receives an undefined request, it will return a 404 error.
app.use('/', (req, res) =>{
    return res.status(404).render("404", {title: "404"});
})

app.listen(80, () =>  {
    console.log('Listening') });
