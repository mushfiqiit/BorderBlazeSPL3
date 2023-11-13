import axios from 'axios';

function PostWithHead(key, data) {
    const baseURL="http://127.0.0.1:8000/";

      console.log(baseURL+key);
      console.log(data);
  return (
    axios.post(baseURL+key,data)
  )
}

export default PostWithHead;