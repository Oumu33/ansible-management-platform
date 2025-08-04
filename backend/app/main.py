from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import logging
import time

from app.core.config import settings
from app.api.main import api_router
from app.core.cache import cache_manager
from app.core.response_optimizer import ResponseOptimizationMiddleware
from app.core.database_optimizer import create_database_indexes
from app.core.performance_monitor import (
    performance_monitor, 
    init_performance_monitoring, 
    cleanup_performance_monitoring
)
from app.database import get_db

# 企业级特性导入
from app.core.plugin_system import init_plugin_system, cleanup_plugin_system
from app.core.workflow_engine import init_workflow_engine
from app.core.multi_tenant import init_tenant_system, TenantMiddleware, tenant_manager
from app.core.microservices import init_microservices, cleanup_microservices
from app.core.sso import init_sso_system
from app.core.external_integrations import init_external_integrations, cleanup_external_integrations

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化
    logger.info("应用启动中...")
    
    # 初始化缓存
    await cache_manager.initialize()
    
    # 创建数据库索引
    try:
        async for db in get_db():
            await create_database_indexes(db)
            break
    except Exception as e:
        logger.error(f"数据库索引创建失败: {e}")
    
    # 启动性能监控
    if settings.ENABLE_PERFORMANCE_MONITORING:
        await init_performance_monitoring()
    
    # 初始化企业级特性
    logger.info("初始化企业级特性...")
    
    # 初始化多租户系统
    await init_tenant_system()
    
    # 初始化工作流引擎
    await init_workflow_engine()
    
    # 初始化插件系统
    await init_plugin_system()
    
    # 初始化微服务架构
    if getattr(settings, 'ENABLE_MICROSERVICES', False):
        await init_microservices()
    
    # 初始化SSO系统
    if getattr(settings, 'ENABLE_SSO', False):
        await init_sso_system()
    
    # 初始化外部系统集成
    if getattr(settings, 'ENABLE_EXTERNAL_INTEGRATIONS', True):
        await init_external_integrations()
    
    logger.info("企业级特性初始化完成")
    logger.info("应用启动完成")
    
    yield
    
    # 关闭时清理
    logger.info("应用关闭中...")
    
    # 清理企业级特性
    logger.info("清理企业级特性...")
    
    # 清理外部系统集成
    if getattr(settings, 'ENABLE_EXTERNAL_INTEGRATIONS', True):
        await cleanup_external_integrations()
    
    # 清理微服务架构
    if getattr(settings, 'ENABLE_MICROSERVICES', False):
        await cleanup_microservices()
    
    await cleanup_plugin_system()
    
    # 清理性能监控
    if settings.ENABLE_PERFORMANCE_MONITORING:
        await cleanup_performance_monitoring()
    
    # 清理缓存
    await cache_manager.cleanup()
    
    logger.info("应用关闭完成")


# 创建 FastAPI 应用
app = FastAPI(
    title="Ansible Web Management Platform",
    description="专业的 Ansible Web 管理平台",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加响应优化中间件
app.add_middleware(ResponseOptimizationMiddleware)

# 添加多租户中间件
app.add_middleware(TenantMiddleware)

# 添加性能监控中间件
@app.middleware("http")
async def performance_middleware(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # 记录性能数据
    if settings.ENABLE_PERFORMANCE_MONITORING:
        await performance_monitor.record_request(
            method=request.method,
            url=str(request.url),
            status_code=response.status_code,
            response_time=process_time
        )
    
    return response

# 健康检查端点
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0"
    }

# 根路径
@app.get("/")
async def root():
    return {
        "message": "Ansible Web Management Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# 包含 API 路由
app.include_router(api_router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )