/* Copyright 2017 Kevin Kruempelstaedter

Permission is hereby granted, free of charge, to any person obtaining a copy of this 
software and associated documentation files (the "Software"), to deal in the 
Software without restriction, including without limitation the rights to use, copy, 
modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
and to permit persons to whom the Software is furnished to do so, subject to the 
following conditions:

The above copyright notice and this permission notice shall be included in all copies 
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
 PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
 HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
 OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
 SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

This software provides the AWS lambda code for the HRC^2 Smartlab implemented
for the Human Robot Collaboration and Communication lab at Cornell University.

Authors:
Kevin Kruempelstaedter - kevkruemp@gmail.com
Michael Suguitan
*/

// import libraries
const Keys = require('./keys.js'); // storage file for particle device keys
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

exports.handler = function(event, context, callback){
	// init function
	//context.callbackWaitsForEmptyEventLoop = false;  //<---Important for firebase, but also breaks things
	// firebase initialization
	if(admin.apps.length == 0) {   // <---Important!!! In lambda, it will cause double initialization.
        admin.initializeApp({
 			 credential: admin.credential.cert(serviceAccount),
  			 databaseURL: "https://gal-9000.firebaseio.com"
		});
    }
    // Read in the evaluation condition being tested
    fbGet("/evaluation/cond").then(data => { // do not initialize alexa until the data is read in
  		console.log("eval condtion: ", data); // logs evaluation condition
  		evalmode = data;
  		var alexa = Alexa.handler(event, context, callback);
		alexa.appId = APP_ID;
		alexa.registerHandlers(handlers);
		alexa.execute();
	}).catch(e => {
  		console.log("error saving to firebase: ");
  		console.log(e);
	});
};

var handlers = {

	'launchRequest': function() {
		var speechOutput = "GAL Nine Thousand is ready.";
    	var repromptText = "What would you like to do?";
    	this.emit(':ask',speechOutput, repromptText);
	},
	'PlanterIntent': function() {	// Intent function called for planter related commands
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
		var speechOutput = "";
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
		console.log(speechOutput);
		console.log("Evaluation mode: ", evalmode);
		if(evalmode == 2 || evalmode == 4){ // If alexa response is enabled
			callDirectiveService(this.event, speechOutput); // give an alexa response immediately
			console.log("Directive called");
		}
		if(evalmode == 3 || evalmode == 4){
			callParticle(this.event,"controlled","D0,HIGH",BLINDS_DEVICE_ID,BLINDS_TOKEN);
			console.log("Blossom triggered");
		}
		callParticle(this.event,"waterSome",plants,PLANTER_DEVICE_ID, PLANTER_TOKEN);		
		if(evalmode == 2 || evalmode == 4){ // If alexa response is enabled
			this.emit(':tell','Completed');
		}
		else{
			this.emit(':tell',' ');
		}
	},

	'BlindsIntent': function() { // Intent function called for blinds related commands
		var intentObj = this.event.request.intent; // setup a slots object
		var objectID = intentObj.slots.objectID.value;
		console.log("objectID = " + objectID);
		console.log(evalmode);
		
		if(objectID == "raise"){
			fbPut("/blinds/cmd", "raise").then(res => {
				if(evalmode == 3 || evalmode == 4){
					callParticle(this.event,"controlled","D0,HIGH",BLINDS_DEVICE_ID,BLINDS_TOKEN);
				}
				callParticle(this.event,"controlled","D7,HIGH",BLINDS_DEVICE_ID,BLINDS_TOKEN);
				if(evalmode == 2 || evalmode == 4){
					this.emit(':tell',"Ok, raising the blinds."); // Dont respond with alexa until the data has been successfully entered
				}
				else{
					this.emit(':tell',' ');
				}
			});
		}
		else if(objectID == "lower"){
			fbPut("/blinds/cmd", "raise").then(res => {
				if(evalmode == 3 || evalmode == 4){
					callParticle(this.event,"controlled","D0,HIGH",BLINDS_DEVICE_ID,BLINDS_TOKEN);
				}
				callParticle(this.event,"controlled","D6,HIGH",BLINDS_DEVICE_ID,BLINDS_TOKEN);
				if(evalmode == 2 || evalmode == 4){
					this.emit(':tell',"Ok, lowering the blinds."); // Dont respond with alexa until the data has been successfully entered
				}
				else{
					this.emit(':tell',' ');
				}
			});
		}
		else{
			this.emit('unhandled');
		}
	},

    'LightsIntent': function() {
        var intentObj = this.event.request.intent;
        var lights = intentObj.slots.LIGHTS.value;

        if (typeof lights == 'undefined') {
            lights = ' ';
        }
        this.emit(':tell',"Ok, switching the "+lights+" lights");
        callParticle(this.event,"hitSwitch",lights,BLINDS_DEVICE_ID,BLINDS_TOKEN)
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

function callParticle(event, func, input, Device_ID, token) {
	// Call the Particle API
	var fnPr = particle.callFunction({
	    deviceId: Device_ID,
	    name: func, // function to call
	    argument: input,   // input to the called function
	    auth: token
	    });
    console.log(fnPr);
	fnPr.then(
        function(data) {
            console.log(func + ' successful:', data);
    }).catch(function(err) {
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

// firebase http boilerplate
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