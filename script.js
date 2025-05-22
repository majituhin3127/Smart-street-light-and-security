function startRecognition() {
    fetch('http://127.0.0.1:5000/start')
    .then(response => response.text())
    .then(data => {
        console.log(data);
        alert("Face recognition started!");
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Failed to start face recognition.");
    });
}


function sign(){
    window.location.href = "https://blynk.cloud/dashboard/415046/global/devices/1";
}