from fastapi import APIRouter

from app.api.routes import (
    auth, users, hosts, playbooks, tasks, files, task_execution, 
    system_settings, user_management, logging, reporting, oauth2, permissions, security
)

api_router = APIRouter()

# 认证路由
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])

# OAuth2认证路由
api_router.include_router(oauth2.router, prefix="/oauth2", tags=["OAuth2认证"])

# 权限管理路由
api_router.include_router(permissions.router, prefix="/permissions", tags=["权限管理"])

# 安全管理路由
api_router.include_router(security.router, prefix="/security", tags=["安全管理"])

# 用户管理路由
api_router.include_router(users.router, prefix="/users", tags=["用户管理"])

# 高级用户管理路由
api_router.include_router(user_management.router, prefix="/user-mgmt", tags=["高级用户管理"])

# 主机管理路由
api_router.include_router(hosts.router, prefix="/hosts", tags=["主机管理"])

# Playbook管理路由
api_router.include_router(playbooks.router, prefix="/playbooks", tags=["Playbook管理"])

# 任务管理路由
api_router.include_router(tasks.router, prefix="/tasks", tags=["任务管理"])

# 任务执行路由
api_router.include_router(task_execution.router, prefix="/task-execution", tags=["任务执行"])

# 文件管理路由
api_router.include_router(files.router, prefix="/files", tags=["文件管理"])

# 系统设置路由
api_router.include_router(system_settings.router, prefix="/system", tags=["系统设置"])

# 日志记录路由
api_router.include_router(logging.router, prefix="/logs", tags=["日志记录"])

# 报告统计路由
api_router.include_router(reporting.router, prefix="/reports", tags=["报告统计"])