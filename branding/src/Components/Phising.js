import React, { useEffect, useState } from 'react'
import { Button,  Container, Table,Alert, Form } from 'react-bootstrap'
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
      <Container className='mt-5'>
        {loading>0?<ReactLoading type="cylon" color="blue" height={107} width={75} />:null}
        <Form className='mt-4 form pt-5 pb-3 px-4'>
        <Form.Group controlId="formBasicEmail">
          <Form.Label><b>URL</b></Form.Label>
          <Form.Control type="email" placeholder="Enter site" onChange={(e)=>setUrl(e.target.value)} />
        </Form.Group>
        <Button variant="primary" onClick={fetchData} className='mt-3'>
          Report
        </Button>
      </Form>
      <br />
      {datas && datas.suggested_urls && datas.suggested_urls.length>0 && !err && datas.err==0 && datas.exceed==0?ItemOfTable():null}
      {datas && datas.suggested_urls && datas.suggested_urls.length==0 && !err && datas.err==0 && datas.exceed==0?<h5><Alert variant='success' className='py-4'>This is not a phishing site</Alert></h5>:null}
      {datas && datas.err==1?<h5><Alert variant='danger' className='py-4'>Some Error occured</Alert></h5>:null}
      {datas && datas.exceed==1?<h5><Alert variant='primary' className='py-4'>Request Limit Exceeded</Alert></h5>:null}
      {err?<h2>Some error occured!!</h2>:null}
    </Container>
    )
}

export default Phising