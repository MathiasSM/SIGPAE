$(document).ready(function () {
  $('#bt-t').on('click', function () {
    $('#tipo').val('T'); $('#main-form').submit()
  })
  $('#bt-i').on('click', function () {
    $('#tipo').val('I'); $('#main-form').submit()
  })
})
