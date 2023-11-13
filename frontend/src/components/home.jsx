import React, { Component } from 'react';
import FileUpload from './fileUpload';

class Home extends Component {
    render() { 
        return (
            <React.Fragment>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
        <meta name="description" content="" />
        <meta name="author" content="" />
        <title>Bare - Start Bootstrap Template</title>
        <link rel="icon" type="image/x-icon" href="assets/favicon.ico" />
        <link href="App.css" rel="stylesheet" />
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container">
                
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation"><span class="navbar-toggler-icon"></span></button>
                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                        <li class="nav-item"><a class="nav-link active" aria-current="page" href="#">Home</a></li>
                        <li class="nav-item"><a class="nav-link" href="#">Link</a></li>
                    </ul>
                </div>
            </div>
        </nav>
        <div class="container">
            <div class="text-center mt-5">
                <h1>Border Blaze</h1>
                <p class="lead">A Boundary Detector Tool for Point Cloud Data</p>
                <div>
  <br></br> <br></br>

  <FileUpload/>
  
</div>
            </div>
            
        </div>
        
    </body>
</html>
    </React.Fragment>
        );

    }
}
 
export default Home;