let devices = null
let response = null
var xhttp = new XMLHttpRequest();



// xhttp.open("GET", document.URL + 'search', true);
// xhttp.send();

// xhttp.onreadystatechange = function () {
//     if (this.readyState == 4 && this.status == 200) {
//         response = xhttp.responseText;
//         console.log(response)
//     }
// };

// document.getElementById("blur").addEventListener('change',()=>{
//     xhttp.open("POST", document.URL + 'submit_data', true);    
//     xhttp.send( JSON.stringify({"blur": document.getElementById("blur").value}));

// } )

// document.getElementById("color").addEventListener('change',()=>{

//     xhttp.open("POST", document.URL + 'submit_data', true);    
//     xhttp.send( JSON.stringify({"color":document.getElementById("color").value}));

// } )

// document.getElementById("refresh").addEventListener("click", ()=>{
//     console.log("refresh")
//     xhttp.open("GET", document.URL + 'refresh', true);
//     xhttp.send();

// })

// Camera feed error handling
const videoFeed = document.getElementById('video-feed');
const cameraError = document.getElementById('camera-error');

videoFeed.onerror = function() {
    videoFeed.style.display = 'none';
    cameraError.style.display = 'block';
};

videoFeed.onload = function() {
    videoFeed.style.display = 'block';
    cameraError.style.display = 'none';
};

// Function to check camera feed status
function checkCameraFeed() {
    fetch('/video_feed')
        .then(response => {
            if (!response.ok) {
                throw new Error('Camera feed not available');
            }
        })
        .catch(error => {
            videoFeed.style.display = 'none';
            cameraError.style.display = 'block';
        });
}

// Check camera feed status periodically
setInterval(checkCameraFeed, 5000);

function start() {
    fetch('/start')
        .then(response => response.text())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
    return false;
}

function pause() {
    fetch('/pause')
        .then(response => response.text())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
    return false;
}

function home() {
    fetch('/home')
        .then(response => response.text())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
    return false;
}

function stop() {
    fetch('/stop')
        .then(response => response.text())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
    return false;
}

function HomeBot1() {
    fetch('/home_1')
        .then(response => response.text())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
    return false;
}

function HomeBot2() {
    fetch('/home_2')
        .then(response => response.text())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
    return false;
}