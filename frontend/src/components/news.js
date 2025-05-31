import React, { useEffect, useState } from "react";
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import CardGroup from 'react-bootstrap/CardGroup';
import Spinner from 'react-bootstrap/Spinner';

const News = () => {
    const [dictTickerNews, setDictTickerNews] = useState({});
    const [isLoading, setIsLoading] = useState(true); 
  
    useEffect(() => {
        setIsLoading(true); 
        fetch('http://127.0.0.1:5000/ticker-news/AAPL').then((res) => {
            res.json().then((data) => {
                setDictTickerNews(data);
            })
            .catch((error) => {
                console.log(error);
            })
        })
        setIsLoading(false);
    }, []);

  
    return (
        <div>
            {isLoading ? ( // Display spinner when loading
                <Spinner animation="border" role="status">
                    <span className="visually-hidden">Loading...</span>
                </Spinner>
            ) : (
                <div>
                    {Object.entries(dictTickerNews).map(([key, value]) => (
                        <div key={key}>
                            <h1>{value.title}</h1>
                            <p>{value.author}</p>
                            <p>{value.article_url}</p>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default News;