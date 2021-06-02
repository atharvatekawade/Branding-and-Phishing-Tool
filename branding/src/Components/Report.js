import React, { useEffect, useState } from 'react'
import { Button, Container, FormControl, InputGroup, Pagination, ProgressBar, Spinner, Table,Card } from 'react-bootstrap'
import ReactLoading from 'react-loading';
import axios from "axios";

const Report = () => {
    const [loading, setLoading] = useState(0);
    const [url, setUrl] = useState("");
    const [err,setErr]=useState(false);
    const [datas, setData] = useState({});

    const fetchData=()=>{
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
        <div style={{padding:"20px"}}>
            <Card>
            <Card.Body><h3><p>This module is used for reporting a website. Enter the the URL you want to report and hit Report, it will be reported.</p></h3></Card.Body>
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
                <Button variant="outline-dark" onClick={fetchData}>Report</Button> 
                </InputGroup.Append>
            </InputGroup>
            <br/>
            {loading>0?<ReactLoading type="cylon" color="blue" height={107} width={75} />:null}
            <br />
            {datas && datas.exceed==1 && !err?<h2>Already reported!!</h2>:null}
            {datas && datas.report==1 && !err?<h2>Reported successfully</h2>:null}
            {err?<h2>Some error occured!!</h2>:null}
        </div>
    )
}

export default Report