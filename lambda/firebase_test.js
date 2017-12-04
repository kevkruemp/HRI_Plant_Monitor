var admin = require("firebase-admin");

// Fetch the service account key JSON file contents
var serviceAccount = require('./gal-9000-firebase.json');

// Initialize the app with a service account, granting admin privileges
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://gal-9000.firebaseio.com"
});

// As an admin, the app has access to read and write all data, regardless of Security Rules
var db = admin.database();
var ref = db.ref("blinds/state");
var stuff = ref.once("value", function(snapshot) {
  console.log("snapshot = ",snapshot.val());
  return snapshot;
});
var ref = db.ref('blinds');
ref.set({
  state: "test",
  cmd: "testcmd"
});