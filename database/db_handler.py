from supabase import create_client, Client
import pandas as pd
from config import SUPABASE_URL, SUPABASE_KEY
import streamlit as st

class DatabaseHandler:
    def __init__(self):
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    def insert_oss_data(self, data_frame: pd.DataFrame):
        """Insert multiple OSS data records"""
        try:
            # Konversi DataFrame ke list of dict
            records = data_frame.to_dict('records')
            
            # Insert ke tabel 'oss_data'
            response = self.supabase.table('oss_data').insert(records).execute()
            return response
        except Exception as e:
            st.error(f"Error inserting data: {str(e)}")
            return None
    
    def get_all_oss_data(self):
        """Get all OSS data"""
        try:
            response = self.supabase.table('oss_data')\
                .select("*")\
                .order('created_at', desc=True)\
                .execute()
            return pd.DataFrame(response.data)
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")
            return pd.DataFrame()
    
    def get_filtered_data(self, filters: dict):
        """Get filtered OSS data"""
        try:
            query = self.supabase.table('oss_data').select("*")
            
            # Apply filters
            for key, value in filters.items():
                if value and value != "Semua":
                    query = query.eq(key, value)
            
            response = query.order('created_at', desc=True).execute()
            return pd.DataFrame(response.data)
        except Exception as e:
            st.error(f"Error filtering data: {str(e)}")
            return pd.DataFrame()
    
    def delete_all_data(self):
        """Delete all data (for maintenance)"""
        try:
            response = self.supabase.table('oss_data').delete().gte('id', 0).execute()
            return response
        except Exception as e:
            st.error(f"Error deleting data: {str(e)}")
            return None
