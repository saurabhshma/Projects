
<!DOCTYPE html>
<html>
<head>
<title>"upload"</title>
<link rel="stylesheet" href="css/bootstrap.css">
<link rel="stylesheet" href="css/main.css">
</head>
<body>
<br>
<form action="upload.php" method="post" enctype="multipart/form-data">
<div > <input style="height:40px;width:100px" type="submit" value="Home" name="Home" class="btn btn-lg btn-success btn-block"> </div>
</form>
<div class="container">
  <div class="row" style="margin-top:20px">
    <div class="col-xs-12 col-sm-8 col-md-6 col-sm-offset-2 col-md-offset-3">
	<form action="upload.php" method="post" enctype="multipart/form-data">
    <h2 align="center">Select file to upload</h2>
     <hr class="colorgraph">
     <div class="col-xs-6 col-sm-6 col-md-6"> <input align="center" type="file" name="fileToUpload" id="fileToUpload" class="btn btn-lg btn-primary btn-block"> </div>
     <div class="col-xs-6 col-sm-6 col-md-6"> <input type="submit" name="certificate" id="certificate" value="Get Certificates" class="btn btn-lg btn-primary btn-block"> </div>
     <br><br><br>

     <div class="col-xs-6 col-sm-6 col-md-12" > <input type="submit" value="Upload and Verify File" name="submit" class="btn btn-lg btn-success btn-block"> </div>    
    </div>
	</form>
	  </div>
  </div>
</div>
<br><br>

<?php
if(isset($_REQUEST['submit']))
{
	$target_dir = "uploads/";
	$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
	$uploadOk = 1;
	$imageFileType = pathinfo($target_file,PATHINFO_EXTENSION);
	// Check if image file is a actual image or fake image
	if(isset($_POST["submit"])) {
	    $check = filesize($_FILES["fileToUpload"]["tmp_name"]);
	    if($check !== false) {
	        //echo "File is a PDF - " . $check["mime"] . ".";
	        $uploadOk = 1;
	    } else {
	        //$message =  "File is not a PDF.";

	        $uploadOk = 0;
	    }
	}

	$dir = 'uploads/';
	foreach(glob($dir.'*.*') as $v)
	{
    	unlink($v);
	}		
	// Check if file already exists
	if (file_exists($target_file)) {
	    //echo "Sorry, file already exists.";
	    $uploadOk = 0;
	}
	// Check file size
	if ($_FILES["fileToUpload"]["size"] > 5000000) {
	    //echo "Sorry, your file is too large.";
	    $uploadOk = 0;
	}
	// Allow certain file formats
	if($imageFileType != "pdf") {
	    //echo "Sorry, only sPDF files are allowed.";
	    //echo "<script type='text/javascript'>alert("."Sorry, only sPDF files are allowed".");</script>";
	    $uploadOk = 0;
	}
	// Check if $uploadOk is set to 0 by an error
	if ($uploadOk == 0) {
	    $message = "Sorry, your file was not uploaded, a PDF file reqd.";
	    echo "<script type='text/javascript'>alert('$message');</script>";
	// if everything is ok, try to upload file
	} else {
	    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
	        //echo "The file ". basename( $_FILES["fileToUpload"]["name"]). " has been uploaded.";
	        $message = system('python verify.py '. basename( $_FILES["fileToUpload"]["name"]).'');
	        echo "<script type='text/javascript'>alert('$message');</script>";

	    } else {
	        echo "Sorry, there was an error uploading your file.";
	    }
	}
}

if(isset($_REQUEST['Home']))
{
header('location:login.php');

}

if(isset($_REQUEST['certificate']))
{
	
header('location:certi.zip');

}
?>

</body>
</html>
