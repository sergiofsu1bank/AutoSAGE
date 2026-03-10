import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { listDatasets } from "../api/autosage_api"
import "../styles/datasets.css"

interface Dataset {
    dataset_name: string
    last_pipeline_version: number
    last_run_timestamp: string
    last_metric_value: number
    last_model: string
}

export default function DatasetsPage() {

    const [datasets, setDatasets] = useState<Dataset[]>([])

    useEffect(() => {
        listDatasets().then(setDatasets)
    }, [])

    return (
        <div>

            <h1>Datasets</h1>

            <table className="datasets-table">

                <thead>
                    <tr>
                        <th>Dataset</th>
                        <th>Model</th>
                        <th>Metric</th>
                        <th>Pipeline</th>
                        <th>Last Run</th>
                    </tr>
                </thead>

                <tbody>

                    {datasets.map((dataset) => (

                    <tr key={dataset.dataset_name}>

                        <td>
                        <Link to={`/datasets/${dataset.dataset_name}`}>
                            {dataset.dataset_name}
                        </Link>
                        </td>

                        <td>{dataset.last_model}</td>
                        <td>{dataset.last_metric_value}</td>
                        <td>{dataset.last_pipeline_version}</td>
                        <td>{dataset.last_run_timestamp}</td>

                    </tr>

                    ))}

                </tbody>

            </table>

        </div>
    )
}
