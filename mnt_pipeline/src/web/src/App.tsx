import { BrowserRouter, Routes, Route } from "react-router-dom"

import MainLayout from "./layout/MainLayout"

import DashboardPage from "./pages/DashboardPage"
import DatasetsPage from "./pages/DatasetsPage"
import DatasetPage from "./pages/DatasetPage"
import HealthPage from "./pages/HealthPage"

function App() {

  return (
    <BrowserRouter>
      <Routes>
          <Route element={<MainLayout />}>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/datasets" element={<DatasetsPage />} />
            <Route path="/datasets/:dataset" element={<DatasetPage />} />
            <Route path="/health" element={<HealthPage />} />
          </Route>
      </Routes>
    </BrowserRouter>
  )

}

export default App
