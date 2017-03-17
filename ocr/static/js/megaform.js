$(document).ready(function () {
  $('#field-objetivosE').hide()
  $('#btn-sep-obj').on('click', function (e) {
    e.preventDefault()
    $('#field-objetivosE').show()
  })
  $('#btn-mix-obj').on('click', function (e) {
    e.preventDefault()
    var extra = $('#field-objetivosE')
    var cont = extra.children('textarea').val()
    console.log(cont)
    extra.children('textarea').val('')
    extra.hide()
    var gen = $('#field-objetivos').children('textarea')
    gen.val( gen.val()+'\n'+cont )
  })
})
