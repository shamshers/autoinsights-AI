from fastapi import APIRouter, UploadFile, File, Form, Request
from fastapi.responses import FileResponse, JSONResponse
from typing import Optional
import pandas as pd
import tempfile, os, json

from app.api.utils import clean_json
from app.services.history_service import history_service
from app.agents.orchestrator import OrchestratorAgent
from app.agents.ingestion_agent import IngestionAgent
from app.agents.cleaning_agent import CleaningAgent
from app.agents.data_science_agent import DataScienceAgent
from app.agents.visualization_agent import VisualizationAgent
from app.agents.genai_insights_agent import GenAIInsightsAgent
from app.agents.rag_retriever_agent import RAGRetrieverAgent
from fpdf import FPDF

router = APIRouter()


# --- Analyze endpoint with user and timestamp ---
@router.post("/analyze/")
async def analyze_data(
    request: Request,
    file: UploadFile = File(...),
    user_query: Optional[str] = Form(None)
):
    user = request.headers.get("X-User", "guest")
    suffix = os.path.splitext(file.filename)[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        pipeline = OrchestratorAgent([
            IngestionAgent(),
            CleaningAgent(),
            DataScienceAgent(),
            VisualizationAgent(),
            GenAIInsightsAgent(),
            RAGRetrieverAgent(),
        ])
        init_state = {"file_path": tmp_path, "user_query": user_query}
        result = pipeline.run(init_state)
        result['original_file_name'] = file.filename
        analysis_id = history_service.save(result, user=user)
        result["analysis_id"] = analysis_id
        resp = {k: result.get(k) for k in [
            "analysis_id", "columns", "eda_stats", "genai_summary", "chart_path",
            "visualization_status", "rag_context", "error", "original_file_name",
            "timestamp", "user"
        ]}
        return clean_json(resp)
    except Exception as e:
        import traceback
        print("INTERNAL SERVER ERROR:", traceback.format_exc())
        return JSONResponse(content={"error": str(e)}, status_code=500)


# --- History Endpoints ---
@router.get("/history/")
async def list_history():
    store = history_service.all()
    return [
        {
            "analysis_id": k,
            "original_file_name": v.get("original_file_name"),
            "timestamp": v.get("timestamp"),
            "user": v.get("user", "guest"),
        }
        for k, v in store.items()
    ]

@router.get("/history/{analysis_id}")
async def get_history(analysis_id: int):
    try:
        result = history_service.get(analysis_id)
        if not result:
            return JSONResponse(content={"error": "Not found"}, status_code=404)
        resp = {k: result.get(k) for k in [
            "analysis_id", "columns", "eda_stats", "genai_summary", "chart_path",
            "visualization_status", "rag_context", "error", "original_file_name",
            "timestamp", "user"
        ]}
        return clean_json(resp)
    except Exception as e:
        import traceback
        print("ERROR in /history/{analysis_id}:", traceback.format_exc())
        return JSONResponse(content={"error": str(e)}, status_code=500)


# --- Download Endpoints ---
@router.get("/download/{analysis_id}/csv")
async def download_csv(analysis_id: int):
    result = history_service.get(analysis_id)
    if not result or "data" not in result:
        return JSONResponse(content={"error": "Not found or no data"}, status_code=404)
    df = result["data"]
    tmp_path = f"tmp_{analysis_id}.csv"
    df.to_csv(tmp_path, index=False)
    return FileResponse(tmp_path, filename=f"analysis_{analysis_id}.csv", media_type='text/csv')

@router.get("/download/{analysis_id}/excel")
async def download_excel(analysis_id: int):
    result = history_service.get(analysis_id)
    if not result or "data" not in result:
        return JSONResponse(content={"error": "Not found or no data"}, status_code=404)
    df = result["data"]
    tmp_path = f"tmp_{analysis_id}.xlsx"
    df.to_excel(tmp_path, index=False)
    return FileResponse(tmp_path, filename=f"analysis_{analysis_id}.xlsx", media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@router.get("/download/{analysis_id}/report")
async def download_report(analysis_id: int):
    result = history_service.get(analysis_id)
    if not result:
        return JSONResponse(content={"error": "Not found"}, status_code=404)
    report = {
        "eda_stats": result.get("eda_stats"),
        "genai_summary": result.get("genai_summary"),
        "rag_context": result.get("rag_context"),
        "original_file_name": result.get("original_file_name"),
        "timestamp": result.get("timestamp"),
        "user": result.get("user")
    }
    tmp_path = f"tmp_report_{analysis_id}.json"
    with open(tmp_path, "w") as f:
        json.dump(report, f)
    return FileResponse(tmp_path, filename=f"analysis_{analysis_id}_report.json", media_type="application/json")

# --- PDF download ---


@router.get("/download/{analysis_id}/pdf")
async def download_pdf(analysis_id: int):
    result = history_service.get(analysis_id)
    if not result:
        return JSONResponse(content={"error": "Not found"}, status_code=404)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="AutoInsights AI Report", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Analysis ID: {analysis_id}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"User: {result.get('user','')}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Timestamp: {result.get('timestamp','')}", ln=True, align='L')
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt="AI Summary:\n" + str(result.get("genai_summary","")))
    pdf.ln(5)
    pdf.multi_cell(0, 10, txt="EDA Stats:\n" + str(result.get("eda_stats","")))
    tmp_pdf_path = f"report_{analysis_id}.pdf"
    pdf.output(tmp_pdf_path)
    return FileResponse(tmp_pdf_path, filename=f"analysis_{analysis_id}.pdf", media_type="application/pdf")

@router.get("/download/{analysis_id}/chart")
async def download_chart(analysis_id: int):
    result = history_service.get(analysis_id)
    chart_path = result.get("chart_path") if result else None
    if not chart_path or not os.path.exists(chart_path):
        return JSONResponse(content={"error": "Chart not found"}, status_code=404)
    return FileResponse(chart_path, filename=os.path.basename(chart_path), media_type="image/png")
