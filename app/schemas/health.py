from typing import Optional

from pydantic import BaseModel, Field


class HealthCheckBase(BaseModel):
    message: Optional[str] = Field(None, example="health check OK!!")


class HealthCheck(HealthCheckBase):
    pass