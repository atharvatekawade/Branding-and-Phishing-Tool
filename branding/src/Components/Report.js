import React, { useEffect, useState } from 'react'
import { Container,Form,Button,Alert } from 'react-bootstrap'
import ReactLoading from 'react-loading';
import axios from "axios";
import './styles.css'


/*{loading>0?<ReactLoading type="cylon" color="blue" height={107} width={75} />:null}
            <br />
            {datas && datas.exceed==1 && !err?<h2>Already reported!!</h2>:null}
            {datas && datas.report==1 && !err?<h2>Reported successfully</h2>:null}
            {err?<h2>Some error occured!!</h2>:null}
*/

const Report = () => {
    const [loading, setLoading] = useState(0);
    const [url, setUrl] = useState("");
    const [err,setErr]=useState(false);
    const [datas, setData] = useState({});

    const fetchData=()=>{
        console.log('Reporting')
        setLoading(1);
        const fetchAll = async () => {
          try {
            console.log(url);
            //  www.google.com/
            //   /search/?q=www.google.com/
            const search_url=`/report/?p=${url}`
            console.log(search_url)
            const { data } = await axios.get(search_url);
            console.log(data)
            //console.log("Length is",data.suggested_urls.length)
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

    return (
        <Container className='mt-5'>
            {loading>0?<ReactLoading type="cylon" color="blue" height={107} width={75} />:null}
            {datas && datas.exceed==1 && !err?<h5><Alert variant='primary' className='py-4'>Already Reported</Alert></h5>:null}
            {datas && datas.report==1 && !err?<h5><Alert variant='success' className='py-4'>Successfully Reported</Alert></h5>:null}
            {err?<h5><Alert variant='danger' className='py-4'>Some Error occured</Alert></h5>:null}
            {(datas && !(datas.report || datas.exceed)) && !err?<Alert className='invisible'>Hey</Alert>:null}
            <Form className='mt-4 form pt-5 pb-3 px-4'>
            <Form.Group controlId="formBasicEmail">
              <Form.Label><b>URL</b></Form.Label>
              <Form.Control type="text" placeholder="Enter site" onChange={(e)=>setUrl(e.target.value)} />
            </Form.Group>
            <Button variant="primary" onClick={fetchData} className='mt-3'>
              Report
            </Button>
          </Form>
        </Container>
    )
}

export default Report