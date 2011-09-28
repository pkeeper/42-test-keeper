$(document).ready(function() { 
    var options = { 
        target:        '#foutput',   // target element(s) to be updated with server response 
        beforeSubmit:  showRequest,  // pre-submit callback 
        success:       showResponse,  // post-submit callback 
 
        // other available options: 
        //url:       url         // override for form's 'action' attribute 
        //type:      type        // 'get' or 'post', override for form's 'method' attribute 
        //dataType:  null        // 'xml', 'script', or 'json' (expected server response type) 
        clearForm: false,       // clear all form fields after successful submit 
        resetForm: false        // reset the form after successful submit 
 
        // $.ajax options can be used here too, for example: 
        //timeout:   3000 
    }; 
  
    // bind form using 'ajaxForm' 
    $('#form').ajaxForm(options); 
}); 
 
// pre-submit callback 
function showRequest(formData, jqForm, options) { 
    // formData is an array; here we use $.param to convert it to a string to display it 
    // but the form plugin does this for you automatically when it submits the data 
    var queryString = $.param(formData); 
 
    // jqForm is a jQuery object encapsulating the form element.  To access the 
    // DOM element for the form do this: 
    // var formElement = jqForm[0]; 
 
	$("input").attr("disabled", "disabled");
	$("textarea").attr("disabled", "disabled");
    $("#foutput").html("Submitig form...");
 
    // here we could return false to prevent the form from being submitted; 
    // returning anything other than false will allow the form submit to continue 
    return true; 
} 
 
// post-submit callback 
function showResponse(data, statusText, xhr, $form)  { 
    // for normal html responses, the first argument to the success callback 
    // is the XMLHttpRequest object's responseText property 
 
    // if the ajaxSubmit method was passed an Options Object with the dataType 
    // property set to 'xml' then the first argument to the success callback 
    // is the XMLHttpRequest object's responseXML property 
 
    // if the ajaxSubmit method was passed an Options Object with the dataType 
    // property set to 'json' then the first argument to the success callback 
    // is the json data object returned by the server 
    
    console.log(data);
    // Clear all error span's
    $('span.error').remove();
    if (data.status != 'ok') {
        // validation fail
        // Show profile errors
        for (field in data.profile_errors) {
            html = '<span class="error">' 
            for (i in data.profile_errors[field]) {
                html += data.profile_errors[field][i] + '<br />';
            }
            html += '</span>'
            $('#id_' + field).after(html);
        };
        // Show contacts errors
        for (id in data.contacts_errors) {
        for (field in data.contacts_errors[id]) {
            html = '<span class="error">' 
            for (i in data.contacts_errors[id][field]) {
                html += data.contacts_errors[id][field][i] + '<br />';
            }
            html += '</span>'
            $('#id_form-' + id + '-'+ field).after(html);
        };
        	id += 1;
        };
        
        // Show status message
    	$('#foutput').text('Form is not valid! <br/>' + 
    										data.contacts_nonform_errors)
    }
    else {
    	$('#foutput').text('Form send and valid!')
    	// need to reload formset after successfull change for form consistency
    	window.setTimeout(location.reload(), 2000);
    };

	$("input").removeAttr('disabled');
	$("textarea").removeAttr('disabled');
} 