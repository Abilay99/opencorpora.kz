
var MAX_BYTES = 1048576; // 1MB

function dragEnter(event) {
    //console.log('dragEnter', event);
    event.stopPropagation();
    event.preventDefault();
}

function dragExit(event) {
    //console.log('dragExit', event);
    event.stopPropagation();
    event.preventDefault();
}

function dragOver(event) {
    //console.log('dragOver', event);
    event.stopPropagation();
    event.preventDefault();
}

function drop(event) {

    //console.log('drop', event);
    event.stopPropagation();
    event.preventDefault();

    var data = event.dataTransfer;
    var files = data.files;
    var file;
    var reader;

    for (var i = 0; i < files.length; i++) {
        file = files[i];
        //console.log(file, file.fileName);
        //$('#filename').text('BINARY: ' + file.fileName);
    	//$('#result').name('FIELD: ' + file.fileName);
        //$('#text').attr('name', file.fileName);
        reader = new FileReader();
        reader.onloadend = onFileLoaded;
        reader.readAsText(file, 'utf-8')
        //reader.readAsDataURL(file);
    }
}

function onFileLoaded(event) {
    //console.log('onFileLoaded', event);
    var initialData = event.currentTarget.result.substr(0, MAX_BYTES);
    $('#text').text(initialData);
    //$('#result').name(initialData);
    //$("#result").name(result#result);
}

var dropArea = $("#text").get(0);

dropArea.addEventListener("dragenter", dragEnter, false);
dropArea.addEventListener("dragexit", dragExit, false);
dropArea.addEventListener("dragover", dragOver, false);
dropArea.addEventListener("drop", drop, false);