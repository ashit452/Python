
  $(function () {
    $(".tabs").tabs();
    $('#optiondiv').hide();

    
    $(".radio").change(function() {
      $(".radio").not(this).prop('checked', false);
    });

    

    var count=$('[id^=option-row]').length - 1;
    
    $("#add").click(function () {
      count++;
      if (count<10){

          var html = `<tr id="option-row[${count}]">
            {% for i in language %}
              <td>
                <input class="form-control" type="text" id="option{{i.locale}}['${count}'][opname]" name="option{{i.locale}}['${count}'][opname]" required>
                <input class="form-control" type="hidden" id="option{{i.locale}}['${count}'][oplanguage]" name="option{{i.locale}}['${count}'][oplanguage]" value="{{i.locale}}">
              </td>
            {% endfor %}
            <td><input class="form-control" type="text" id="option['${count}'][customoption]" name="option['${count}'][customoption]" required></td>
            
            <td><input class="form-control" type="number" id"option['${count}'][order]" name="option['${count}'][order]" required></td>
            
            <td><input type="radio" class="radio" id="option['${count}'][default]" name="option['${count}'][default]" ></td>
            <td><img src="{% static 'admin/images/delete.png' %}" height="30px" width="30px" class="delete"></td>
          </tr>`;
          
          $("#tbl").append(html);
          
      }

    
    $(".delete").click(function(){
      
      $(event.target).closest("tr").remove();
            
    });

    $(".radio").change(function() {
      $(".radio").not(this).prop('checked', false);
    });
      
      
    });

    var dltcount=0;
    $(".delete").click(function(){
      var dltId = $(this).parent().attr('id');
      if(dltId != undefined){
      var dlt = `<input type="hidden" id="deleterows['${dltcount}']" name="deletedata['${dltcount}']" value="${dltId}">`
      $("#tbl").append(dlt);
      }
      $(event.target).closest("tr").remove();
      dltcount++;      
    });

    
    

    var arr = ['radio','select','multiselect','checkbox']

    if(jQuery.inArray($("#inputtype").val(),arr) != -1){
        $("#optiondiv").show()
        $("#option-row td input").prop('required',true);
      }
      else{
        $("#optiondiv").hide()
        $("#option-row td input").prop('required',false);
      }

    $("#inputtype").change(function(){
      if(jQuery.inArray($("#inputtype").val(),arr) != -1){
        $("#optiondiv").show()
        $("#option-row td input").prop('required',true);
      }
      else{
        $("#optiondiv").hide()
        $("#option-row td input").prop('required',false);
        
      }
    });
  });

  