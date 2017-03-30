$(document).ready(function () {
  var adicionalCNT = $("#adicionalCNT");      // ID del contenedor de los campos adicionales
  var seccionCNT = $("#seccionCNT");          // ID del contenedor de las secciones
  var addAdicional = $("#agregarAdicional");  // ID del botón para añadir campo adicional
  var addSeccion = $("#agregarSeccion");      // ID del botón para añadir seccion
  var adicionalCount = 0;                     // Contador de campos adicionales
  var seccionCount = 1;                       // Contador de secciones
  var referenciaCount = [1];                  // Arreglo para contar las referencias (Por defecto 1)

  if(/^\s*$/.test($('#objetivosE').val())){
    $('#field-objetivosE').hide();
  }
  else{
    $('#btn-sep-obj').hide();
  }

  $('#btn-sep-obj').on('click', function (e) {
    e.preventDefault();
    $('#btn-sep-obj').hide();
    $('#field-objetivosE').show();
  });

  $('#btn-mix-obj').on('click', function (e) {
    e.preventDefault();
    swal({
        title: "¿Está seguro de que desea combinar los campos?",
        text: "Esta acción no se puede deshacer",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#1565C0",
        confirmButtonText: "Combinar",
        cancelButtonText: "Cancelar",
        closeOnConfirm: false,
        html: false
    }, function(isConfirm) {
        if (isConfirm) {
          $('#btn-sep-obj').show();
          var extra = $('#field-objetivosE');
          var cont = extra.children('textarea').val();
          console.log(cont);
          extra.children('textarea').val('');
          extra.hide();
          var gen = $('#field-objetivos').children('textarea');
          gen.val( gen.val()+'\n'+cont );
          swal("",
          "Se han combinado los campos de manera exitosa",
          "success");
        }
    });
  });
  
  // Función para los botones para añadir unidades externas
  $("body").on("click","button.agregarReferencia", function() {
    var num1 = parseInt(this.id.match(/\d+/g), 10 );   // Obtener el número de seccion correspondiente
    var referenciaCNT = "#referenciaCNT" + num1;       // Generar el identificador al contenedor de la unidad correspondiente

    referenciaCount[num1-1]++;                         // Aumentar el contador de phones para el referencia permitente
    var num2 = referenciaCount[num1-1];                // Variable auxiliar para la sustitucion en el html de abajo

    // Inserción del html
    $(referenciaCNT).append(
    '<hr>\
    <div id="referencia'+num1+'-'+num2+'">\
      <label><small>Referencia '+num1+'.'+num2+'</small></label>\
      <input type="text" name="titulo'+num1+'-'+num2+'" placeholder="Título de la referencia">\
      <label><small>Autor</small></label>\
      <input type="text" name="autor-'+num1+'" placeholder="Autor de la referencia">\
      <label><small>Editorial</small></label>\
      <input type="text" name="editorial'+num1+'-'+num2+'" placeholder="Editorial de la referencia">\
      <label><small>Edición</small></label>\
      <input type="text" name="edicion'+num1+'-'+num2+'" placeholder="Edición de la referencia">\
      <label><small>Notas</small></label>\
      <input type="text" name="notas'+num1+'-'+num2+'" placeholder="Notas de la referencia">\
    </div>');
  });

  // Función para el botón para añadir campos adicionales
  $(addAdicional).on('click', function() {
    adicionalCount++;           // Aumentar el contador de campos adicionales
    var num1 = adicionalCount;  // Variable auxiliar para la sustitucion en el html de abajo

    // Inserción del html
    $(adicionalCNT).append(
    '<hr>\
    <h3>Campo adicional #'+num1+'</h3>\
    <div id="adicional'+num1+'">\
      <label><small>Tipo:</small></label>\
      <input type="text" name="tipo'+num1+'" placeholder="Tipo de campo adicional">\
      <label><small>Valor:</small></label>\
      <input type="text" name="valor'+num1+'" placeholder="Valor de campo adicional">\
    </div>');
  });

  // Función para el botón para añadir secciones
  $(addSeccion).on('click', function() {
    seccionCount++;                                 // Aumentar el contador de secciones
    referenciaCount = referenciaCount.concat([1]);  // Agregar un nuevo slot contador de referencias

    var num1 = seccionCount;                        // Variable auxiliar para la sustitucion en el html de abajo
    var num2 = referenciaCount[num1-1];             // Variable auxiliar para la sustitucion en el html de abajo

    // Inserción del html
    $(seccionCNT).append(
    '<hr>\
    <div id="seccion'+num1+'">\
      <label>Sección '+num1+'</label>\
      <input type="text" name="seccionNombre'+num1+'" placeholder="Nombre de la sección">\
      <div align="left"><label>Referencias</label></div>\
      <div id="referenciaCNT'+num1+'">\
        <div id="referencia'+num1+'-'+num2+'">\
          <label><small>Referencia '+num1+'.'+num2+'</small></label>\
          <input type="text" name="titulo'+num1+'-'+num2+'" placeholder="Título de la referencia">\
          <label><small>Autor</small></label>\
          <input type="text" name="autor-'+num1+'" placeholder="Autor de la referencia">\
          <label><small>Editorial</small></label>\
          <input type="text" name="editorial'+num1+'-'+num2+'" placeholder="Editorial de la referencia">\
          <label><small>Edición</small></label>\
          <input type="text" name="edicion'+num1+'-'+num2+'" placeholder="Edición de la referencia">\
          <label><small>Notas</small></label>\
          <input type="text" name="notas'+num1+'-'+num2+'" placeholder="Notas de la referencia">\
        </div>\
      </div>\
      <div align="right">\
        <button id="agregarReferencia'+num1+'" class="agregarReferencia" type="button" style="float: right;"><small>Agregar referencia</small></button>\
      </div>\
      </br>\
      </br>\
    </div>');
  });
});
