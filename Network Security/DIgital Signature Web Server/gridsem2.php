<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!-->
<html class="no-js">
<!--<![endif]-->
<style>
table, th, td {
    border: 1px solid black;
}
</style>
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
<title>PHP Login Form</title>
<meta name="description" content="">
<meta name="viewport" content="width=device-width">
<link rel="stylesheet" href="css/bootstrap.css">
<link rel="stylesheet" href="css/main.css">
<link rel="stylesheet" href="css/main3.css">

</head>
<!-- NAVBAR
================================================== -->

<body>
<br>
<form action="gridsem2.php" method="post" enctype="multipart/form-data">
<div > <input style="height:40px;width:100px" type="submit" value="Back" name="Home" class="btn btn-lg btn-success btn-block"> </div>
</form>
<div class="container">
  <div class="row" style="margin-top:20px">
    <div class="col-xs-12 col-sm-8 col-md-6 col-sm-offset-2 col-md-offset-3">
    <form name="form_login" method="post" action="gridsem2.php" role="form">
        <h2 align="center"><B>Semester 2 Grade Sheet</B></h2>
          <hr class="colorgraph">
  
  <table BORDER=1 WIDTH="100%">
    <thead>
      <tr>
         <th align = "left"><B>Subject</B></th>
        <th align = "justify"><B>Credits</B></th>
        <th align = "center"><B>Grade</B></th>
        <th align = "justify"><B>Credits Earned</B></th>
      </tr>
    </thead>
    <tbody>
    <?php
    Include('connect.php');
   
    session_start();
    $enrol = $_SESSION['enrolment'];
    
    $sql1= "select * from sem2 where enrolment= '".$enrol."'" ;
    $result=mysql_query($sql1)or exit("Sql Error".mysql_error());
    $num_rows=mysql_num_rows($result);
    
    if($num_rows>0)
    {
      
      while ($row = mysql_fetch_object($result)) {
        echo '<tr> <td height = "50" align = "center"> '.$row->sub.'</td> <td align = "center">'.$row->credit.' </td> <td align = "center"> '.$row->grade.'</td> <td align = "center"> '.$row->earned.'</td></tr>';
      }
    }

    ?>
      
    </tbody>
  </table>
  <br><br><br>
  <?php

  $sql2= "select sem2 from sem2dc where enrolment= '".$enrol."'" ;
      $result2=mysql_query($sql2)
      or exit("Sql Error".mysql_error());
      $obj = mysql_fetch_object($result2);
      
  echo '<div class="col-xs-6 col-sm-6 col-md-12"> <input type="submit" name="sem2" value="Download" class="btn btn-lg btn-primary btn-block"> </div>';

  if (isset($_REQUEST['sem2'])) //here give the name of your button on which you would like    //to perform action.
  {
    
    system('python signing.py '.$obj->sem2.'');
    header("location:signed.pdf");
    //sleep(120);
    //unlink('signed.pdf');
  }
  ?>
  </form>
 </div>
  </div>
</div>
  

  <br><br>

<?php
if(isset($_REQUEST['Home']))
{
header('location:info.php');
  }
?>
</body>
</html>