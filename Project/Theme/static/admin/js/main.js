$(function(){
   
    $(".chosen-select").chosen(
        
        $("#bannergroup").change(function(){
            
            // var rowCount = $("#bannerinfo tr").length-1;
            thisSelect = $(this).val();
            thisSelectedvals = []
            $("#bannergroup option:selected").each(function()
            {
                thisSelectedvals.push($.trim(($(this).text())));
            });
            // var dltcount = 0
            $("#bannergroup option:not(:selected)").each(function()
            {
                var dltId = $(".added-"+$(this).val()+" [id^=bannerimgid]").val();
                if(dltId != undefined){
                var dlt = `<input type="hidden" id="deletedata[0]" name="deletedata[0]" value="${dltId}">`
                $("#banner").append(dlt);
                }
                // dltcount++;
                $(".added-"+$(this).val()+"").remove();
                
            });
            
            
            
            var countselected=thisSelect.length;
            console.log("selected",thisSelect);

            
            
            for(i=0;i<countselected;i++){
                console.log($(".added-"+thisSelect[i]+"").length);
               
                if($(".added-"+thisSelect[i]+"").length>0){
                }else {
                    
                var html = `<tr class="added-${thisSelect[i]}">
                <td>${thisSelectedvals[i]}</td>

                <td><div class="row"><a id="imglink" class="col-md-2" href="#"><img id="img" src ="#" style="height:50px; width:50px;"></a>
                <input type="file" class="form-control col-md-8 mt-2" id="bannerimage[${thisSelect[i]}]" name="bannerimage[${thisSelect[i]}]" onchange="readURL(this);" accept="image/*" required>
                </div></td>
                <td><input type="text" class="form-control" id="url[${thisSelect[i]}]" name="url[${thisSelect[i]}]" required></td>
                <input type="hidden"  id="bannergrpid[${thisSelect[i]}]" name="bannergrpid[${thisSelect[i]}]" value="${thisSelect[i]}" required>
                </tr>`;
                
                $("#bannerinfo").append(html);
                
                }
            }
            
        })
        
    ); 
    })