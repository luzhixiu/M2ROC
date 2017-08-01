
window.onload = function() {
    var canvas = document.getElementById("myCanvas");
    var ctx = canvas.getContext("2d");
    var img = new Image(1,1); // width, height values are optional params 
    img.src ="static/auc.png
    ctx.drawImage(img, 10, 10);
};
