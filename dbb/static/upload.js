Dropzone.options.myDropzone = {
    init: function() {this.on("drop", newClothing)},
    uploadMultiple: false,
    parallelUploads: 2,
    paramName: "file", // The name that will be used to transfer the file
    maxFilesize: 3, // MB
    acceptedFiles: "image/*, audio/*, video/*, text/*, application/*",
    maxFiles: 1,
    dictDefaultMessage: "Drop a picture of your clothing  here or click to upload.", // message display on drop area
    dictFallbackMessage: "Your browser does not support drag'n'drop file uploads.",
    dictInvalidFileType: "You can't upload files of this type.",
    dictFileTooBig: "File is too big . Max filesize: MiB.",
    dictResponseError: "Server error: ",
    dictMaxFilesExceeded: "Your can't upload any more files.",
    // renameFilename: cleanFilename,
};

var newClothing = function() {
    console.log("new clothes");
    var editInfo = document.getElementById("editInfo");
    editInfo.innerHTML = `
	<center>
	<form action="/upload_clothing">
	<br>
	Name:
	<br>
	<input type="text" name="name" value="Red shirt">
	<br>
	Type of clothing:
	<br>
	<select name="type">
	<option value="top">Top</option>
	<option value="pants">Pants</option>
	<option value="shoes">Shoes</option>
	</select>
	<br><br>
	<input type="submit" value="Submit">
	</form>
	</center>
	`;
}

