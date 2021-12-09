$('.message .close')
  .on('click', function() {
    $(this)
      .closest('.message')
      .transition('fade')
    ;
  })
;


$(document).ready(function(){
    $('#modal-btn').click(function(){
        $('.ui.modal')
        .modal('show')
        ;
    })
})



$( document ).ready(function() {
  let display = false
  $(".cmt_btn").click(function () {
      if (display==="none") {
          $(this).next(".comment-box").show("slow");
          display="block"
      } else {
          $(this).next(".comment-box").hide("slow");
          display="none"
      }
  });
});

$( document ).ready(function() {
    $('.ui.dropdown').dropdown('hide');
    $('#dropdown_id').click(function(){
      $('.ui.dropdown')
      .dropdown('show')
    })
});