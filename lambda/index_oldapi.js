/* eslint-disable  func-names */
/* eslint quote-props: ["error", "consistent"]*/
/**
 * This sample demonstrates a simple skill built with the Amazon Alexa Skills
 * nodejs skill development kit.
 * This sample supports multiple lauguages. (en-US, en-GB, de-DE).
 * The Intent Schema, Custom Slots and Sample Utterances for this skill, as well
 * as testing instructions are located at https://github.com/alexa/skill-sample-nodejs-fact
 **/

// import libraries
var http = require("http");
var Particle = require('particle-api-js');
var AlexaSkill = require('./AlexaSkill');

const APP_ID = undefined;  // TODO replace with your app ID (OPTIONAL).

var cardTitle = 'HRC2 Smart Lab';
var cardContent = 'This is stuff';

var particle = new Particle();
var PARTICLE_DEVICE_ID = "260036001047343339383037";
var PARTICLE_ACCESS_TOKEN = "b70eaba685fc4ddb7ff9b2ff0d32c889c4cd17ba";

var ParticleSkill = function () {
    AlexaSkill.call(this, APP_ID);
};

// Extend AlexaSkill
ParticleSkill.prototype = Object.create(AlexaSkill.prototype);
ParticleSkill.prototype.constructor = ParticleSkill;

ParticleSkill.prototype.eventHandlers.onSessionStarted = function (sessionStartedRequest, session) {
    console.log("ParticleSkillssionStarted requestId: " + sessionStartedRequest.requestId
	+ ", sessionId: " + session.sessionId);
};

//-------->This is invoked by invocation word
ParticleSkill.prototype.eventHandlers.onLaunch = function (launchRequest, session, response) {
    console.log("ParticleSkillunch requestId: " + launchRequest.requestId + ", sessionId: " + session.sessionId);
    var speechOutput = "Welcome to the HRI Smart Lab, please tell me what to do.";
    var repromptText = "What would you like to do?";
    response.ask(speechOutput, repromptText);
};

ParticleSkill.prototype.eventHandlers.onSessionEnded = function (sessionEndedRequest, session) {
    console.log("ParticleSkillssionEnded requestId: " + sessionEndedRequest.requestId
	+ ", sessionId: " + session.sessionId);
};

ParticleSkill.prototype.intentHandlers = {
    // register custom intent handlers
    "ParticleIntent": function (intent, session, response) {
		var sensorSlot = intent.slots.sensor;
		var onoffSlot = intent.slots.onoff;
		var objectSlot = intent.slots.objectID;
		var plant1Slot = intent.slots.FIRSTPLANT;
		var plant2Slot = intent.slots.SECONDPLANT;
		var plant3Slot = intent.slots.THIRDPLANT;
		var plant4Slot = intent.slots.FOURTHPLANT;
		
		// set the initial value for the utterance variables
		var sensor = sensorSlot ? intent.slots.sensor.value : "";
		var onoff = onoffSlot ? intent.slots.onoff.value : "off";
		var objectID = objectSlot ? intent.slots.objectID.value : "";
		var plant1 = plant1Slot ? intent.slots.FIRSTPLANT.value : "0";
		var plant2 = plant2Slot ? intent.slots.SECONDPLANT.value : "0";
		var plant3 = plant3Slot ? intent.slots.THIRDPLANT.value : "0";
		var plant4 = plant4Slot ? intent.slots.FOURTHPLANT.value : "0";
		
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
		
	
		console.log("Sensor = " + sensor);
		console.log("OnOff = " + onoff);
		console.log("objectID = " + objectID);
		console.log("plant1 = " + plant1);
		console.log("plant2 = " + plant2);
		console.log("plant3 = " + plant3);
		console.log("plant4 = " + plant4);
		console.log("plants = " + plants);
		
		var op = "";
		var pin = "";
		var pinvalue = "";
		var func = "";
		
		// Check slots and call appropriate Particle Functions
		if(sensor == "planter"){
			
			func = "waterAll";
		}
		if(sensor == "water"){
			func = "waterSome";
		}
		if(sensor == "blinds"){
			func = "blinds";
		}
		
		console.log("func = " + func);
		// If the user gives a command with no response value
		if(func.length > 0){

			if(func == "waterAll"){
				var fnPr = particle.callFunction({
	                deviceId: PARTICLE_DEVICE_ID,
	                name: "waterAll", // function to call
	                argument: "go",   
	                auth: PARTICLE_ACCESS_TOKEN
	                });

	            fnPr.then(
	                    function(data) {
	                        console.log('waterAll successful:', data);
	                        response.tellWithCard("OK, " + sensor + " turned " + onoff, cardTitle, "Planter on");
	                        }, function(err) {
	                            console.log('An error occurred:', err);
	                });
				}
			else if(func == "blinds"){
				if(objectID == "raise"){
					var options = {
  					hostname: '10.148.8.235',
  					port: 8000,
  					path: '/up',
  					method: 'GET',
  					headers: {
      					'Content-Type': 'application/json',
  						}
					};
					console.log("raised statement hit");
				}
				else{
					response.tellWithCard("OK, lowering the blinds", cardTitle, "Blinds lowered");
				}
				var req = http.get(options, function(res) {
  					console.log('STATUS: ' + res.statusCode);
  					console.log('HEADERS: ' + JSON.stringify(res.headers));

  					// Buffer the body entirely for processing as a whole.
  					var bodyChunks = [];
  					res.on('data', function(chunk) {
    				// You can process streamed parts here...
    				bodyChunks.push(chunk);
  						}).on('end', function() {
    				var body = Buffer.concat(bodyChunks);
   					 console.log('BODY: ' + body);
    					// ...and/or process the entire body here.
  					})
				});

				req.on('error', function(e) {
  				console.log('ERROR: ' + e.message);
				});
				response.tellWithCard("OK, raising the blinds", cardTitle, "Blinds raised");
			}
			else{

				var fnWs = particle.callFunction({
	                deviceId: PARTICLE_DEVICE_ID,
	                name: "waterSome", // function to call
	                argument: plants,
	                auth: PARTICLE_ACCESS_TOKEN
	                });
                if(typeof plant2 == 'undefined'){ // if a second plant was not defined
	                fnWs.then(
	                    function(data) {
	                        console.log('waterSome successful:', data);
	                        response.tellWithCard("OK, watering plant " + plant1, cardTitle, "Plant" + plant1);
	                        }, function(err) {
	                            console.log('An error occurred:', err);
	                });
                }
                else if(typeof plant3 == 'undefined'){
	                fnWs.then(
	                    function(data) {
	                        console.log('waterSome successful:', data);
	                        response.tellWithCard("OK, watering plants " + plant1 +", and " + plant2, cardTitle, "Plants " + plants);
	                        }, function(err) {
	                            console.log('An error occurred:', err);
	                });
                }
                else if(typeof plant4 == 'undefined'){
	                fnWs.then(
	                    function(data) {
	                        console.log('waterSome successful:', data);
	                        var plants = plant1 + ", "+ plant2;
	                        response.tellWithCard("OK, watering plants " + plants +", and " + plant3, cardTitle, "Plants " + plants);
	                        }, function(err) {
	                            console.log('An error occurred:', err);
	                });
                }
                else{
                    fnWs.then(
	                    function(data) {
	                        console.log('waterSome successful:', data);
	                        var plants = plant1 + " "+ plant2 + " " + plant3;
	                        response.tellWithCard("OK, watering plants " + plants +", and " + plant4, cardTitle, "Plants " + plants);
	                        }, function(err) {
	                            console.log('An error occurred:', err);
	                });
                }
			}
		}
		else{
			response.tell("Sorry, I could not understand what you said");
		}
    },
    HelpIntent: function (intent, session, response) {
        var output = "You can ask me to turn the planter on or off, which will water all of the plants. You can also ask me to water a plant individually.";
        var reprompt = "What would you like to do?";
        console.log('Help intent');
		response.ask(output, reprompt);
    }
};

// Create the handler that responds to the Alexa Request.
exports.handler = function (event, context) {
    // Create an instance of the ParticleSkill skill.
    var particleSkill = new ParticleSkill();
    particleSkill.execute(event, context);
};