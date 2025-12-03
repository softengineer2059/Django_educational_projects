// Отправляет get запрос на edit_view и заменяет содержимое div #modal на содержимое полученного ответа
$(".open_modal_button").on("click",function(){
    var productModalDiv=$("#place_for_modal")
    $.ajax({
        url:$(this).attr("data-url"),
        success:function(data){
        productModalDiv.html(data);
        $("#modal-window").modal('show');
        }
    })
  })
