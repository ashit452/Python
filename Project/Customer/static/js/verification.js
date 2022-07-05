var oldemail = `{{ customerDetails.0.email }}`;
    var verification = `{{ customerDetails.0.emailVarificationDate }}`;
    console.log("old",oldemail,verification);
    $("#email").change(function(){
      $("#verifycheckbox").remove();
      if (oldemail != $("#email").val()){
        
        var verify = `<div class="form-check form-check-inline m-4" id="verifycheckbox">
                        <input class="form-check-input" type="checkbox" id="verified" name="verified">
                        <label class="form-check-label" for="verified"><strong>Verify</strong></label>
                      </div>
                      `;
        $("#customer #checkboxes").append(verify);
        }
        else if(oldemail == $("#email").val() && verification == "None"){
          var verify = `<div class="form-check form-check-inline m-4" id="verifycheckbox">
                          <input class="form-check-input" type="checkbox" id="verified" name="verified">
                          <label class="form-check-label" for="verified"><strong>Verify</strong></label>
                        </div>`;
          $("#customer #checkboxes").append(verify);
        }
    });