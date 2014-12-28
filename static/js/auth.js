// Constants
var CLIENT_ID = "607994131901-if7as8ck330umlddcgmnmbhr05isalhm.apps.googleusercontent.com";
var SCOPES = ["email"];
var words = [];


// Main callback from gapi
function init() {
    var apisToLoad;
    function loadCallback() {
        if (--apisToLoad == 0) {
            signin(true, userAuthed);
        }
    };

    apisToLoad = 2; // must match number of calls to gapi.client.load()
    apiRoot = '//' + window.location.host + '/_ah/api';
    gapi.client.load('wordsapi', 'v1', loadCallback, apiRoot);
    gapi.client.load('oauth2', 'v2', loadCallback);
}

// Sign in with google
function signin(mode, authorizeCallback) {
    gapi.auth.authorize({client_id: CLIENT_ID,
                        scope: SCOPES, immediate: mode},
                        authorizeCallback);
}


function userAuthed() {
    function initializeWords() {
        gapi.client.wordsapi.getallmywords().then(function(resp){
            if (resp.result.hasOwnProperty('records')) {
                words = resp.result.records;
                main.data = words;
            }
        });
    }

    var request =
        gapi.client.oauth2.userinfo.get().execute(function(resp) {
            if (!resp.code) {
                // User is signed in, call my Endpoint
                $("#signinButton").addClass("hidden");
                $("#userinfo").text(resp.email);
                // Initialize data
                initializeWords();
            }
        });
}


function auth() {
    signin(false, userAuthed);
};
