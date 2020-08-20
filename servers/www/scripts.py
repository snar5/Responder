page_scripts = """
<script src="www/jquery/jquery.min.js"></script> 
<script src="www/jquery/jquery-ui.js"></script> 
<script>

$(document).ready(function() {
  setTimeout(doListCapturedCreds, 1000);
  setTimeout(doListPoisoned, 1000);
  setTimeout(doListNames, 1000); 
  getServerIP();
  getPoisonCount();
  getCredTypeCount(); 
  $(document).tooltip(); 
  
});


function getCredTypeCount() { 
	$.ajax ({
                type: 'GET',
                url: '/?option=cred_count',
                success: function(result) {
                        $("#cred_type_count").html(result);
                }
        });
}
function getPoisonCount() { 
	$.ajax ({
		type: 'GET',
		url: '/?option=poison_count',
		success: function(result) {
			$("#server_poisoned").html(result); 
		}
	});
}

function getServerIP() {
	$.ajax ({
		type: 'GET',
		url: '/?option=getIP',
		success: function(result) {
			$("#server_label").html(result); 	
		}
	});

}

function doClearPoisons() {
	
	$.ajax ({
		type: 'GET',
		url: '/?option=clear_poison',
		success: function(result) {
			window.confirm("Counts Cleared");
		}
	});
	
}

function doDumpHashes() {
 
	$.ajax ({
		type: 'GET',
		url: '/?option=dump_hashes',
		success: function(result) {
			$("#dumped_hashes").html(result); 
		}
	});
}

function doListNames() { 
	$.ajax ({
		type: 'GET',
		url: '/?option=request_names',
		success: function(result){
			$("#tabs-3").html(result);
			var cnames = $(result).find('tr').length -1; 
			$("#bubble_names").html(cnames).fadeIn(); 
		}
	});
	setTimeout(doListNames, 5000); 
} 
function doListPoisoned() { 
	$.ajax ({ 
		type: 'GET',
		url: '/?option=poison_details',
		success: function(result){
			$("#tabs-2").html(result);
			var cnames = $(result).find('tr').length -1;
			$("#bubble_poison").html(cnames).fadeIn();  
		}
	});
	setTimeout(doListPoisoned, 5000);  
}

function doListCapturedCreds() {
	$.ajax ({ 
		type: 'GET',
		url: '/?option=captured_creds',
		success: function(result){
			$("#tabs-1").html(result);
			var cnames = $(result).find('tr').length -1;
			$("#bubble_cap_cred").html(cnames).fadeIn(); 
		}
	});
	setTimeout(doListCapturedCreds, 5000);
 
} 


</script>
"""

