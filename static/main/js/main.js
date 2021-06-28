var selectedshtml = [];
var idfordownload;


$(document).ready(function($){

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
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
$("#Search").click(function(evt){
    (selectedshtml.length > 0) ? $("#filters").val(selectedshtml.join()) : $("#filters").val("all");
    var $form = $('#formsearch');
    
    $form.submit();
});
$('#source').keyup(function(event) {
    if (event.keyCode === 13) {
        $("#Search").click();
    }
});
var sendforgetid = function(e){
    if($('#checkbox1').is(':checked') || $('#checkbox2').is(':checked') || $('#checkbox3').is(':checked'))
    {
        $.ajax({
            url:"/handlerpost/",
            type: "POST",
            data: {'id': e.id},
            success:function(response){ 
                console.log(response.id)
                idfordownload = response.id;
                if($('#checkbox1').is(':checked')){
                    $('#withtoken').html(response.token);
                    $('#token').modal('show');
                }
                if($('#checkbox2').is(':checked')){
                    $('#withlemmas').html(response.lemmas);
                    $('#lemmas').modal('show');
                }
                if($('#checkbox3').is(':checked')){
                    $('#withmorph').html(response.morphanaliz);
                    $('#morph').modal('show');
                }
            },
            complete:function(){},
            error:function (xhr, textStatus, thrownError){
                alert("error doing something");
            }
        });
    }
  }
var sendforgetfile = function(type){
    $.ajax({
        url:"/download/",
        type: "POST",
        data: {'id': idfordownload, 'type': type },
        success:function(response){ 
            var element = document.createElement('a');
            element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(response.fileval));
            element.setAttribute('download', response.title+"("+type+").txt");

            element.style.display = 'none';
            document.body.appendChild(element);

            element.click();

            document.body.removeChild(element);
        },
        complete:function(){},
        error:function (xhr, textStatus, thrownError){
            alert("error doing something");
        }
    });
}
var getsumma = function(e){
    if($(e).attr('class') == 'showsumma'){
        $.ajax({
            url:"/ressumma/",
            type: "POST",
            data: {'id': e.id, 'type': 'show'},
            success:function(response){
                p = $("p#"+response.id);
                p.html(response.summa);
            },
            complete:function(){},
            error:function (xhr, textStatus, thrownError){
                alert("error doing something");
            }
        });
    }
    else{
        $.ajax({
            url:"/ressumma/",
            type: "POST",
            data: {'id': e.id, 'type': 'hide'},
            success:function(response){
                p = $("p#"+response.id);
                p.html(response.summa);
            },
            complete:function(){},
            error:function (xhr, textStatus, thrownError){
                alert("error doing something");
            }
        });
    }
}

var sendexec = function(e){
    if(e.val() != '')
    {
        $(".doload").css({'display':'block'});
        $(".wrap").css({'display':'block'});
        $.ajax({
            url:'/execpost/',
            type: 'POST',
            data: {'text': e.val()},
            success:function(response){ 
                $("#text").text(response.text);
                $("#annotation").html(response.annotation);
                $("#lemma").html(response.lemma);
                $("#keywords").html(response.keywords);
                $("#morph").html(response.morph);
                $("#result").css({'display':'block'});
                $(".doload").css({'display':'none'});
                $(".wrap").css({'display':'none'});
            },
            complete:function(){},
            error:function (xhr, textStatus, thrownError){
                alert("error doing something");
            }
        });
    }
    else{
        alert("Enter text!!!");
    }
}

							    
