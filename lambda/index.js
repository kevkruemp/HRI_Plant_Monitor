/* eslint-disable  func-names */
/* eslint quote-props: ["error", "consistent"]*/
/**
 * This sample demonstrates a simple skill built with the Amazon Alexa Skills
 * nodejs skill development kit.
 * This sample supports multiple lauguages. (en-US, en-GB, de-DE).
 * The Intent Schema, Custom Slots and Sample Utterances for this skill, as well
 * as testing instructions are located at https://github.com/alexa/skill-sample-nodejs-fact
 **/
'use strict';

// import libraries
const Keys = require('./keys'); // storage file for particle device keys
const Alexa = require("alexa-sdk");
var Particle = require('particle-api-js');
var admin = require('firebase-admin');
var serviceAccount = require('./gal-9000-firebase.json');
var https = require('https');
var firebaseHost = "gal-9000.firebaseio.com";

const APP_ID = undefined;  // TODO replace with your app ID (OPTIONAL).

var cardTitle = 'HRC2 Smart Lab';
var cardContent = 'This is stuff';

var particle = new Particle();
var PLANTER_DEVICE_ID = Keys.PLANTER_DEVICE_ID;
var PLANTER_TOKEN = Keys.PLANTER_TOKEN;
var BLINDS_DEVICE_ID = Keys.BLINDS_DEVICE_ID;
var BLINDS_TOKEN = Keys.BLINDS_TOKEN;
var evalmode = '';

var states = {
    GUESSMODE: '_GUESSMODE', // User is trying to guess the number.
    STARTMODE: '_STARTMODE'  // Prompt the user to start or restart the game.
};

exports.handler = function(event, context, callback){
	// init function
	// firebase initialization
	context.callbackWaitsForEmptyEventLoop = false;  //<---Important
	/*var config = {
        apiKey: "AIzaSyAm1V5_UjuW-pAtb9Kgeq3iCi58j_Kz5a0",
        authDomain: "gal-9000.firebaseapp.com",
        databaseURL: "https://gall-9000.firebaseio.com",
        storageBucket: "gal-9000.appspot.com",
    };*/
	if(admin.apps.length == 0) {   // <---Important!!! In lambda, it will cause double initialization.
        admin.initializeApp({
 			 credential: admin.credential.cert(serviceAccount),
  			 databaseURL: "https://gal-9000.firebaseio.com"
		});
		//admin.initializeApp(config);
    }
    fbGet("/evaluation/cond").then(data => {
  		console.log(data); // prints "lol"
  		evalmode = data;
  		var alexa = Alexa.handler(event, context, callback);
		alexa.appId = APP_ID;
		alexa.registerHandlers(handlers);
		alexa.execute();
	}).catch(e => {
  		console.log("error saving to firebase: ");
  		console.log(e);
	});
	// Get a reference to the database service
    
};

var handlers = {

	'launchRequest': function() {
		var speechOutput = "Welcome to the HRI Smart Lab, please tell me what to do.";
    	var repromptText = "What would you like to do?";
    	this.emit(':ask',speechOutput, repromptText);
	},
	'PlanterIntent': function() {
		var intentObj = this.event.request.intent; // setup a slots object
		var objectID = intentObj.slots.objectID.value;
		var plant1 = intentObj.slots.FIRSTPLANT.value;
		var plant2 = intentObj.slots.SECONDPLANT.value;
		var plant3 = intentObj.slots.THIRDPLANT.value;
		var plant4 = intentObj.slots.FOURTHPLANT.value;

		// assemble the composite plant structure length = num of plants
		var plants = "";
		if(typeof plant1 != 'undefined'){
		    plants = plants + plant1;
		}
		if(typeof plant2 != 'undefined'){
		    plants = plants + plant2;
		}
		if(typeof plant3 != 'undefined'){
		    plants = plants + plant3;
		}
		if(typeof plant4 != 'undefined'){
		    plants = plants + plant4;
		}
		// debugging console logs
		console.log("objectID = " + objectID);
		console.log("plant1 = " + plant1);
		console.log("plant2 = " + plant2);
		console.log("plant3 = " + plant3);
		console.log("plant4 = " + plant4);
		console.log("plants = " + plants);

		// Determine speech based on number of plants requested
		if(typeof plant2 == 'undefined'){ // if a second plant was not defined
			speechOutput = "OK, watering plant " + plant1;
		}
		else if(typeof plant3 == 'undefined'){
			speechOutput = "OK, watering plants " + plant1 +", and " + plant2;
		}
		else if(typeof plant4 == 'undefined'){
			speechOutput = "OK, watering plants " + plant1 +", " + plant2 +", and " + plant3;
		}
		else {
			speechOutput = "OK, watering plants " + plant1 +", " + plant2 +", " + plant3 +", and " + plant4;
		}

		callDirectiveService(this.event, speechOutput); // give an alexa response immediately
		callParticle(this.event,"waterSome",plants,PLANTER_DEVICE_ID, PLANTER_TOKEN);		
		callParticle(this.event,"controlled","D0,HIGH",BLINDS_DEVICE_ID,BLINDS_TOKEN);
		this.emit(':tell','Completed');
	},
	'BlindsIntent': function() {
		var intentObj = this.event.request.intent; // setup a slots object
		var objectID = intentObj.slots.objectID.value;
		console.log("objectID = " + objectID);

		if(objectID == "raise"){
			callParticle(this.event,"controlled","D7,HIGH",BLINDS_DEVICE_ID,BLINDS_TOKEN);
			fbPut("/hello", "world").then(res => {
				this.emit(':tell',"Ok, raising the blinds.");
			});
		}
		else if(objectID == "lower"){
			callParticle(this.event,"controlled","D6,HIGH",BLINDS_DEVICE_ID,BLINDS_TOKEN);
			this.emit(':tell',"Ok, lowering the blinds.");
		}
		else{
			this.emit('unhandled');
		}
	},
	'AMAZON.HelpIntent': function () {
        this.response
            .speak("You can ask me to turn the planter on or off, which will water all of the plants. You can also ask me to water a plant individually.")
            .listen("What would you like to do?");
        this.emit(':responseReady');
    },
    'Unhandled': function() {
        this.emit(':tell',"I'm sorry, I didn't understand what you said")
    }
};

function testGuards(event, intentObj){
	// FMR logic checking to prevent system breakage
}

function sendToFirebase(){
	var database = admin.database();
	var blinds_state = database.ref('/blinds/state').once('value', function(data){
		console.log("Blinds state:", data.val());
		return data.val();
		});
	//var updates = {};
	//updates['blinds/cmd'] = "lambda";
	database.ref().child("hello") // creates a key called hello
    .set("world")                            // sets the key value to world
    .then(function (data) {
      console.log('Firebase data: ', data);        
      context.succeed();                  // important that you don't call succeed until you are called back otherwise nothing will be saved to the database!
    })
    .catch(function (error) {
        console.log('Firebase error: ', error);
        context.fail();
    });
}

function callParticle(event, func, input, Device_ID, token) {
	// Call the Particle API
	var fnPr = particle.callFunction({
	    deviceId: Device_ID,
	    name: func, // function to call
	    argument: input,   // input to the called function
	    auth: token
	    });
	fnPr.then(
        function(data) {
            console.log(func + ' successful:', data);
            }, function(err) {
                console.log('An error occurred:', err);
    });
}

function callDirectiveService(event, message) {
    // Call Alexa Directive Service.
    const ds = new Alexa.services.DirectiveService();
    const requestId = event.request.requestId;
    const endpoint = event.context.System.apiEndpoint;
	const token = event.context.System.apiAccessToken;
	const directive = new Alexa.directives.VoicePlayerSpeakDirective(requestId, message);
    ds.enqueue(directive, endpoint, token)
    .catch((err) => {
        console.log(Messages.DIRECTIVEERRORMESSAGE + err);
    });
}

function fbGet(key){
  return new Promise((resolve, reject) => {
    var options = {
      hostname: firebaseHost,
      port: 443,
      path: key + ".json",
      method: 'GET'
    };
    var req = https.request(options, function (res) {
      res.setEncoding('utf8');
      var body = '';
      res.on('data', function(chunk) {
        body += chunk;
      });
      res.on('end', function() {
        resolve(JSON.parse(body))
      });
    });
    req.end();
    req.on('error', reject);
  });
}
 
function fbPut(key, value){
  return new Promise((resolve, reject) => {
    var options = {
      hostname: firebaseHost,
      port: 443,
      path: key + ".json",
      method: 'PUT'
    };
 
    var req = https.request(options, function (res) {
      res.setEncoding('utf8');
      var body = '';
      res.on('data', function(chunk) {
        body += chunk;
      });
      res.on('end', function() {
        resolve(body)
      });
    });
    req.end(JSON.stringify(value));
    req.on('error', reject);
  });
}