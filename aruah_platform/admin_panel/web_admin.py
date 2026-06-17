"""
Веб-интерфейс для админ-панели
"""

from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
import logging
from typing import Optional

from admin_panel.admin_service import AdminService
from config import settings

logger = logging.getLogger(__name__)

# Создание FastAPI приложения
app = FastAPI(title="АРУАХ Админ-панель", version="1.0.0")

# Настройка шаблонов
templates = Jinja2Templates(directory="admin_panel/templates")

# Статические файлы
app.mount("/static", StaticFiles(directory="admin_panel/static"), name="static")

# Простая аутентификация (в продакшене использовать JWT)
ADMIN_PASSWORD = "aruah_admin_2024"


def check_admin_auth(request: Request):
    """Проверить аутентификацию админа"""
    if not request.session.get("admin_authenticated"):
        raise HTTPException(status_code=401, detail="Требуется аутентификация")
    return True


@app.get("/", response_class=HTMLResponse)
async def admin_login(request: Request):
    """Страница входа в админ-панель"""
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def admin_login_post(request: Request, password: str = Form(...)):
    """Обработка входа в админ-панель"""
    if password == ADMIN_PASSWORD:
        request.session["admin_authenticated"] = True
        return RedirectResponse(url="/dashboard", status_code=302)
    else:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Неверный пароль"
        })


@app.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request, auth: bool = Depends(check_admin_auth)):
    """Главная панель админа"""
    try:
        stats = await AdminService.get_dashboard_stats()
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "stats": stats
        })
    except Exception as e:
        logger.error(f"Ошибка при загрузке дашборда: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Ошибка при загрузке данных"
        })


@app.get("/users", response_class=HTMLResponse)
async def admin_users(request: Request, auth: bool = Depends(check_admin_auth),
                     page: int = 1, search: Optional[str] = None):
    """Страница управления пользователями"""
    try:
        users_data = await AdminService.get_users_list(page=page, search=search)
        return templates.TemplateResponse("users.html", {
            "request": request,
            "users_data": users_data,
            "search": search
        })
    except Exception as e:
        logger.error(f"Ошибка при загрузке пользователей: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Ошибка при загрузке пользователей"
        })


@app.get("/users/{user_id}", response_class=HTMLResponse)
async def admin_user_detail(request: Request, user_id: int, 
                           auth: bool = Depends(check_admin_auth)):
    """Детальная информация о пользователе"""
    try:
        user_data = await AdminService.get_user_details(user_id)
        return templates.TemplateResponse("user_detail.html", {
            "request": request,
            "user_data": user_data
        })
    except Exception as e:
        logger.error(f"Ошибка при загрузке деталей пользователя: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Ошибка при загрузке данных пользователя"
        })


@app.post("/users/{user_id}/subscription")
async def admin_update_subscription(request: Request, user_id: int,
                                  plan_type: str = Form(...), days: int = Form(30),
                                  auth: bool = Depends(check_admin_auth)):
    """Обновить подписку пользователя"""
    try:
        result = await AdminService.update_user_subscription(user_id, plan_type, days)
        if "error" in result:
            return templates.TemplateResponse("error.html", {
                "request": request,
                "error": result["error"]
            })
        return RedirectResponse(url=f"/users/{user_id}", status_code=302)
    except Exception as e:
        logger.error(f"Ошибка при обновлении подписки: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Ошибка при обновлении подписки"
        })


@app.post("/users/{user_id}/reset-limits")
async def admin_reset_limits(request: Request, user_id: int,
                           auth: bool = Depends(check_admin_auth)):
    """Сбросить лимиты пользователя"""
    try:
        result = await AdminService.reset_user_limits(user_id)
        if "error" in result:
            return templates.TemplateResponse("error.html", {
                "request": request,
                "error": result["error"]
            })
        return RedirectResponse(url=f"/users/{user_id}", status_code=302)
    except Exception as e:
        logger.error(f"Ошибка при сбросе лимитов: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Ошибка при сбросе лимитов"
        })


@app.get("/payments", response_class=HTMLResponse)
async def admin_payments(request: Request, auth: bool = Depends(check_admin_auth),
                        page: int = 1, status: Optional[str] = None):
    """Страница управления платежами"""
    try:
        payments_data = await AdminService.get_payments_list(page=page, status=status)
        return templates.TemplateResponse("payments.html", {
            "request": request,
            "payments_data": payments_data,
            "status": status
        })
    except Exception as e:
        logger.error(f"Ошибка при загрузке платежей: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Ошибка при загрузке платежей"
        })


@app.get("/analytics", response_class=HTMLResponse)
async def admin_analytics(request: Request, auth: bool = Depends(check_admin_auth),
                         days: int = 30):
    """Страница аналитики"""
    try:
        analytics_data = await AdminService.get_analytics_data(days=days)
        return templates.TemplateResponse("analytics.html", {
            "request": request,
            "analytics_data": analytics_data,
            "days": days
        })
    except Exception as e:
        logger.error(f"Ошибка при загрузке аналитики: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Ошибка при загрузке аналитики"
        })


@app.get("/logout")
async def admin_logout(request: Request):
    """Выход из админ-панели"""
    request.session.clear()
    return RedirectResponse(url="/", status_code=302)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

