function ShowPassword(id) {
    var x = document.getElementById(id);
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
}

function validate(){
  password1=document.getElementById('password1').value
  password2=document.getElementById('password2').value
  if(password1!=password2){
    alert("Both the passwords are diferent")
    return false;
  }
  else{
    var val=passwordchecker(password1)
    if(!val){
      alert("Not a valid password format, password must be of format:\nAt least 1 uppercase character.\nAt least 1 lowercase character.\nAt least 1 digit.\nAt least 1 special character.\nMinimum 8 characters.")
      return false
      }
    return true
  }
}

function passwordchecker(str){
  if (str.match(/[a-z]/g) && str.match( 
    /[A-Z]/g) && str.match( 
    /[0-9]/g) && str.match( 
    /[^a-zA-Z\d]/g) && str.length >= 8) 
    return true;
  return false;
}