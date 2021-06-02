import React, { useEffect, useState } from 'react'
import { Button, Container, FormControl, InputGroup, Pagination, ProgressBar, Spinner, Table,Card } from 'react-bootstrap'
import ReactLoading from 'react-loading';
import axios from "axios";

const Phising = () => {
  const [active, setActive] = useState(1);
  const [loading, setLoading] = useState(0);
  const [url, setUrl] = useState("");
  const [err,setErr]=useState(false);
  const [exceed,setExceed]=useState(0);
 
  const [datas, setData] = useState({});

 //CUSTOMIZE CUSTOMIZE CUSTOMIZE CUSTOMIZE CUSTOMIZE CUSTOMIZE CUSTOMIZE
 const fetchData=()=>{
   setLoading(1);
   const fetchAll = async () => {
     try {
       console.log(url);
       //  www.google.com/
       //   /search/?q=www.google.com/
       const search_url=`/phis/?p=${url}`
       console.log(search_url);
       const { data } = await axios.get(search_url);
       console.log(data)
       console.log("Length is",data.suggested_urls.length)
       setLoading(0);
       setData(data);
     } catch (error) {
       console.log(error);
       setErr(true);
       setLoading(0);
     }
   };
   fetchAll();
}

  const Items = () => {
    return (
      datas.suggested_urls
      .map((filterData,indi) => 
      <tr>
        <td>{indi+1}</td>
        <td><a href={filterData}>{filterData}</a></td>
      </tr>)
    )
  }
   
  const ItemOfTable = () => {
    return( 
      <Table striped bordered hover>
        <thead>
            <tr>
            <th>S.No</th>
            <th>URL</th>
            </tr>
        </thead>
        <tbody><Items /></tbody>
      </Table>
    )
  };


    return (
        <div style={{padding:"20px"}}>
          <Card>
          <Card.Body><h3><p>This module is used for detecting if a URL is a phishing site. Enter the URL and hit Detect. It will tell you if the URL is safe or not. If not, it will also give you a list of ten suggested URLS. You can only use this module for a maximum of five times per day.</p></h3></Card.Body>
            </Card>
            <br />
    <InputGroup className="mb-3">
    <InputGroup.Prepend>
      <InputGroup.Text id="inputGroup-sizing-default" style={{width:"10vw"}}>URL:</InputGroup.Text>
    </InputGroup.Prepend>
    <FormControl
      aria-label="Default"
      aria-describedby="inputGroup-sizing-default"
      onChange={(e)=>setUrl(e.target.value)}
    />
     <InputGroup.Append >
      {/* CUSTOMIZE CUSTOMIZE CUSTOMIZE CUSTOMIZE CUSTOMIZE---><Button variant="outline-dark" onClick={fetchData()}>Compute</Button>   */}
      <Button variant="outline-dark" onClick={fetchData}>Detect</Button> 
    </InputGroup.Append>
  </InputGroup>

 <br/>
 {loading>0?<ReactLoading type="cylon" color="blue" height={107} width={75} />:null}
 <br />
  
    {datas && datas.suggested_urls && datas.suggested_urls.length>0 && !err && datas.err==0 && datas.exceed==0?ItemOfTable():null}
    {datas && datas.suggested_urls && datas.suggested_urls.length==0 && !err && datas.err==0 && datas.exceed==0?<h2>This is not a phising site!!</h2>:null}
    {datas && datas.err==1?<h2>Some error occured!!</h2>:null}
    {datas && datas.exceed==1?<h2>Request Limit exceeded!!</h2>:null}
    {err?<h2>Some error occured!!</h2>:null}
    </div>
    )
}

export default Phising