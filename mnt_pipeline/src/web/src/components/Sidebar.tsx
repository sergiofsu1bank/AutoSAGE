import { Link } from "react-router-dom"

export default function Sidebar() {

    return (
        <div style={{
            width: "220px",
            background: "#1e293b",
            color: "white",
            padding: "20px"
        }}>

            <h2>AutoSAGE</h2>

            <nav style={{ display: "flex", flexDirection: "column", gap: "10px" }}>

                <Link to="/" style={{ color: "white" }}>Dashboard</Link>

                <Link to="/datasets" style={{ color: "white" }}>Datasets</Link>

                <Link to="/health" style={{ color: "white" }}>Platform Health</Link>

            </nav>

        </div>
    )
}
