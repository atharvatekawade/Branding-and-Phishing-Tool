import React from "react";
import { Navbar,Container, Nav } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";

const Header = () => {

  return (
    <Nav className="justify-content-center" variant="tabs">
    <Nav.Item>
      <Nav.Link href="/monitoring">Monitor</Nav.Link>
    </Nav.Item>
    <Nav.Item>
      <Nav.Link href="/similarity" eventKey="link-1">Similar</Nav.Link>
    </Nav.Item>
    <Nav.Item>
      <Nav.Link href="/phising" eventKey="link-2">Phising</Nav.Link>
    </Nav.Item> 
    <Nav.Item>
      <Nav.Link href="/reporting" eventKey="link-3">Reporting</Nav.Link>
    </Nav.Item> 
  </Nav>
  );
};

export default Header;
