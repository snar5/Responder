from scripts import * 

page_header = """
<html>
	<head><title>Responder Status</title>
	<link href='www/jquery/jquery-ui.css' rel='stylesheet'>
	<link href='www/jquery/custom.css' rel='stylesheet'>
	<style>
	button:focus {outline:0 !important;}

	div.container {width: 100%;border: 2px solid #3F3F3F;}
	header, footer {
		padding: 1em;
		color: white;
		background-color: #040404;
		clear: left;   text-align: center;}


	nav {
	    float: left;
	    max-width: 200px;
	    height: 800px;
	    margin: 5px;
	    padding: 1em;
	}
	nav ul {
		list-style-type: none;
		padding: 0;
	}
	nav h4 {
	    background-color: #5B6073; 
            border: 1px solid green; 
            color: white; 
            padding: 10px 10px; 
            cursor: pointer;

	}

	h4 { 
	background-color: #5B6073;
	border: 1px solid green;
	color: white;
	padding: 10px 10px;
	cursor: pointer;
	}
	nav ul a {
	    text-decoration: none;
	}
	article {
    		margin-left: 170px;
		border-left: 1px solid gray;
		padding: 1em;
		overflow: hidden;}
	table {
 		font-family: arial, sans-serif;
		border-collapse: collapse;
		width: 100%;}

	td, th {
		border: 1px solid #dddddd;
		text-align: left;
		padding: 8px;
		}
	tr:nth-child(even) {
		background-color: #dddddd;
		}
    .menu {
      color: white;
      background-color: #6E6E6E;
      text-align: left;
      height: 40;
      border: 1px solid black;
      margin: 5px;
      padding: 5px;

    }

    .menu button {
          background-color: #3F3F3F; /* Green background */
          border: 1px solid green; /* Green border */
          color: white; /* White text */
          padding: 10px 24px; /* Some padding */
          cursor: pointer; /* Pointer/hand icon */
          float: left; /* Float the buttons side by side */
      }

    .menu:after {
      content:"";
      clear: both;
          display: table;
      }

    .menu button:not(:last-child) {
      border-right: none;
      }

    .menu button:hover {
      background-color: #3e8e41;
      }
#icons {
		margin: 0;
		padding: 0;
	}
	#icons li {
		margin: 2px;
		position: relative;
		padding: 4px 0;
		cursor: pointer;
		float: left;
		list-style: none;
	}
	#icons span.ui-icon {
		float: left;
		margin: 0 4px;
	}
	.r-badge {
  		display: none;
  		background: #BA070F;
  		color: #fff;
  		padding: 1px 7px;
  		position: absolute;
  		right: 4px;
  		top: -12px;
  		z-index: 999;
  		border-radius: .8em;
  		border: 2px solid #fff;
	}

</style>
"""
page_header = page_header 
page_header = page_header + page_scripts + "</head>" 

