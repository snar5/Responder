page_footer = """
<footer>Happy Hunting </footer> 

<div id="hashModal" class="modal">
  <div class="modal-content">
    <div class="modal-header">
      <span class="close">&times;</span>
      <h2>Captured Hashes</h2>
    </div>
    <div class="modal-body">
      <p id='dumped_hashes'></p>
    </div>
    <div class="modal-footer">
      <h3>Copy the hashes from above</h3>
    </div>
  </div>
</div>

<script>

// Modal Window Stuff in this section Get the modal
var modal = document.getElementById('hashModal');
var btnHash = document.getElementById("btnHash");
var span = document.getElementsByClassName("close")[0];
var btnClearCounters = document.getElementById("btnClearCounters");

btnHash.onclick = function() {
    doDumpHashes();
    modal.style.display = "block";
}

btnClearCounters.onclick = function() { 
	var ans = window.confirm("This Action Cannont be Undone!"); 
	if (ans) {
		doClearPoisons(); 
		}
			
} 

span.onclick = function() {
    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

// End Modal Window
 
$( "#tabs").tabs(); 
$( "#accordion" ).accordion();
</script>
</div>
</body>
</html>
"""
