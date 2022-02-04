Sortable.create(listWithHandle, {
    handle: '.glyphicon-move',
    animation: 150,
    ghostClass: 'ghost',
    dragClass: "chosen"
});

function gotoCourse(id) {
    console.log(id);
    document.location.href = "/course/" + id;
}