$(document).ready(function () {
  var form = $('#main-form')
  $('#bt-t').on('click', function () {
    $('#tipo').val('T');
    if(form[0].checkValidity()){
      form.submit()
    }
    else{
      var x = $('#django-msgs')
      if (x.length) {
        x.remove()
      }
      $("<div id=\"django-msgs\" class=\"alert-messages\">\
        <ul>\
          <li  id=\"error\" class=\"alert-messages\" >\
            <span>Error: No se ha seleccionado algún archivo </span>\
          </li>\
        </ul>\
      </div>").insertBefore("#bt-t")
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
