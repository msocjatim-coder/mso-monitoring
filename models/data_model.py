from dataclasses import dataclass
from datetime import datetime
import pandas as pd
from typing import Optional

@dataclass
class OSSData:
    """Model untuk data OSS Telkom"""
    site_id: str
    site_name: str
    region: str
    status: str
    uptime_percentage: float
    bandwidth_usage: float
    last_maintenance: str
    alert_count: int
    created_at: Optional[str] = None
    
    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> list:
        """Convert DataFrame to list of OSSData objects"""
        oss_data_list = []
        
        required_columns = ['site_id', 'site_name', 'region', 'status', 
                          'uptime_percentage', 'bandwidth_usage', 
                          'last_maintenance', 'alert_count']
        
        # Validate columns
        if not all(col in df.columns for col in required_columns):
            missing = [col for col in required_columns if col not in df.columns]
            raise ValueError(f"Missing columns: {missing}")
        
        for _, row in df.iterrows():
            oss_data = cls(
                site_id=str(row['site_id']),
                site_name=str(row['site_name']),
                region=str(row['region']),
                status=str(row['status']),
                uptime_percentage=float(row['uptime_percentage']),
                bandwidth_usage=float(row['bandwidth_usage']),
                last_maintenance=str(row['last_maintenance']),
                alert_count=int(row['alert_count'])
            )
            oss_data_list.append(oss_data.__dict__)
        
        return oss_data_list
