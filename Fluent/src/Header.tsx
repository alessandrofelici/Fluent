import { Link } from "react-router-dom"

function Header() {
    return (<><div style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        backgroundColor: '#000',
        padding: '10px',
        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
        zIndex: 1000,
    }}>
        <h1><Link to="/">
            <button style={{ 
                padding: '10px 20px',
                fontSize: '16 px',
                marginBottom: '5px',
                position: 'absolute',
                left: '10px',
            }}>
            Home
            </button>
            </Link>
            Fluent !
        </h1>
    </div></>)
}

export default Header