function openNav() {
	if(document.getElementById("mySidenav").style.height == "0px")
		document.getElementById("mySidenav").style.height = "300px";
	else
		document.getElementById("mySidenav").style.height = "0";
}

/* Set the width of the side navigation to 0 */
function closeNav() {
    document.getElementById("mySidenav").style.display = "none";
}
function menu1()
{
	if(document.getElementById("personal").style.display=="none")
	{
		document.getElementById("personal").style.display="block";
		document.getElementById("personal").style.marginTop="-8px";
		document.getElementById("personal").style.width=document.getElementById("ele2").getBoundingClientRect().width+"px";
	}
	else
		document.getElementById("personal").style.display="none";
}
function set_pos()
{
	document.getElementById("body_item").style.marginTop=(document.getElementById("ele2").getBoundingClientRect().bottom+8)+"px";

}
$(document).ready(function(){
$(function() {
    $('#submit').bind('click', function() {
			$("#myModal").modal("show");
      $.getJSON($SCRIPT_ROOT + '/add_user', {
        a: $('#email').val(),
        b: $('#fname').val(),
		c: $('#lname').val(),
		d: $('#id').val(),
		e: $('#type').val()
      },
	  function(data) {
		  $("#myModal").modal("hide");
        alert(data.msg)
      });
	  $('#email').val("");
	  $('#fname').val("");
	  $('#lname').val("");
	  $('#id').val("");
	  
      return false;
    });
	$('#submit1').bind('click', function() {
		$("#myModal").modal("show");
      $.getJSON($SCRIPT_ROOT + '/add_user', {
        a: $('#email1').val(),
        b: $('#fname1').val(),
		c: $('#lname1').val(),
		d: $('#id4').val(),
		e: $('#type1').val()
      }, function(data) {
		  $("#myModal").modal("hide");
        alert(data.msg)
      });
	  
	  $('#email1').val("");
	  $('#fname1').val("");
	  $('#lname1').val("");
	  $('#id4').val("");
      return false;
    });
	$('#submit2').bind('click', function() {
		$("#myModal").modal("show");
      $.getJSON($SCRIPT_ROOT + '/add_user', {
        a: $('#email2').val(),
        b: $('#fname2').val(),
		c: $('#lname2').val(),
		d: $('#id2').val(),
		e: $('#type2').val()
      }, function(data) {
		  $("#myModal").modal("hide");
        alert(data.msg)
      });
	  
	  $('#email2').val("");
	  $('#fname2').val("");
	  $('#lname2').val("");
	  $('#id2').val("");
      return false;
    });
	$('#submit3').bind('click', function() {
		$("#myModal").modal("show");
      $.getJSON($SCRIPT_ROOT + '/add_user', {
        a: $('#email3').val(),
        b: $('#fname3').val(),
		c: $('#lname3').val(),
		d: $('#id3').val(),
		e: $('#type3').val()
      }, function(data) {
		  $("#myModal").modal("hide");
        alert(data.msg)
      });
	  
	  $('#email3').val("");
	  $('#fname3').val("");
	  $('#lname3').val("");
	  $('#id3').val("");
      return false;
    });
  });
  

});

