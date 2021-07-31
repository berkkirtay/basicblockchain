const express = require('express');

//const spawn = require('child_process').spawn;
const spawn = require('await-spawn');

const app = express();

const fetch = require('node-fetch');

app.use(express.static('public'));

app.use(express.urlencoded({ extended: true }));

app.use(express.json());

var crypto = require('crypto');

const database = require('./database');

async function readDB() {
	fs.readFile('./public/walletData.json', 'utf8', async (err, data) => {
		if (err) {
			throw err;
		}
		//wallets = data;
		wallets = await JSON.parse(data);
	});
	await db.users.push(wallets[0]);
	db.save(done);
}

async function insertToDB(publicName, publicPass) {
	await new database({
		name: publicName,
		balance: 0,
		hashValue: crypto.createHash('sha256').update(publicPass).digest('hex'),
	}).save();
}

async function deleteUserFromDB(publicName) {
	await database.deleteOne({ name: publicName });
}

var cookieSession = require('cookie-session');

app.use(
	cookieSession({
		name: 'currentSession',
		keys: ['key1'],
		resave: false,
		saveUninitialized: false,
		maxAge: 60 * 10000,
	})
);

var path = require('path');

// To keep using html files with ejs engine.
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');
app.set('views', path.join(__dirname, 'views'));

var fs = require('fs'); // .promises
var wallets = [];

/*function readWallet() {
   fs.readFile('./public/walletData.json', 'utf8', (err, data) => {
        if (err){
            throw err;
        }
        //wallets = data;
        wallets = JSON.parse(data);
    });
 //   wallets = await fs.readFile('./public/walletData.json', 'utf8');
}
*/

async function readWallet() {
	fs.readFile('./public/walletData.json', 'utf8', async (err, data) => {
		if (err) {
			throw err;
		}
		//wallets = data;
		wallets = await JSON.parse(data);
	});
}

readWallet();
// readDB();

var isUserSpecified = false;
var currentUser = 'undefined';
var session;

// IO method should be changed to get a better performance.
async function refreshCurrentUser(publicName) {
	await assignUser(publicName);
	return;
}

async function assignUser(publicName) {
	for (var i = 0; i < wallets.users.length; i++) {
		if (wallets.users[i].name === publicName) {
			isUserSpecified = true;
			currentUser = wallets.users[i];
		}
	}
}

/*
app.use((req, res, next) => {
    console.log("New Request ");
    console.log('Host name: ' + req.hostname);
    console.log('Request url: ' + req.path);
    console.log('Request http method: ' + req.method);
    next();
})
*/

//Home page

app.get('/', (req, res) => {
	req.session.isAuth = true;

	readWallet();
	if (isUserSpecified) {
		res.render('index', { title: 'Home', isUserSpecified, user: currentUser, alert: false });
	} else {
		res.render('index', { title: 'Home', isUserSpecified, user: currentUser, alert: false });
	}
});

app.post('/', (req, res) => {
	const publicName = req.body.wallet.publicName;
	const publicPass = req.body.wallet.publicPass;

	refreshCurrentUser(publicName);

	if (isUserSpecified === false) {
		return res.render('index', { title: 'Home', isUserSpecified, user: currentUser, alert: true });
	} else {
		return res.redirect('/');
	}
});

app.get('/exit', (req, res) => {
	isUserSpecified = false;
	return res.redirect('/');
});

// Users and wallet operations.
app.get('/users', (req, res) => {
	readWallet();
	res.render('users', { title: 'Users', users: wallets.users, isUserSpecified, user: currentUser });
});

app.get('/createWallet', (req, res) => {
	res.render('createWallet', { title: 'Create wallet', isUserSpecified: false, user: currentUser });
});

app.post('/createWallet', async (req, res) => {
	const publicName = req.body.createWallet.publicName;
	const publicPass = req.body.createWallet.publicPass;
	const python = await spawn('python', ['api-scripts/createWallet.py', publicName, publicPass]);
	/* python.stdout.on('data', function (data) {
         console.log(data.toString());
     })*/
	insertToDB(publicName, publicPass);

	console.log('New wallet created-> ' + publicName);

	readWallet();

	if (isUserSpecified === true) {
		return res.redirect('/');
	}

	refreshCurrentUser(publicName);

	return res.redirect('/');
});

app.get('/users/:id', (req, res) => {
	const id = req.params.id;
	wallets.users.find((user) => {
		if (user.name === id) {
			return res.render('users', { title: id, users: [], user: user, isUserSpecified });
		}
	});
});

app.get('/users/:id/delete', async (req, res) => {
	const id = req.params.id;
	const python = await spawn('python', ['api-scripts/deleteWallet.py', id]);
	console.log('Wallet ' + id + ' is deleted.');
	deleteUserFromDB(id);
	return res.redirect('/users');
});

//Transactions
app.get('/transactions', (req, res) => {
	if (isUserSpecified) {
		readWallet();
		refreshCurrentUser(currentUser.name);
		res.render('transactions', { title: 'Transactions', isUserSpecified, user: currentUser });
	} else {
		res.redirect('/');
	}
});

app.post('/transactions', async (req, res) => {
	const publicAddress = req.body.transactions.publicAddress;
	const coinAmount = req.body.transactions.coinAmount;
	const python = await spawn('python', ['api-scripts/handleTransaction.py', currentUser.name, publicAddress, coinAmount]);
	/* python.stdout.on('data', function (data) {
        console.log(data.toString());
    })*/
	return res.redirect('/transactions');
});

// If server receives an undefined request, it will return a 404 error.
app.use('/', (req, res) => {
	return res.status(404).render('404', { title: '404', user: currentUser, isUserSpecified });
});

app.listen(8000, async () => {
	console.log('Listening');
});
