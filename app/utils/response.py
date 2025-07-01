from fastapi.responses import JSONResponse


def create_response(status_code, message=None, data=None, detail=None):
    content = {
        "status_code": status_code,
        "message": message,
    }
    
    if data is not None:
        content["data"] = data

    if detail is not None:
        content["detail"] = detail

    return JSONResponse(content=content, status_code=status_code)