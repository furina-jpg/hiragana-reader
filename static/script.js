// create the drawing board & give it functionality
var sidelength = 28;
var drawboard = document.getElementById('drawboard');
var isDragging = false;
drawboard.addEventListener('mousedown', function(){
  isDragging = true;
});
drawboard.addEventListener('mouseup', function(){
  isDragging = false;
});
for(var i = 0; i < sidelength*sidelength; i++){
  var cell = document.createElement('span');
    
  // classification
  cell.classList.add('cell');
  cell.id = 'cell' + i;
    
  // make it work smoothly
  cell.addEventListener('mouseover', function(){
    if(isDragging){
    this.classList.add('colored');
  }});
    cell.addEventListener('click', function(){
    this.classList.add('colored');
  });
    
  // add to board
  drawboard.appendChild(cell);
}

// give the buttons at the bottom functionality
var submitmap = [];
var count = 0;
document.getElementById('clear').addEventListener('click', function(){
  for(var i = 0; i < sidelength*sidelength; i++){
    document.getElementById('cell' + i).classList.remove('colored');
  }
});
document.getElementById('submit').addEventListener('click', function(){
  submitmap = [];
  for(var i = 0; i < sidelength; i++){
    var rowmap = [];
    for(var j = 0; j < sidelength; j++){
      if(document.getElementById(('cell' + (i*sidelength + j))).classList.contains('colored')){
        rowmap.push(1);
      } else {
        rowmap.push(0);
      }
    }
    submitmap.push(rowmap);
  }
  for(var i = 0; i < sidelength*sidelength; i++){
    document.getElementById('cell' + i).classList.remove('colored');
  }
  console.log(submitmap);
});