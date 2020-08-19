var submit = document.getElementById('button');
var input = document.getElementById('email');
var span = document.getElementById('message');
submit.addEventListener('click',()=>{
  if(input.value.length == 0){
    submit.disabled = true;
    input.style.borderColor = 'red';
    span.innerHTML = 'Field is empty!';
  }
});
input.addEventListener('change',()=>{
  if(input.value.length > 0){
    submit.disabled = false;
    input.style.borderColor = '';
    span.innerHTML = '';
  }
});
