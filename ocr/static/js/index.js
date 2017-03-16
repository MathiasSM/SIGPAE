$(document).ready(function () {
  var form = $('#main-form')
  $('#bt-t').on('click', function () {
    $('#tipo').val('T');
    if(form[0].checkValidity()){
      form.submit()
    }
    else{
      //SHOW ERRORS HERE
    }
  })
  $('#bt-i').on('click', function () {
    $('#tipo').val('I');
    if(form[0].checkValidity()){
      form.submit()
    }
    else{
      //SHOW ERRORS HERE
    }
  })
})
