$(document).ready(function () {
  var adicionalCNT = $("#adicionalCNT");                  // ID del contenedor de los campos adicionales
  var seccionCNT = $("#seccionCNT");                      // ID del contenedor de las secciones
  var addAdicional = $("#agregarAdicional");              // ID del botón para añadir campo adicional
  var addSeccion = $("#agregarSeccion");                  // ID del botón para añadir seccion
  var adicionalCount = $("#adicionalCNT > div").length;    // Contador de campos adicionales

  var seccionCount = $("#seccionCNT > div").length; // Contador de secciones
  console.log(seccionCount);
  var referenciaCount = [];                         // Arreglo para contar las referencias de cada seccion
  var autorCount = [];

  for(var i=0;i<seccionCount;i++){
    referenciaCount = referenciaCount.concat([$("#referenciaCNT"+(i+1)+" > div").length]);
    console.log(" "+referenciaCount[i]);
    autorCount = autorCount.concat([[]]);
    for(var j=0; j<referenciaCount[i]; j++){
      console.log("#autorCNT"+(i+1)+"-"+(j+1)+" > div");
      autorCount[i] = autorCount[i].concat([$("#autorCNT"+(i+1)+"-"+(j+1)+" > div").length]);
      console.log("  "+autorCount[i][j]);
    }
  }

  function anadirUnaSeccion(){
    seccionCount++;                                 // Aumentar el contador de secciones
    referenciaCount = referenciaCount.concat([1]);  // Agregar un nuevo slot contador de referencias
    autorCount = autorCount.concat([[1]]);

    var num1 = seccionCount;                        // Variable auxiliar para la sustitucion en el html de abajo
    var num2 = referenciaCount[num1-1];             // Variable auxiliar para la sustitucion en el html de abajo
    var num3 = autorCount[num1-1][num2-1];

    // Inserción del html
    $(seccionCNT).append(
    '<hr>\
    <div id="seccion'+num1+'">\
      <label>Sección #'+num1+'</label>\
      <input type="hidden" name="seccionpk'+num1+'" value=-1>\
      <input type="text" name="seccionNombre'+num1+'" placeholder="Nombre de la sección"">\
      <div align="left"><label>Referencias</label></div>\
      <div id="referenciaCNT'+num1+'">\
        <div id="referencia'+num1+'-'+num2+'">\
          <label><small>Referencia '+num1+'.'+num2+'</small></label>\
          <input type="hidden" name="referenciapk'+num1+'-'+num2+'" value=-1>\
          <input type="text" name="titulo'+num1+'-'+num2+'" placeholder="Título de la referencia"">\
          <div id="autorCNT'+num1+'-'+num2+'">\
            <div id="autor'+num1+'-'+num2+'-'+num3+'">\
              <label><small>Autor '+num1+'.'+num2+'.'+num3+'</small></label>\
              <input type="hidden" name="autorpk'+num1+'-'+num2+'-'+num3+'" value=-1>\
              <input type="text" name="nombres'+num1+'-'+num2+'-'+num3+'" placeholder="Nombres"">\
              <input type="text" name="apellidos'+num1+'-'+num2+'-'+num3+'" placeholder="Apellidos"">\
            </div>\
          </div>\
          <div align="right">\
            <button id="agregarAutor'+num1+'-'+num2+'" class="agregarAutor" type="button" style="float: right;"><small>Agregar autor</small></button>\
          </div>\
        </br>\
        </br>\
          <label><small>Editorial</small></label>\
          <input type="text" name="editorial'+num1+'-'+num2+'" placeholder="Editorial de la referencia"">\
          <label><small>Edición</small></label>\
          <input type="text" name="edicion'+num1+'-'+num2+'" placeholder="Edición de la referencia"">\
          <label><small>Notas</small></label>\
          <input type="text" name="notas'+num1+'-'+num2+'" placeholder="Notas de la referencia"">\
        </div>\
      </div>\
      <div align="right">\
        <button id="agregarReferencia'+num1+'" class="agregarReferencia" type="button" style="float: right;"><small>Agregar referencia</small></button>\
      </div>\
    </br>\
    </br>\
    </div>');
  }

  if(seccionCount == 0) anadirUnaSeccion();

  if(/^\s*$/.test($('#objetivosE').val())) $('#field-objetivosE').hide()
  else  $('#btn-sep-obj').hide();

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

  // Función para los botones para añadir referencias
  $("body").on("click","button.agregarReferencia", function() {
    var num1 = parseInt(this.id.match(/\d+/g), 10 );   // Obtener el número de seccion correspondiente
    var referenciaCNT = "#referenciaCNT" + num1;       // Generar el identificador al contenedor de la referencia correspondiente

    referenciaCount[num1-1]++;                         // Aumentar el contador de phones para el referencia permitente
    var num2 = referenciaCount[num1-1];                // Variable auxiliar para la sustitucion en el html de abajo

    autorCount[num1-1] = autorCount[num1-1].concat([1]);
    var num3 = autorCount[num1-1][num2-1];

    // Inserción del html
    $(referenciaCNT).append(
    '<hr>\
    <div id="referencia'+num1+'-'+num2+'">\
      <label><small>Referencia '+num1+'.'+num2+'</small></label>\
      <input type="hidden" name="referenciapk'+num1+'-'+num2+'" value=-1>\
      <input type="text" name="titulo'+num1+'-'+num2+'" placeholder="Título de la referencia">\
      <div id="autorCNT'+num1+'-'+num2+'">\
        <div id="autor'+num1+'-'+num2+'-'+num3+'">\
          <label><small>Autor '+num1+'-'+num2+'-'+num3+'</small></label>\
          <input type="hidden" name="autorpk'+num1+'-'+num2+'-'+num3+'" value=-1>\
          <input type="text" name="nombres'+num1+'-'+num2+'-'+num3+'" placeholder="Nombres">\
          <input type="text" name="apellidos'+num1+'-'+num2+'-'+num3+'" placeholder="Apellidos">\
        </div>\
      </div>\
      <div align="right">\
        <button id="agregarAutor'+num1+'-'+num2+'" class="agregarAutor" type="button" style="float: right;"><small>Agregar autor</small></button>\
      </div>\
      </br>\
      </br>\
      <label><small>Editorial</small></label>\
      <input type="text" name="editorial'+num1+'-'+num2+'" placeholder="Editorial de la referencia">\
      <label><small>Edición</small></label>\
      <input type="text" name="edicion'+num1+'-'+num2+'" placeholder="Edición de la referencia">\
      <label><small>Notas</small></label>\
      <input type="text" name="notas'+num1+'-'+num2+'" placeholder="Notas de la referencia">\
    </div>');
  });

  // Función para los botones para añadir autor
  $("body").on("click","button.agregarAutor", function() {

    
    var matchess = this.id.match(/\d+/g);
    num1 = matchess[0];
    num2 = matchess[1];
    var autorCNT = "#autorCNT" + num1 + '-' + num2;
    autorCount[num1-1][num2-1]++;
    var num3 = autorCount[num1-1][num2-1];

    $(autorCNT).append(
      '<hr>\
      <div id="autor'+num1+'-'+num2+'-'+num3+'">\
      <label><small>Autor '+num1+'.'+num2+'.'+num3+'</small></label>\
      <input type="hidden" name="autorpk'+num1+'-'+num2+'-'+num3+'" value=-1>\
      <input type="text" name="nombres'+num1+'-'+num2+'-'+num3+'" placeholder="Nombres"">\
      <input type="text" name="apellidos'+num1+'-'+num2+'-'+num3+'" placeholder="Apellidos"">\
      </div>');
    });

  // Función para el botón para añadir secciones
  $(addSeccion).on('click', function() {
    anadirUnaSeccion();
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
      <input type="hidden" name="pkvalor'+num1+'" value=-1>\
    </div>');
  });
});
