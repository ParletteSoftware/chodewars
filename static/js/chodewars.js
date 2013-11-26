$(document).ready(function(){
  //alert("page ready");
});

$(document).on("click", ".transfer", function () {
  //alert("transfer clicked");
  var source_id = $(this).data('source');
  var destination_id = $(this).data('destination');
  var default_amount = $(this).data('amount');
  $("#transfer_modal").find("#from").val(source_id);
  $("#transfer_modal").find("#to").val(destination_id);
  $("#transfer_modal").find("#amount").val(default_amount);
});
