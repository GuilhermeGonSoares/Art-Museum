const input = document.querySelector('input');
const output = document.querySelector('.output');
const outputContainer = document.querySelector('.container');
console.log("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
function resize_to_fit() {
  let fontSize = window.getComputedStyle(output).fontSize;
  output.style.fontSize = (parseFloat(fontSize) - 1) + 'px';
  
  if(output.clientHeight >= outputContainer.clientHeight){
    resize_to_fit();
  }
}

function processInput() { 
  output.innerHTML =this.value;
  output.style.fontSize = '200px'; // Default font size
  resize_to_fit();
}

input.addEventListener('input', processInput);

/* <input type="text" placeholder="Add text input here" style="margin: 10px; width:50%;">

<div id="outer" class="container" 
style="width:80%; height:100px; border:2px solid red; font-size:20px;">
  
<div class="output" style="word-break: break-all; word-wrap: break-word;">
</div>

</div> */