$('#select_all').click(function(event){
  if(this.checked){
    $('form :checkbox').each(
      function(){
        this.checked = true;
      }
    )
  } else {
    $('form :checkbox').each(
      function(){
        this.checked = false;
      }
    )
  }
});
