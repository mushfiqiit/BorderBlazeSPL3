import React, { Component } from 'react';
import PostWithHead from '../utils/postWithHead';

class FileUpload extends Component {
    state = { 
        selectedFile:null
     } 

    fileSelectedHandler=event=>{
        this.setState({
            selectedFile:event.target.files[0]
        })
    }

    fileUploadHandler=async()=>{
        const fd=new FormData();
        fd.append(
            'image', this.state.selectedFile, 
            this.state.selectedFile.name
            )
        const response=await PostWithHead(
            "uploadfile/", fd, 
        )
        console.log(response);
    }

    render() {
        return (
            <div className='App'>
    <label for="formFile" class="form-label">Upload Point Cloud Data File</label>
  <input 
  class="form-control" 
  id="formFile" type="file" 
  onChange={this.fileSelectedHandler}
  />
    <button type="button" class="btn btn-primary" 
    onClick={this.fileUploadHandler}>
    Submit
    </button>
  </div>
            
        );
    }
}
 
export default FileUpload;