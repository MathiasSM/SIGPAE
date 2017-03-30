$(document).ready(function() {
    $("#codigo").attr({
        "pattern" : "[A-Za-z]{2}[0-9]{4}"
    })
    $("#codigo").on('change invalid', function() {
        var textfield = $(this).get(0);
        textfield.setCustomValidity('');
        if (textfield.validity.valueMissing) {
          textfield.setCustomValidity('Este campo es obligatorio');
        }
        if(textfield.validity.patternMismatch) {
            textfield.setCustomValidity('Código en formato incorrecto');
        }
    })
    
    $("#fecha_periodo").on('change invalid', function() {
        var textfield = $(this).get(0);
        textfield.setCustomValidity('');
        if (textfield.validity.valueMissing) {
          textfield.setCustomValidity('Este campo es obligatorio');
        }
    })
    
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
    
    $("#creditos").attr({
        "max" : 16
    })
    $("#creditos").on('change invalid', function() {

        var textfield = $(this).get(0);
        textfield.setCustomValidity('');
        if (textfield.validity.rangeUnderflow) {
            textfield.setCustomValidity('Cantidad de créditos debe ser positiva');
        }
        if (textfield.validity.rangeOverflow) {
            textfield.setCustomValidity('Cantidad de créditos debe ser menor o igual a 16');
        }
    })
    
    $("#instancia").on('change invalid', function() {
        var textfield = $(this).get(0);
        textfield.setCustomValidity('');
        if (textfield.validity.valueMissing) {
          textfield.setCustomValidity('Este campo es obligatorio');
        }
    })
    $("#hours-parent").attr({
        "value" : parseInt($("#horas_teoria").val()) + parseInt($("#horas_practica").val()) + parseInt($("#horas_laboratorio").val()),
        "min" : 0,
        "max" : 40
    })
    $("#hours-parent").on('change invalid', function(){
        var x = $(this).get(0);
        x.setCustomValidity('');
        if(x.validity.rangeOverflow) {
            alert("QUIETO MAMAGUEVO!")
        }
    })
})
