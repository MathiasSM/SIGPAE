$(document).ready(function() {
    var x = parseInt($("#horas_teoria").val()) +  parseInt($("#horas_practica").val()) + parseInt($("#horas_laboratorio").val())
    $("#codigo").attr({
        "pattern" : "[A-Za-z]{2}[0-9]{4}"
    })
    $("#codigo").on('input', function() {
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
    $("#fecha_año").on('change invalid input', function() {
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
    $("#creditos").on('input', function() {

        var textfield = $(this).get(0);
        textfield.setCustomValidity('');
        if (textfield.validity.rangeUnderflow) {
            textfield.setCustomValidity('Cantidad de créditos debe ser positiva');
        }
        if (textfield.validity.rangeOverflow) {
            textfield.setCustomValidity('Cantidad de créditos debe ser menor o igual a 16');
        }
    })

    $("#horas_teoria").attr({
        "max" : 40
    })
    $("#horas_teoria").on('input', function() {
        var textfield = $(this).get(0);
        textfield.setCustomValidity('');
        if (textfield.validity.rangeUnderflow) {
            textfield.setCustomValidity('Cantidad de horas de teoría debe ser positiva');
        }
        if (textfield.validity.rangeOverflow) {
            textfield.setCustomValidity('Cantidad de horas de teoría debe ser menor o igual a 40');
        }
    })

    $("#horas_practica").attr({
        "max" : 40
    })
    $("#horas_practica").on('input', function() {
        var textfield = $(this).get(0);
        textfield.setCustomValidity('');
        if (textfield.validity.rangeUnderflow) {
            textfield.setCustomValidity('Cantidad de horas de práctica debe ser positiva');
        }
        if (textfield.validity.rangeOverflow) {
            textfield.setCustomValidity('Cantidad de horas de práctica debe ser menor o igual a 40');
        }
    })

    $("#horas_laboratorio").attr({
        "max" : 40
    })
    $("#horas_laboratorio").on('input', function() {
        var textfield = $(this).get(0);
        textfield.setCustomValidity('');
        if (textfield.validity.rangeUnderflow) {
            textfield.setCustomValidity('Cantidad de horas de laboratorio debe ser positiva');
        }
        if (textfield.validity.rangeOverflow) {
            textfield.setCustomValidity('Cantidad de horas de laboratorio debe ser menor o igual a 40');
        }
    })
    
    $("#instancia").on('change invalid', function() {
        var textfield = $(this).get(0);
        textfield.setCustomValidity('');
        if (textfield.validity.valueMissing) {
          textfield.setCustomValidity('Este campo es obligatorio');
        }
    })
    
})
$(this).validate({
    submitHandler: function(form) {
        var x = parseInt($("#horas_teoria").val()) +  parseInt($("#horas_practica").val()) + parseInt($("#horas_laboratorio").val());
        if(x > 40) {
            swal({
                title: "¡Horas excedidas!",
                text: "Deben haber menos de 40 horas por materia",
                type: "warning"
            })
            //alert("Total de horas es mayor a 40")
            return false;
        }else{
            form.submit();
        }
    }
})