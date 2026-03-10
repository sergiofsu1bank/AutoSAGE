const API_BASE = "http://localhost:9000"

function getTraceId(): string {

    let traceId = sessionStorage.getItem("trace-id")

    if (!traceId) {
        traceId = crypto.randomUUID()
        sessionStorage.setItem("trace-id", traceId)
    }

    return traceId
}

async function apiFetch(path: string) {

    const res = await fetch(`${API_BASE}${path}`, {
        headers: {
            "trace-id": getTraceId()
        }
    })

    if (!res.ok) {
        throw new Error(`API error: ${res.status}`)
    }

    return res.json()
}

export function listDatasets() {
    return apiFetch("/datasets")
}

export function getLatest(dataset: string) {
    return apiFetch(`/datasets/${dataset}/latest`)
}

export function getPipeline(dataset: string) {
    return apiFetch(`/datasets/${dataset}/pipeline`)
}

export function getRuns(dataset: string) {
    return apiFetch(`/datasets/${dataset}/runs`)
}
