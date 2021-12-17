import React, { useState } from 'react';
import { Input } from 'antd';
import TestImage from '../assests/images/test/test.jpg'
import ClickIcon from '../assests/images/icon/click.png'



const FaceRecognitionDemo = () => {
    const [sampleImages, setSampleImages] = useState([
        TestImage, TestImage, TestImage, TestImage
    ])

    return(
        <div className='face-recognition-demo'>
            <h4 className='frd-title'>Semantic Face Retection Demo</h4>
            <div className='frd-image-select'>
                <p className='frd-is-title'>Select a sample image or upload one</p>
                <div className='frd-is-content'>
                    {sampleImages.map((item, index) => {
                        return <img className='frd-is-c-img' key={index} src={item} alt=''></img>
                    })}
                    <div className='frd-is-c-buttom'>
                        <img src={ClickIcon} alt='' className=''></img>
                    </div>
                </div>
            </div>
            <div className='frd-image-result'>
                <div className='frd-ir-item'>
                    <p className='frd-ir-title'>Source</p>
                    <img className='frd-ir-image-content' src={TestImage} alt=''></img>
                </div>
                <div className='frd-ir-item'>
                    <p className='frd-ir-title'>Result</p>
                    <img className='frd-ir-image-content' src={TestImage} alt=''></img>
                </div>
            </div>
            <div className='frd-release'>
                <p className='frd-r-title'>Release</p>
                </div>
        </div>
    )
}

export default FaceRecognitionDemo;