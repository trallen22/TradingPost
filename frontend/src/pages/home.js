import React, { useEffect, useState } from "react";
import Container from 'react-bootstrap/Container';
// import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Spinner from 'react-bootstrap/Spinner';
import News from "./news";

function Home() {
    const [isLoading, setIsLoading] = useState(true); // State to track data loading
    
    return (
        <>
            <div className="content">
                <Container>
                    <Row>
                        <Col>
                            <h1 className="popular-movies m-3">Welcome to the TradingPost</h1>
                        </Col>
                    </Row>
                    <Row>
                        <Col md={2} className="mb-3">
                            <p>This is a line</p>
                        </Col>
                    </Row>
                    <div className="main-content mb-3">
                        <Row>
                            <Col>
                                {isLoading ? (
                                    // Display spinner when data is loading
                                    <Spinner animation="border" role="status">
                                        <span className="visually-hidden"
                                        animation="border"
                                        variant="dark">Loading...</span>
                                    </Spinner>
                                ) : <p>Currently nothing implemented</p>}
                            </Col>
                        </Row>
                    </div>
                    <Row>
                        <News />
                    </Row>
                </Container>
            </div>
        </>
    );
}

export default Home;
