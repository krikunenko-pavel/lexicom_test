from typing import (
    List,
    Any,
    Dict,
    Optional
)

from fastapi import (
    Request,
    FastAPI
)
from pydantic_core import ValidationError as CoreValidationError
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from starlette.exceptions import HTTPException as StarletteHTTPException

from service.models import (
    ErrorResponse,
    ValidationError
)





async def ok_204() -> JSONResponse:
    return JSONResponse(status_code=204)


async def error_500(detail: Optional[str] = None, debug: Optional[str] = None) -> JSONResponse:
    return JSONResponse(status_code=500,
                        content=ErrorResponse(error=detail or 'Server internal fatal_error', debug=debug).dict())


async def error_400_with_detail(detail: Optional[str] = None, debug: Optional[str] = None) -> JSONResponse:
    return JSONResponse(status_code=400,
                        content=ErrorResponse(error=detail or 'Wrong request data', debug=debug).dict())


async def error_404(message: Optional[str] = None) -> JSONResponse:
    return JSONResponse(status_code=404, content=ErrorResponse(error=message or 'not found').dict())


async def error_401(message: Optional[str] = None) -> JSONResponse:
    return JSONResponse(status_code=401, content=ErrorResponse(error=message or 'unauthorized').dict())


async def error_403(message: Optional[str] = None) -> JSONResponse:
    return JSONResponse(status_code=403, content=ErrorResponse(error=message or 'forbidden').dict())


async def error_400(message: Optional[str] = None) -> JSONResponse:
    return JSONResponse(status_code=400, content=ErrorResponse(error=message or 'invalid input data').dict())


async def error_400_with_content(content: Dict) -> JSONResponse:
    return JSONResponse(status_code=400, content=content)


def register_exception_handler(app: FastAPI):
    if not app.state.conf['debug']:
        @app.exception_handler(Exception)
        async def http_exception_handler(request, exc) -> JSONResponse:
            return await error_500(debug=str(exc) )

        @app.exception_handler(StarletteHTTPException)
        async def starlette_http_exception_handler(request, exc) -> JSONResponse:
            return await error_500(debug=str(exc) )

    @app.exception_handler(CoreValidationError)
    async def validation_exception(request: Request, exc: CoreValidationError) -> JSONResponse:
        return await error_400(str(exc))
    @app.exception_handler(Exception)
    async def http_exception_handler(request, exc) -> JSONResponse:
        return await error_500(debug=str(exc))

    @app.exception_handler(StarletteHTTPException)
    async def starlette_http_exception_handler(request, exc) -> JSONResponse:
        return await error_500(debug=str(exc))
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        validation_error = None
        errors = exc.errors()
        if errors:
            validation_error = []
            for i in errors:
                validation_error.append(
                    ValidationError(
                        field='.'.join([str(l) for l in i['loc'][1:]]),
                        message=i['msg']
                    )
                )

        return JSONResponse(
            status_code=400,
            content=ErrorResponse(
                error='Client sent incomplete data',
                validation_error=validation_error,
                debug=str(exc)
            ).model_dump())

