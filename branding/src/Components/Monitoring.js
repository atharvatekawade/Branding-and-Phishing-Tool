import React, { useEffect, useState } from 'react'
import { Button, Container, FormControl, InputGroup, Pagination, ProgressBar, Spinner, Table,Card } from 'react-bootstrap'
import ReactLoading from 'react-loading';
import axios from "axios";

const Monitoring = () => {
  const [active, setActive] = useState(1);
  const [num, setNum] = useState(1);
  const [loading, setLoading] = useState(0);
  const [url, setUrl] = useState("");
  const [P, setP] = useState(20);
  const [err,setErr]=useState(false);
  const [exceed,setExceed]=useState(0);
 
  const items=[];
  for (let number = 1; number <= num; number++) {
    items.push(
      <Pagination.Item
        key={number}
        active={number === active}
        onClick={() => setActive(number)}
      >
        {number}
      </Pagination.Item>
    );
  }
  const [datas, setData] = useState({});

 //CUSTOMIZE CUSTOMIZE CUSTOMIZE CUSTOMIZE CUSTOMIZE CUSTOMIZE CUSTOMIZE
 const fetchData=()=>{
   setLoading(1);
   setActive(1);
   const fetchAll = async () => {
     try {
       console.log(url);
       //  www.google.com/
       //   /search/?q=www.google.com/
       const search_url=`/scan/?q=${url}&p=${P}`
       console.log(search_url);
       const { data } = await axios.get(search_url);
       console.log(data.urls);
       console.log(Math.ceil(data.urls.length/10))
       setLoading(0);
       setNum(Math.ceil(data.urls.length/10));
       setData(data);
     } catch (error) {
       console.log(error);
       setErr(true);
       setLoading(0);
     }
   };
   fetchAll();
}
   
  const Items= () => {
    return datas.urls
      .filter((dat, index) => index >=(active-1) * 10 && index <= (active-1) * 10 + 9)
      .map((filterData,indi) => <tr>
      <td>{(active-1)*10+indi+1}</td>
      <td><a>{filterData.url}</a></td>
      <td><ProgressBar style={{height:"20px"}} striped variant="warning" now={filterData.score} animated label={`${filterData.score}%`}/></td>
    </tr>);
  };

  const ItemOfTable = () => (
    <Table striped bordered hover>
      <thead>
        <tr>
          <th>S.No</th>
          <th>URL</th>
          <th>Similarity</th>
        </tr>
      </thead>
      <tbody><Items /></tbody>
    </Table>
  )



    return (
        <div style={{padding:"20px"}}>
          <Card>
          <Card.Body><h3><p>This module is used for finding all similar names out there to your website. Enter the URL you want to monitor with a threshold on similarity and hit Find. This will take several minutes as a thorough search is required. You can only use this module for a maximum of five times per day.</p></h3></Card.Body>
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
      <Button variant="outline-dark" onClick={fetchData}>Find</Button> 
    </InputGroup.Append>
    <InputGroup.Prepend>
      <InputGroup.Text id="inputGroup-sizing-default" style={{width:"10vw"}}>Threshold:</InputGroup.Text>
    </InputGroup.Prepend>
    <FormControl
      aria-label="Default"
      aria-describedby="inputGroup-sizing-default"
      onChange={(e)=>setP(e.target.value)}
    />
  </InputGroup>
 <br/>
 {loading>0?<ReactLoading type="cylon" color="blue" height={107} width={75} />:null}
 <br />
   {datas && datas.urls && datas.urls.length>0 && !err && datas.err==0 && datas.exceed==0?ItemOfTable():null}
   {datas && datas.err==1?<h2>Some error occured!!</h2>:null}
   {datas && datas.exceed==1?<h2>Request Limit exceeded!!</h2>:null}
   {err?<h2>Some error occured!!</h2>:null}
    <Pagination style={{ justifyContent: "center" }} size="lg" >
        {items}
    </Pagination>
  </div>
    )
}

export default Monitoring
