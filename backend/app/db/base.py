"""
データベースベースモデル

すべてのSQLAlchemyモデルが継承する基底クラス
"""
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
