function openNav() {
    if (document.getElementById("mySidenav").style.height == "0px")
        document.getElementById("mySidenav").style.height = "300px";
    else
        document.getElementById("mySidenav").style.height = "0";
}

/* Set the width of the side navigation to 0 */
function closeNav() {
    document.getElementById("mySidenav").style.display = "none";
}
function menu1() {
    if (document.getElementById("personal").style.display == "none") {
        document.getElementById("personal").style.display = "block";
        document.getElementById("personal").style.marginTop = "8px";
        document.getElementById("personal").style.width = document.getElementById("ele2").getBoundingClientRect().width + "px";
        //	document.getElementById("sample").value=(document.getElementById("cont-flu").getBoundingClientRect().bottom-8)+"px";
    }
    else
        document.getElementById("personal").style.display = "none";
}
function set_pos() {
    document.getElementById("body_item").style.marginTop = (document.getElementById("cont-flu").getBoundingClientRect().bottom + 8) + "px";
    //document.getElementById("sample").value=(document.getElementById("ele2").getBoundingClientRect().bottom+8)+"px";
}
function view(roll) {
    document.getElementById("search_results").outerHTML = "";
}
function query() {
    var g = document.getElementById("inp1").value;
    var h = document.getElementById("filter").value;
    if (!validate(h, g)) {
        alert("Invalid input for " + h);
        return;
    }

    confirm(String("Search by " + String(h) + "  :  " + String(g)));
    del_rev();
}
function validate(a, b) {
    if (a == "Roll number" && isNaN(b)) {
        return false;
    }
    if (a == "Year" && (b == NaN || b > 2017 && b < 1900))
        return false;
    return true;
}
function create_students() {

}
function del() {
    document.getElementById("inp1").disabled = true;
    document.getElementById("filter").disabled = true;
    document.getElementById("b1").disabled = true;
}
function del_rev() {
    document.getElementById("inp1").disabled = false;
    document.getElementById("filter").disabled = false;
    document.getElementById("b1").disabled = false;
}
function fetch_option(n) {
    confirm(n);
}
function modal1() {
    document.getElementById("modal_test").modal - "show";
}
function htmlToElement(html) {
    var template = document.createElement('template');
    template.innerHTML = html;
    return template.content.firstChild;
}
function load() {
    var G = document.getElementsByClassName("cliqued").length + 1;
    var s = `<tr class="trb well cliqued" onclick="togl(String(${G}),this)">\
								<td class="form-group " >\
									<label>Degree :</label>\
								  </td>\
								  <td class="form-group ">\
	<input type="text" class="form-control" id="name${G}" name="name${G}" placeholder="degree name" required/>\
	<input type="number" step="0.01" class="form-control" id="cgpa${G}" name="cgpa${G}" placeholder="CGPA"/>\
	<input type="text" class="form-control" id="ins${G}" name="ins${G}"  placeholder="Institute"/>\
	<input type="number" class="form-control" id="yr${G}" name="yr${G}"  placeholder="Passing year"/>\
		<input type="hidden" value="-2" name="${G}" id="${G}"/>\
		<input type="hidden" value="0" name="butd${G}" id="butd${G}"/>
		<button  type="button" class="btn btn-danger" onclick="tog('butd${G}',this)" >Delete </button>
								  </td></tr>`;
    s = htmlToElement(s);
    var g = document.getElementById("tby");
    g.insertBefore(s, g.children[(g.children.length - 2)]);
}
function load2() {
    var G = document.getElementsByClassName("cliquedc").length + 1;
    var s = `<tr class="trb well cliquedc" onclick="togl('${G}',this)">
								<td class="form-group " >
									<label>Course :</label>
								  </td>
								  <td class="form-group ">
	<input type="number" class="form-control" id="cid${G}" name="cid${G}"  placeholder="Course id" required/>
	<input type="text" class="form-control" id="cname${G}" name="cname${G}"  placeholder="course name"/>
	 <input type="text" class="form-control" id="ctype${G}" name="ctype${G}"  placeholder="Type"/>
 	<input type="text" class="form-control" id="cduration${G}" name="cduration${G}" placeholder="Duration"/>
	<input type="number" class="form-control" id="cmentorid${G}" name="cmentorid${G}"  placeholder="Current mentor id" />
 	<input type="text" class="form-control" id="cmentor${G}" name="cmentor${G}"  placeholder="Current mentor "/>
		<input type="hidden" value="-2" name="${G}" id="${G}"/>
		<input type="hidden" value="0" name="butc${G}" id="butc${G}"/>
		<button  type="button" class="btn btn-danger" onclick="tog('butc${G}',this)" >Delete </button>
								  </td>
								  </tr>`;
    s = htmlToElement(s);
    var g = document.getElementById("tby");
    g.insertBefore(s, g.children[(g.children.length - 2)]);
}
function load3() {
    var G = document.getElementsByClassName("cliquedc").length + 1;
    var s = `<tr class="trb well cliquedc" onclick="togl('${G}',this)">
								<td class="form-group " >
									<label>Course :</label>
								  </td>
								  <td class="form-group ">
	<input type="number" class="form-control" id="cid${G}" name="cid${G}"  placeholder="Course id" required/>
	<input type="text" class="form-control" id="cname${G}" name="cname${G}"  placeholder="course name"/>
	 <input type="text" class="form-control" id="ctype${G}" name="ctype${G}"  placeholder="Type"/>
 	<input type="text" class="form-control" id="cduration${G}" name="cduration${G}" placeholder="Duration"/>
    <input type="number" class ="form-control" id="cmentorid${G}" name="cmentorid${G}"  placeholder="Current mentor id" style="display:none" />
    <input type="hidden" value="-2" name="${G}" id="${G}"/>
		<input type="hidden" value="0" name="butc${G}" id="butc${G}"/>
		<button  type="button" class="btn btn-danger" onclick="tog('butc${G}',this)" >Delete </button>
								  </td>
								  </tr>`;
    s = htmlToElement(s);
    var g = document.getElementById("tby");
    g.insertBefore(s, g.children[(g.children.length - 2)]);
}
function tog(e, y) {
    var ele = document.getElementById(e);
    ele.value = ele.value == 0 ? 1 : 0;
    if (ele.value == 0) {
        y.innerHTML = "Delete";
        y.setAttribute("class", "btn btn-danger");
    }
    else {
        y.innerHTML = "Do not delete";
        y.setAttribute("class", "btn btn-success");
    }
}
function togl(e, y) {
    var x = document.getElementById(e);
    x.value = x.value == -2 ? -1 : -2;
    if (x.value == -1) {
        y.style.backgroundColor = "orange";
    }
    else {
        y.style.backgroundColor = "";
    }
}
function meh() {
    var g = document.getElementById("cs").appendChild(htmlToElement("<input name='na' type='text' value='none'>"));
}
$(document).ready(function () {
    $("#YES").click(function () {
        $("#modal_test").modal("hide");
    });
    $("#NO").click(function () {
        $("#modal_test").modal("hide");
    });

});