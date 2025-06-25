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


// clear the board
document.getElementById('clear').addEventListener('click', function(){
  for(var i = 0; i < sidelength*sidelength; i++){
    document.getElementById('cell' + i).classList.remove('colored');
  }
});

// clear the board & submit pixel map as a nested array
var submitmap = [];
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

  document.getElementById('textdisplay').textContent = 'Analyzing...';

  

  fetch("/read", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({'map': submitmap, 'label': 'foo'})
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById('textdisplay').textContent = 'Your drawing had ' + data.result + ' pixels.';
  });
});