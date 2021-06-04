import React, { useEffect, useState } from 'react'
import { ProgressBar } from 'react-bootstrap';

// <ProgressBar now={datas.score} label={`${datas.score}%`} style={{height:"20px"}} />

const Bar = ({ score,height }) => {
    const [style,setStyle]=React.useState({"score":0,height:20});
    setTimeout(() => {
        const newStyle={
            score,
            height
        }
        setStyle(newStyle)
    },500)

    return (
        <ProgressBar now={style.score} label={`${style.score}%`} style={{height:`${style.height}px`}} />
    )
}

export default Bar;