//import html2canvas from 'html2canvas.js';

var takeScreenShot = function(){

	//const html2canvas = require('html2canvas');
	html2canvas(document.getElementById("container"), {
        onrendered: function (canvas) {
            var tempcanvas=document.createElement('canvas');
            tempcanvas.width=350;
            tempcanvas.height=350;
            var context=tempcanvas.getContext('2d');
            context.drawImage(canvas,0,0,1000,1000,0,0,500,500);
            var link=document.createElement("a");
            link.href=tempcanvas.toDataURL('image/jpg');   //function blocks CORS
            link.download = 'screenshot.jpg';
            link.click();
        }
    });

}