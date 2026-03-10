import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { getLatest, getPipeline, getRuns } from "../api/autosage_api"

import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
} from "chart.js"

import { Line } from "react-chartjs-2"

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
)

interface Stage {
    stage_name: string
    duration_ms: number | null
}

interface Pipeline {
    dataset_name: string
    total_duration_ms: number
    stages: Stage[]
}

interface Run {
    pipeline_version: number
    pipeline: string | null
    stage: string | null
    model_name: string | null
    metric_name: string | null
    metric_value: number | null
    duration_ms: number | null
    status: string | null
    error_code: string | number | null
    error_message: string | null
}

export default function DatasetPage() {

    const { dataset } = useParams()

    const [pipeline, setPipeline] = useState<Pipeline | null>(null)
    const [latest, setLatest] = useState<Run | null>(null)
    const [runs, setRuns] = useState<Run[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {

        if (!dataset) return

        async function load() {

            try {

                const latestData = await getLatest(dataset)
                setLatest(latestData)

                const pipelineData = await getPipeline(dataset)
                setPipeline(pipelineData)

                const runsData = await getRuns(dataset)
                setRuns(runsData)

            } catch (err) {

                console.error("Dataset load error:", err)

            } finally {

                setLoading(false)

            }

        }

        load()

    }, [dataset])

    if (loading) {
        return <div>Loading dataset...</div>
    }

    /* ===============================
       Status interpretation
    =============================== */

    const displayStatus =
        latest?.status === "FAILED" && String(latest?.error_code) === "409"
            ? "SKIPPED"
            : latest?.status ?? "-"

    /* ===============================
       Metric Evolution Data
    =============================== */

    const metricRuns = runs.filter(r => r.metric_value !== null)

    const metricLabels = metricRuns
        .slice()
        .reverse()
        .map(r => r.pipeline_version)

    const metricValues = metricRuns
        .slice()
        .reverse()
        .map(r => r.metric_value ?? 0)

    const chartData = {
        labels: metricLabels,
        datasets: [
            {
                label: "Metric Evolution",
                data: metricValues,
                borderColor: "rgb(75, 192, 192)",
                backgroundColor: "rgba(75, 192, 192, 0.2)",
                tension: 0.3
            }
        ]
    }

    return (

        <div>

            <h1>Dataset</h1>
            <h2>{dataset}</h2>

            {/* Latest Run */}

            {latest && (

                <div>

                    <h3>Latest Run</h3>

                    <p>
                        Pipeline:
                        <strong style={{ marginLeft: 6 }}>
                            {latest.pipeline_version ?? "-"}
                        </strong>
                    </p>

                    <p>
                        Status:
                        <strong style={{ marginLeft: 6 }}>
                            {displayStatus}
                        </strong>
                    </p>

                    {latest.error_message && (
                        <p style={{ color: "#d9534f" }}>
                            Reason: {latest.error_message}
                        </p>
                    )}

                    {latest.model_name ? (
                        <>
                            <p>Model: {latest.model_name}</p>

                            <p>
                                Metric: {latest.metric_name ?? "-"} = {latest.metric_value ?? "-"}
                            </p>
                        </>
                    ) : (
                        <p style={{ color: "#777" }}>
                            No model training executed
                        </p>
                    )}

                    <p>Duration: {latest.duration_ms ?? "-"} ms</p>

                </div>

            )}

            {/* Pipeline */}

            {pipeline && (

                <div>

                    <h3>Pipeline</h3>

                    <p>Total Duration: {pipeline.total_duration_ms} ms</p>

                    <table className="datasets-table">

                        <thead>
                            <tr>
                                <th>Status</th>
                                <th>Stage</th>
                                <th>Duration</th>
                            </tr>
                        </thead>

                        <tbody>

                            {pipeline.stages.map((stage, index) => {

                                const status = stage.duration_ms ? "🟢" : "⚪"

                                return (

                                    <tr key={index}>

                                        <td>{status}</td>
                                        <td>{stage.stage_name}</td>
                                        <td>{stage.duration_ms ?? "-"} ms</td>

                                    </tr>

                                )

                            })}

                        </tbody>

                    </table>

                </div>

            )}

            {/* Metric Evolution */}

            <div>

                <h3>Metric Evolution</h3>

                <Line data={chartData} />

            </div>

            {/* Run History */}

            <h3>Run History</h3>

            <table className="datasets-table">

                <thead>
                    <tr>
                        <th>Version</th>
                        <th>Pipeline</th>
                        <th>Stage</th>
                        <th>Status</th>
                        <th>Model</th>
                        <th>Metric</th>
                        <th>Duration</th>
                    </tr>
                </thead>

                <tbody>

                    {runs
                        .filter(r => r.metric_value !== null)
                        .map((run, index) => (

                        <tr key={index}>
                            <td>{run.pipeline_version}</td>
                            <td>{run.pipeline ?? "-"}</td>
                            <td>{run.stage ?? "-"}</td>
                            <td>{run.status ?? "-"}</td>
                            <td>{run.model_name ?? "-"}</td>
                            <td>
                                {run.metric_name ?? "-"} {run.metric_value ?? "-"}
                            </td>
                            <td>{run.duration_ms ?? "-"} ms</td>
                        </tr>

                    ))}

                </tbody>

            </table>

        </div>

    )

}
