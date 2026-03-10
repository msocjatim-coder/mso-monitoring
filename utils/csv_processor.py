import pandas as pd
import streamlit as st
from models.data_model import OSSData

class CSVProcessor:
    @staticmethod
    def validate_csv(uploaded_file):
        """Validasi struktur CSV"""
        try:
            df = pd.read_csv(uploaded_file)
            
            required_columns = ['site_id', 'site_name', 'region', 'status', 
                              'uptime_percentage', 'bandwidth_usage', 
                              'last_maintenance', 'alert_count']
            
            # Cek kolom yang diperlukan
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return False, f"Kolom yang hilang: {', '.join(missing_columns)}", None
            
            # Validasi tipe data
            try:
                df['uptime_percentage'] = pd.to_numeric(df['uptime_percentage'])
                df['bandwidth_usage'] = pd.to_numeric(df['bandwidth_usage'])
                df['alert_count'] = pd.to_numeric(df['alert_count'], downcast='integer')
            except Exception as e:
                return False, f"Error dalam tipe data: {str(e)}", None
            
            return True, "CSV valid", df
            
        except Exception as e:
            return False, f"Error membaca CSV: {str(e)}", None
    
    @staticmethod
    def process_upload(df):
        """Proses data yang diupload"""
        try:
            # Konversi ke model OSSData
            oss_data_list = OSSData.from_dataframe(df)
            
            # Summary statistik
            summary = {
                'total_sites': len(df),
                'active_sites': len(df[df['status'] == 'Active']),
                'avg_uptime': df['uptime_percentage'].mean(),
                'total_alerts': df['alert_count'].sum(),
                'regions': df['region'].nunique()
            }
            
            return True, "Data berhasil diproses", oss_data_list, summary
            
        except Exception as e:
            return False, f"Error memproses data: {str(e)}", None, None
