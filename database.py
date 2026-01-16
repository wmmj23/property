# database.py
import sqlite3
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
from pathlib import Path

from config import DB_FILE, DECIMAL_PLACES

logger = logging.getLogger(__name__)


class DatabaseManager:
    """数据库操作管理类"""
    
    def __init__(self, db_file: str = DB_FILE):
        self.db_file = db_file
        self.conn = None
        self.cursor = None
    
    def connect(self) -> bool:
        """连接数据库"""
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.conn.row_factory =  sqlite3.Row  # 返回字典格式  #self._dict_factory
            self.cursor = self.conn.cursor()
            logger.info(f"数据库连接成功: {self.db_file}")
            return True
        except sqlite3.Error as e:
            logger.error(f"连接数据库失败: {e}")
            return False
        
    def _dict_factory(self, cursor, row):
        """自定义行工厂函数，将行转换为字典，处理列名问题"""
        d = {}
        for idx, col in enumerate(cursor.description):
            col_name = col[0]
            value = row[idx]
            
            # 处理列名：如果包含点号，可能只取最后部分
            # 例如 'm.code' -> 'code'，但 'market_code' 保持不变
            if col_name and '.' in col_name:
                # 对于 'table.column' 格式，我们可能需要保留完整列名
                # 或者根据需要进行简化
                parts = col_name.split('.')
                if len(parts) == 2:
                    # 如果列名是 'table.column' 格式，我们有两种选择：
                    # 1. 保留完整列名（如 'm.code'）
                    # 2. 使用列名（如 'code'），但可能会有冲突
                    # 这里我们根据是否有别名来决定
                    if parts[1] in ['code', 'name'] and parts[0] != 's':
                        # 对于连接查询中的 m.code, m.name，我们使用别名
                        # 但在我们的查询中，我们已经使用了 as market_code
                        # 所以这里应该不会遇到 'm.code' 这样的列名
                        pass
                
                # 简化列名：只取最后部分
                simple_name = parts[-1]
                
                # 检查是否有冲突
                if simple_name in d:
                    # 如果有冲突，使用完整列名
                    d[col_name] = value
                else:
                    d[simple_name] = value
            else:
                d[col_name] = value
            
            # 将 None 值转换为 None（而不是字符串 'None'）
            if d.get(col_name) == 'None':
                d[col_name] = None
        
        return d
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            logger.debug("数据库连接已关闭")
    
    def backup(self, backup_dir: str = "backups"):
        """备份数据库"""
        try:
            Path(backup_dir).mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = Path(backup_dir) / f"propertyTables_backup_{timestamp}.sqlite"
            
            # 创建备份
            backup_conn = sqlite3.connect(backup_file)
            with backup_conn:
                self.conn.backup(backup_conn)
            backup_conn.close()
            
            logger.info(f"数据库备份成功: {backup_file}")
            return True
        except Exception as e:
            logger.error(f"数据库备份失败: {e}")
            return False
    
    def get_all_stocks(self) -> List[Dict[str, Any]]:
        """获取所有股票信息"""
        query = """
        SELECT s.id
        , s.code
        , s.name
        , m.code as market_code
        , m.name as market_name
        FROM stock s
        LEFT JOIN market m ON s.market_id = m.id
        ORDER BY s.id
        """
        
        try:
            self.cursor.execute(query)
            stocks = []
            for row in self.cursor.fetchall():
            
                stocks.append(dict(row))
            
            logger.debug(f"获取到 {len(stocks)} 只股票信息")
            return stocks
        except sqlite3.Error as e:
            logger.error(f"获取股票信息失败: {e}")
            return []
    
    def get_us_stocks(self) -> List[Dict[str, Any]]:
        """获取所有美股信息"""
        query = """
        SELECT s.id, s.code, s.name, m.code as market_code
        FROM stock s
        LEFT JOIN market m ON s.market_id = m.id
        WHERE m.code = 'US'
        ORDER BY s.id
        """
        
        try:
            self.cursor.execute(query)
            stocks = []
            for row in self.cursor.fetchall():
                stocks.append(dict(row))
            
            logger.debug(f"获取到 {len(stocks)} 只美股信息")
            return stocks
        except sqlite3.Error as e:
            logger.error(f"获取美股信息失败: {e}")
            return []
    
    def get_all_funds(self) -> List[Dict[str, Any]]:
        """获取所有基金信息"""
        query = """
        SELECT f.id, f.code, f.name
        FROM fund f
        ORDER BY f.id
        """
        
        try:
            self.cursor.execute(query)
            funds = []
            for row in self.cursor.fetchall():
                funds.append(dict(row))
            
            logger.debug(f"获取到 {len(funds)} 只基金信息")
            return funds
        except sqlite3.Error as e:
            logger.error(f"获取基金信息失败: {e}")
            return []
    
    def get_all_currencies(self) -> List[Dict[str, Any]]:
        """获取所有货币信息（排除人民币）"""
        query = """
        SELECT id, currency
        FROM foreign_exchange
        WHERE currency != 'CNY'
        ORDER BY id
        """
        
        try:
            self.cursor.execute(query)
            currencies = []
            for row in self.cursor.fetchall():
                currencies.append(dict(row))
            
            logger.debug(f"获取到 {len(currencies)} 种货币信息")
            return currencies
        except sqlite3.Error as e:
            logger.error(f"获取货币信息失败: {e}")
            return []
    
    def insert_stock_nav(self, stock_id: int, date: str, nav: float) -> bool:
        """插入股票净值数据"""
        try:
            # 检查是否已存在该日期的数据
            check_query = """
            SELECT id FROM stock_net_asset_value 
            WHERE stock_id = ? AND date = ?
            """
            self.cursor.execute(check_query, (stock_id, date))
            if self.cursor.fetchone():
                logger.info(f"股票 {stock_id} 在 {date} 的数据已存在，跳过")
                return False
            
            insert_query = """
            INSERT INTO stock_net_asset_value (stock_id, date, nav)
            VALUES (?, ?, ?)
            """
            self.cursor.execute(insert_query, (stock_id, date, round(nav, DECIMAL_PLACES)))
            self.conn.commit()
            logger.debug(f"插入股票净值数据成功: stock_id={stock_id}, date={date}, nav={nav}")
            return True
        except sqlite3.Error as e:
            logger.error(f"插入股票净值数据失败: {e}")
            return False
    
    def insert_fund_nav(self, fund_id: int, date: str, nav: float) -> bool:
        """插入基金净值数据"""
        try:
            # 检查是否已存在该日期的数据
            check_query = """
            SELECT id FROM fund_net_asset_value 
            WHERE fund_id = ? AND date = ?
            """
            self.cursor.execute(check_query, (fund_id, date))
            if self.cursor.fetchone():
                logger.debug(f"基金 {fund_id} 在 {date} 的数据已存在，跳过")
                return False
            
            insert_query = """
            INSERT INTO fund_net_asset_value (fund_id, date, nav)
            VALUES (?, ?, ?)
            """
            self.cursor.execute(insert_query, (fund_id, date, round(nav, DECIMAL_PLACES)))
            self.conn.commit()
            logger.debug(f"插入基金净值数据成功: fund_id={fund_id}, date={date}, nav={nav}")
            return True
        except sqlite3.Error as e:
            logger.error(f"插入基金净值数据失败: {e}")
            return False
    
    def insert_exchange_rate(self, currency_id: int, rate: float, date: str) -> bool:
        """插入汇率数据"""
        try:
            # 检查是否已存在该日期的数据
            check_query = """
            SELECT id FROM foreign_exchange_rate 
            WHERE currency_id = ? AND date = ?
            """
            self.cursor.execute(check_query, (currency_id, date))
            if self.cursor.fetchone():
                logger.debug(f"货币 {currency_id} 在 {date} 的汇率数据已存在，跳过")
                return False
            
            insert_query = """
            INSERT INTO foreign_exchange_rate (currency_id, rate, date)
            VALUES (?, ?, ?)
            """
            self.cursor.execute(insert_query, (currency_id, round(rate, DECIMAL_PLACES), date))
            self.conn.commit()
            logger.debug(f"插入汇率数据成功: currency_id={currency_id}, date={date}, rate={rate}")
            return True
        except sqlite3.Error as e:
            logger.error(f"插入汇率数据失败: {e}")
            return False
    
    def update_us_stock_info(self, stock_id: int, info: Dict[str, Any]) -> bool:
        """更新美股详细信息"""
        try:
            update_query = """
            UPDATE stock 
            SET name = ?, notes = ?
            WHERE id = ?
            """
            
            # 构建备注信息
            notes = f"美股信息 - 行业: {info.get('sector', 'N/A')}, "
            notes += f"市值: {info.get('market_cap', 0):,.0f}, "
            notes += f"PE: {info.get('pe_ratio', 0):.2f}, "
            notes += f"股息率: {info.get('dividend_yield', 0):.2%}"
            
            self.cursor.execute(update_query, (info.get('name', ''), notes, stock_id))
            self.conn.commit()
            logger.debug(f"更新美股信息成功: stock_id={stock_id}")
            return True
        except sqlite3.Error as e:
            logger.error(f"更新美股信息失败: {e}")
            return False
    
    def get_stock_by_code(self, code: str) -> Optional[Dict[str, Any]]:
        """根据代码获取股票信息"""
        query = """
        SELECT s.*, m.code as market_code, m.name as market_name
        FROM stock s
        LEFT JOIN market m ON s.market_id = m.id
        WHERE s.code = ?
        """
        
        try:
            self.cursor.execute(query, (code,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            logger.error(f"查询股票失败: {e}")
            return None
    
    def get_latest_stock_nav(self, stock_id: int) -> Optional[Dict[str, Any]]:
        """获取股票最新净值"""
        query = """
        SELECT * FROM stock_net_asset_value
        WHERE stock_id = ?
        ORDER BY date DESC
        LIMIT 1
        """
        
        try:
            self.cursor.execute(query, (stock_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            logger.error(f"查询股票净值失败: {e}")
            return None
        
    def get_latest_fund_nav(self, fund_id: int) -> Optional[Dict[str, Any]]:
        """获取基金最新净值"""
        query = """SELECT * FROM fund_net_asset_value WHERE fund_id = ?
        ORDER BY date DESC
        LIMIT 1
        """

        try:
            self.cursor.execute(query, (fund_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            logger.error(f"查询基金净值失败: {e}")
            return None
    
    def get_latest_exchange_rate(self, currency_id: int) -> Optional[Dict[str, Any]]:
        """获取货币最新汇率"""
        query = """
        SELECT * FROM foreign_exchange_rate
        WHERE currency_id = ?
        ORDER BY date DESC
        LIMIT 1
        """
        
        try:
            self.cursor.execute(query, (currency_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            logger.error(f"查询汇率失败: {e}")
            return None
    
    def get_fund_by_code(self, code: str) -> Optional[Dict[str, Any]]:
        """根据代码获取基金信息"""
        query = """
        SELECT f.*, m.code as market_code, m.name as market_name
        FROM fund f
        LEFT JOIN market m ON f.market_id = m.id
        WHERE f.code = ?
        """
        
        try:
            self.cursor.execute(query, (code,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            logger.error(f"查询基金失败: {e}")
            return None
    
    def get_currency_by_code(self, currency_code: str) -> Optional[Dict[str, Any]]:
        """根据代码获取货币信息"""
        query = """
        SELECT * FROM foreign_exchange
        WHERE currency = ?
        """
        
        try:
            self.cursor.execute(query, (currency_code,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            logger.error(f"查询货币失败: {e}")
            return None
        
    # 确保这些方法存在且命名正确
    def get_latest_fund_nav(self, fund_id: int) -> Optional[Dict[str, Any]]:
        """获取基金最新净值"""
        return self._get_latest_record("fund_net_asset_value", "fund_id", fund_id)
    
    def get_latest_exchange_rate(self, currency_id: int) -> Optional[Dict[str, Any]]:
        """获取货币最新汇率"""
        return self._get_latest_record("foreign_exchange_rate", "currency_id", currency_id)
    
    def get_latest_stock_nav(self, stock_id: int) -> Optional[Dict[str, Any]]:
        """获取股票最新净值"""
        return self._get_latest_record("stock_net_asset_value", "stock_id", stock_id)
    
    def _get_latest_record(self, table: str, id_column: str, record_id: int) -> Optional[Dict[str, Any]]:
        """通用方法：获取表中指定ID的最新记录"""
        try:
            query = f"""
            SELECT * FROM {table}
            WHERE {id_column} = ?
            ORDER BY date DESC
            LIMIT 1
            """
            self.cursor.execute(query, (record_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            logger.error(f"查询{table}最新记录失败: {e}")
            return None
    
    def get_fund_by_code(self, code: str) -> Optional[Dict[str, Any]]:
        """根据代码获取基金信息"""
        query = """
        SELECT f.*, m.code as market_code, m.name as market_name
        FROM fund f
        LEFT JOIN market m ON f.market_id = m.id
        WHERE f.code = ?
        """
        
        try:
            self.cursor.execute(query, (code,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            logger.error(f"查询基金失败: {e}")
            return None
    
    def get_currency_by_code(self, currency_code: str) -> Optional[Dict[str, Any]]:
        """根据代码获取货币信息"""
        query = """
        SELECT * FROM foreign_exchange
        WHERE currency = ?
        """
        
        try:
            self.cursor.execute(query, (currency_code,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            logger.error(f"查询货币失败: {e}")
            return None
    
    def get_stock_by_id(self, stock_id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取股票信息"""
        query = """
        SELECT s.*, m.code as market_code, m.name as market_name
        FROM stock s
        LEFT JOIN market m ON s.market_id = m.id
        WHERE s.id = ?
        """
        
        try:
            self.cursor.execute(query, (stock_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            logger.error(f"查询股票失败: {e}")
            return None

# 全局数据库实例
_db_instance = None

def get_database() -> DatabaseManager:
    """获取数据库实例（单例模式）"""
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseManager()
    return _db_instance