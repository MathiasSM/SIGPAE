$(document).ready(function() {
    $("#fecha_año").attr({
        "min" : 1969,
        "max" : ((new Date).getFullYear() + 1)
    })
    $("#fecha_año").on('change invalid', function() {
        var textfield = $(this).get(0);
        textfield.setCustomValidity('');
        if (textfield.validity.rangeUnderflow) {
            textfield.setCustomValidity('El año ingresado debe ser mayor a 1969');
        }
        if (textfield.validity.rangeOverflow) {
            textfield.setCustomValidity('El año ingresado debe ser menor a ' + ((new Date).getFullYear() + 1));
        }

        if (textfield.validity.valueMissing) {
          textfield.setCustomValidity('Este campo es obligatorio');  
        }
    })
})