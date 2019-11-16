var el = x => document.getElementById(x);

function validateForm() {
    var txt = el("usersline").value;
    var lenlines = el("lenlines").value;
    var lenchars = el("lenchars").value;
    if (txt.length === 0) alert("Please enter some words!");
    if (lenlines.length === 0 || lenchars.length === 0) alert("Please enter an integer!");
}  