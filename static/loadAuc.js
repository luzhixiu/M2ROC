function codeAddress() {
   document.getElementById("submit").addEventListener("click",loadGif);
}

function loadGif(){
document.getElementById("loading") .style="width:50px;height:50px;";
}


window.onload = codeAddress;
