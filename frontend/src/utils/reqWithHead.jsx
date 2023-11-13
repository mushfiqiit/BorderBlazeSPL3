import axios from 'axios';


function ReqWithHead(key,accessToken) {
  const baseURL="http://127.0.0.1:8080/";
  return (axios.get(baseURL+key,accessToken&& {
        headers: {
        'Authorization': "JWT "+accessToken,
        }
      })
  )
}


export default ReqWithHead;