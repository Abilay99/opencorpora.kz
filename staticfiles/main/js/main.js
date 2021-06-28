var selectedshtml = [];
var idfordownload;
$(document).ready(function($){
    $('input[name="source"]').keyup(function(event) {
        if (event.keyCode === 13) {
            $("#Search").click();
        }
    });
	$('.cd-filter-block h4').on('click', function(){
		$(this).toggleClass('closed').siblings('.cd-filter-content').slideToggle(300);
	});
    
	$("select#selectThis").on('change', function(){
        var selected = $("option:selected", this);
        var selectedval = $("option:selected", this).val();
        var divselected = "div#"+selectedval;
        $(divselected).css({display : "inline-block"});
        selectedshtml.push(selected.html());
        $(selected).attr('disabled', true);
        $(this).val('default');
    });
    $("#checkbox1").click(function(){
    	if($(this).is(':checked')){
    		$(this).prop('checked', true);
    	}
    	else{
    		$(this).prop('checked', false);
    	}
    });
    $("#checkbox2").click(function(){
    	if($(this).is(':checked')){
    		$(this).prop('checked', true);
    	}
    	else{
    		$(this).prop('checked', false);
    	}
    });
    $("#checkbox3").click(function(){
    	if($(this).is(':checked')){
    		$(this).prop('checked', true);
    	}
    	else{
    		$(this).prop('checked', false);
    	}
    });
    
});
var sendfromfilter = function(e){
    if(e.val().toString().length > 0){
    $.ajax({
        url: "index1",
        type: "GET",
        data: {'source' : e.val(), 'selectedshtml' : selectedshtml},
        dataType: "JSON"
    }).done(function(data){
        window.location.href = "http://127.0.0.1:8000/index1?source="+ data.source+"&filters="+data.selectedshtml;
    });
    }
}
var sendforgetid = function(e){
    $.post('handlerGET', 
        {'id' : e.id}, 
        function(response) { idfordownload = response.id; }, "JSON");
} 
var sendforgetfile = function(type){
    $.post('example',
        {'id_download' : idfordownload, 'type' : type},
        function(response){ window.location.href = "http://127.0.0.1:8000/download?name="+response.filename;  },"JSON");
}


							    
