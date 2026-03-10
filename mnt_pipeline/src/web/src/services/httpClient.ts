import axios from "axios"

function generateTraceId() {
  return crypto.randomUUID()
}

let traceId = sessionStorage.getItem("trace_id")

if (!traceId) {
  traceId = generateTraceId()
  sessionStorage.setItem("trace_id", traceId)
}

export const http = axios.create({
  baseURL: "http://localhost:8000",
  headers: {
    "trace-id": traceId
  }
})
