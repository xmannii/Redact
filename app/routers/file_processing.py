from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services import pdf_extractor, csv_extractor, doc_extractor, text_extractor
from app.utils.file_utils import get_file_extension
import logging
from app.services.token_counter import check_token_limit 


router = APIRouter()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/extract")
async def extract_content(file: UploadFile = File(...)):
    if file.filename == "":
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    logger.info(f"Received file: {file.filename}")
    file_extension = get_file_extension(file.filename)
    supported_extensions = {".pdf", ".csv", ".doc", ".docx", ".txt", ".md"}
    
    if file_extension not in supported_extensions:
        logger.warning(f"Unsupported file type: {file_extension}")
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_extension}")
    
    try:
        if file_extension == ".pdf":
            content = await pdf_extractor.extract(file)
        elif file_extension == ".csv":
            content = await csv_extractor.extract(file)
            # Skip token checking for CSV files
            num_tokens = None
            within_limit = None
        elif file_extension in [".doc", ".docx"]:
            content = await doc_extractor.extract(file)
        elif file_extension in [".txt", ".md"]:
            content = await text_extractor.extract(file)
        
        # Perform token checking only for non-CSV files
        if file_extension != ".csv":
            num_tokens, within_limit = check_token_limit(content, file.filename)
        else:
            num_tokens, within_limit = None, None
        
        logger.info(f"Successfully extracted content from {file.filename}")
        return {
            "filename": file.filename,
            "content": content,
            "num_tokens": num_tokens,
            "within_token_limit": within_limit
        }
    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")