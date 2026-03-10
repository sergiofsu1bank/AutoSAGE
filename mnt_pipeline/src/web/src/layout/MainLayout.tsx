import { Outlet } from "react-router-dom"
import Sidebar from "../components/Sidebar"
import Header from "../components/Header"

export default function MainLayout() {

    return (
        <div style={{ display: "flex", height: "100vh" }}>

            <Sidebar />

            <div style={{ flex: 1 }}>

                <Header />

                <div style={{ padding: "20px" }}>
                    <Outlet />
                </div>

            </div>

        </div>
    )
}
