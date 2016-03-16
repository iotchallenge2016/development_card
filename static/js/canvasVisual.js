var HEIGHT = 100;
var WIDTH = 100;
var canvas = new fabric.StaticCanvas('respondCanvas');
var button = document.getElementById("create");
var zones = [];


var zonesInfo = [ 
  {left: 295.5063716159557, top: 131.72390292367152, scaleX: 1.536838842526588, scaleY: 1.6857065087475913, angle: 3.8890539330117546, lugares: 30, max: 40},
  {left: 278.8729430261647, top: 331.59313829697, scaleX: 1.4250574039124928, scaleY: 1.5081040961782741, angle: 4.8796811563988145, lugares: 15, max: 40},
  {left: 265.0155181282574, top: 501.2838252759253, scaleX :1.2600444979839147, scaleY:0.9546760388661403, angle:4.434359226879513, lugares: 10, max: 40}
  ];

canvas.setBackgroundImage('/static/img/estacionamiento.jpg', canvas.renderAll.bind(canvas), {
    backgroundImageOpacity: 0.5,
    backgroundImageStretch: true
});


function readZones(){
  var i;
  console.log(zonesInfo.length);
  for(i = 0; i < zonesInfo.length; i++){
    var lugares = zonesInfo[i]["lugares"];
    var max = zonesInfo[i]["max"];
    var red = 255;
    var green = 255;

    if(lugares > max/2){
      red = Math.floor(2*255*(max-lugares)/max);
    } else{
      green = Math.floor(2*255*lugares/max);
    }

    var colorString = 'rgb(' + red.toString() + ',' + green.toString() + ',0)';
    console.log(colorString);

    var rectangle = new fabric.Rect({ 
    width: WIDTH, 
    height: HEIGHT, 
    fill: colorString, 
    opacity: 0.5,



  });

    rectangle.top = zonesInfo[i]["top"];
    rectangle.left = zonesInfo[i]["left"];
    rectangle.scaleX = zonesInfo[i]["scaleX"];
    rectangle.scaleY = zonesInfo[i]["scaleY"];
    rectangle.angle = zonesInfo[i]["angle"];

    zones.push(rectangle)
    canvas.add(rectangle);
  }
}

function createZone(){
  var rectangle = new fabric.Rect({ 
    width: WIDTH, 
    height: HEIGHT, 
    fill: '#77f', 
    top: 100, 
    left: 100 });

  rectangle.opacity = 0.5;
  zones.push(rectangle)
  canvas.add(rectangle);
}

function displayInfo(){
  var rectangle = zones[0];
  console.log("Rectangle 1");
  console.log(rectangle.left);
  console.log(rectangle.top);
  console.log(rectangle.scaleX);
  console.log(rectangle.scaleY);
  console.log(rectangle.angle);
}

$(document).ready( function(){
    readZones();
}); 