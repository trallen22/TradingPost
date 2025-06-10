import React, { useEffect, useState } from "react";
// import Row from 'react-bootstrap/Row';
// import Col from 'react-bootstrap/Col';
// import Card from 'react-bootstrap/Card';
// import CardGroup from 'react-bootstrap/CardGroup';
import Spinner from 'react-bootstrap/Spinner';
import { useLocation } from 'react-router-dom';

const News = () => {
    let location = useLocation();

    const [dictTickerNews, setDictTickerNews] = useState({});
    const [isLoading, setIsLoading] = useState(true); 
  
    useEffect(() => {
        console.log(location.pathname);
        fetch(location.pathname).then((res) => {
            res.json().then((data) => {
                setDictTickerNews(data);
            })
            .catch((error) => {
                console.log(error);
            })
        })
        setIsLoading(false);
    }, [location.pathname]);
  
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
                            <a href={value.article_url}>{value.article_url}</a>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default News;