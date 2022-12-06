import React, { useEffect, useState } from 'react'
import { Button, Container,Form,Table,Alert,Card } from 'react-bootstrap'
import ReactLoading from 'react-loading';
import axios from "axios";
import Bar from './Bar'
import './styles.css'

const Monitoring = () => {
  const [active, setActive] = useState(1);
  const [num, setNum] = useState(1);
  const [loading, setLoading] = useState(0);
  const [url, setUrl] = useState("");
  const [P, setP] = useState(20);
  const [err,setErr]=useState(false);
  const [exceed,setExceed]=useState(0);
 
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
      .map((filterData,indi) =>
        <Card key={indi}>
          <Card.Body>
            <b>{(active-1)*10+indi+1}.</b>
            <a>{filterData.url}</a>
            <Bar score={filterData.score} heigth={20} />
          </Card.Body>
        </Card>
      )
  };


    const decrement = () => {
      setActive(active-1);
    }

    const increment = () => {
      setActive(active+1);
    }

    return (
      <Container className='mt-5'>
        <Form className='mt-4 form pt-5 pb-3 px-4'>
            <Form.Group controlId="formBasicEmail">
              <Form.Label><b>URL</b></Form.Label>
              <Form.Control type="text" placeholder="Enter site" onChange={(e)=>setUrl(e.target.value)} />
            </Form.Group>
            <Form.Group controlId="formBasicPassword">
              <Form.Label><b>Threshold</b></Form.Label>
              <Form.Control type="text" placeholder="Enter threshold" onChange={(e)=>setP(e.target.value)} />
            </Form.Group>
            <Button variant="primary" onClick={fetchData} className='mt-3'>
              Monitor
            </Button>
        </Form>
        {loading>0?<ReactLoading type="cylon" color="blue" height={107} width={75} />:null}
        <br />
        {datas && datas.urls && datas.urls.length>0 && !err && datas.err==0 && datas.exceed==0?Items():null}
        {datas && datas.err==1?<h5><Alert variant='danger' className='py-4'>Some Error occured</Alert></h5>:null}
        {datas && datas.exceed==1?<h5><Alert variant='primary' className='py-4'>Request Limit Exceeded</Alert></h5>:null}
        {err?<h5><Alert variant='danger' className='py-4'>Some Error occured</Alert></h5>:null}
        <br /><br />
        {datas && datas.urls && datas.urls.length>0 && !err && datas.err==0 && datas.exceed==0 && active==1 && num!=1 &&
          <div onClick={increment} className='hov'><h4>Next</h4></div>
        }
        {datas && datas.urls && datas.urls.length>0 && !err && datas.err==0 && datas.exceed==0 && active!=1 && active==num &&
          <div onClick={decrement} className='hov'><h4>Prev</h4></div>
        }
        {datas && datas.urls && datas.urls.length>0 && !err && datas.err==0 && datas.exceed==0 && active!=1 && active!=num &&
          <div>
            <div onClick={decrement} className='hov'><h4>Prev</h4></div>
            <div onClick={increment} className='hov up'><h4>Next</h4></div>
          </div>
        }
      </Container>
    )
}

export default Monitoring
