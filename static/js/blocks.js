var well_circle = document.getElementById('well');
var notwell_circle = document.getElementById('notwell');
var radius = well_circle.r.baseVal.value;
var circumference = radius * 2 * Math.PI;

well_circle.style.strokeDasharray = `${circumference} ${circumference}`;
well_circle.style.strokeDashoffset = `${circumference}`;
notwell_circle.style.strokeDasharray = `${circumference} ${circumference}`;
notwell_circle.style.strokeDashoffset = `${circumference}`;

function setProgress(percent) {
    const offset = circumference - percent / 100 * circumference;
    well_circle.style.strokeDashoffset = -offset;
    notwell_circle.style.strokeDashoffset = offset;
}

setProgress(80);