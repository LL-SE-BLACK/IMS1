$(document).ready(function(){
  	$.getJSON("/controllist.php",
			function(data){
				var tt="";
				var count=1;
				var obj;
				var reply;
				$.ajaxSettings.async = false;
				$.each(data.array_device,function(v,k){
					obj={query: "status",ID : k};
					$.getJSON("/search.php",obj,function(data){if(data.check=="Success") reply=data.status; else reply='error';});
					tt+= '<tr class="active"><td>'+(count++)+'</td><td>'+k+'</td><td id="status_'+k+'">'+reply+'</td><td><button type="button" class="btn btn-default" onClick="gorefresh('+k+')" style="width:80px">Refresh</button></td></tr>';
				});
			$("#control_list").html(tt);
			tt="";
			$.each(data.array_ID,function(v,k){
				tt+='<option device_type="'+data.array_type[v]+'" device_id="'+data.array_ID[v]+'">'+data.array_type[v]+' of device #'+data.array_ID[v]+'</option>';
				});
			$("#device_select").html(tt);
			$.ajaxSettings.async = true;
			
			
			
			}
		);
});
function gorefresh(k){
		var obj={query: "status",ID :k};
		$.getJSON("/search.php",
			obj, 
			function(data, status){
				if(data.check=="Success"){ $("#status_"+k).html(data.status); }
				
			}
		);
  	};
function gocontrol(id,type)
{
	var tt="";
	
	if(type=="LCD")
	{
	 tt='Contents: <input id="lcd_control" placeholder="Display on LCD of #'+id+'" />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a id="ctr_btn" class="btn btn-success btn-large"  href=\'javascript: golcd($("#lcd_control").val(),'+id+');\'>DISPLAY</a>';
	}else if(type=="relay")
	{
		tt='Switch the relay of #'+id+': <input type="radio" name="ex" value="on" checked/>on&nbsp;|&nbsp;<input type="radio" name="ex" value="off"/>off&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a id="ctr_btn" class="btn btn-success btn-large"  href=\'javascript: gorelay($("input[name=ex]:checked").val(),'+id+');\'>SWITCH</a>';
	}
	$("#ctr_div").html(tt);
	
};

function golcd(content, id)
{	$("#ctr_btn").attr("disabled",true);
	$("#ctr_btn").html("Pending...");
	$.post("/control.php",{ID:id,type:"LCD",data:content,status:""},function(msg){if(msg=="1") alert("Control success!"); else alert("Control fail, Try again!");});
	$("#ctr_btn").attr("disabled",false);
	$("#ctr_btn").html("DISPLAY");
};
function gorelay(content, id)
{	$("#ctr_btn").attr("disabled",true);
	$("#ctr_btn").html("Pending...");
	$.post("/control.php",{ID:id,type:"relay",data:content,status:content},function(msg){if(msg=="1") alert("Control success!"); else alert("Control fail, Try again!");});
	$("#ctr_btn").attr("disabled",false);
	$("#ctr_btn").html("SWITCH");
}
