import socket
import threading
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import mysql.connector
import psycopg2
import sqlite3
import cx_Oracle
import pymssql
from utils.logger import Logger

class DatabaseScanner:
    def __init__(self):
        self.logger = Logger()
        self.results = []
        self.common_ports = {
            'mysql': [3306, 3307, 3308, 3309, 3310],
            'postgresql': [5432, 5433, 5434, 5435, 5436],
            'mssql': [1433, 1434, 1435, 1436, 1437],
            'oracle': [1521, 1522, 1523, 1524, 1525, 1526],
            'sqlite': []  # SQLite uses file-based connections
        }
        
        self.default_credentials = {
            'mysql': [
                ('root', ''),
                ('root', 'root'),
                ('root', 'password'),
                ('admin', 'admin'),
                ('mysql', 'mysql'),
                ('sa', ''),
                ('test', 'test'),
                ('user', 'password'),
                ('root', '123456'),
                ('root', '12345')
            ],
            'postgresql': [
                ('postgres', 'postgres'),
                ('postgres', ''),
                ('postgres', 'password'),
                ('admin', 'admin'),
                ('sa', ''),
                ('user', 'password'),
                ('test', 'test'),
                ('root', ''),
                ('postgres', '123456'),
                ('postgres', '12345')
            ],
            'mssql': [
                ('sa', ''),
                ('sa', 'sa'),
                ('sa', 'password'),
                ('admin', 'admin'),
                ('sa', '123456'),
                ('test', 'test'),
                ('user', 'password'),
                ('mssql', 'mssql'),
                ('root', ''),
                ('sa', '12345')
            ],
            'oracle': [
                ('system', 'manager'),
                ('system', 'oracle'),
                ('system', ''),
                ('sys', 'change_on_install'),
                ('scott', 'tiger'),
                ('admin', 'admin'),
                ('test', 'test'),
                ('user', 'password'),
                ('system', '123456'),
                ('sys', '12345')
            ]
        }

    def scan_host(self, host, port, db_type):
        """Scan a specific host and port for database service"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                return {
                    'host': host,
                    'port': port,
                    'type': db_type,
                    'status': 'open',
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                }
        except Exception as e:
            self.logger.log(f"Error scanning {host}:{port} - {str(e)}", "error")
        return None

    def scan_database_ports(self, host):
        """Scan all common database ports on a host"""
        open_services = []
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            future_to_service = {}
            
            for db_type, ports in self.common_ports.items():
                for port in ports:
                    future = executor.submit(self.scan_host, host, port, db_type)
                    future_to_service[future] = (host, port, db_type)
            
            for future in as_completed(future_to_service):
                result = future.result()
                if result:
                    open_services.append(result)
        
        return open_services

    def test_mysql_connection(self, host, port, username, password):
        """Test MySQL connection with credentials"""
        try:
            connection = mysql.connector.connect(
                host=host,
                port=port,
                user=username,
                password=password,
                connect_timeout=5
            )
            connection.close()
            return True
        except:
            return False

    def test_postgresql_connection(self, host, port, username, password):
        """Test PostgreSQL connection with credentials"""
        try:
            connection = psycopg2.connect(
                host=host,
                port=port,
                user=username,
                password=password,
                connect_timeout=5
            )
            connection.close()
            return True
        except:
            return False

    def test_mssql_connection(self, host, port, username, password):
        """Test MSSQL connection with credentials"""
        try:
            connection = pymssql.connect(
                server=host,
                port=port,
                user=username,
                password=password,
                login_timeout=5
            )
            connection.close()
            return True
        except:
            return False

    def test_oracle_connection(self, host, port, username, password):
        """Test Oracle connection with credentials"""
        try:
            dsn = cx_Oracle.makedsn(host, port, service_name='ORCL')
            connection = cx_Oracle.connect(user=username, password=password, dsn=dsn, mode=cx_Oracle.SYSDBA)
            connection.close()
            return True
        except:
            return False

    def brute_force_credentials(self, host, port, db_type):
        """Attempt to brute force database credentials"""
        valid_credentials = []
        credentials = self.default_credentials.get(db_type, [])
        
        test_functions = {
            'mysql': self.test_mysql_connection,
            'postgresql': self.test_postgresql_connection,
            'mssql': self.test_mssql_connection,
            'oracle': self.test_oracle_connection
        }
        
        test_func = test_functions.get(db_type)
        if not test_func:
            return valid_credentials
        
        for username, password in credentials:
            try:
                if test_func(host, port, username, password):
                    valid_credentials.append({
                        'username': username,
                        'password': password,
                        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                    })
                    self.logger.log(f"Found valid credentials: {username}:{password}", "success")
            except Exception as e:
                self.logger.log(f"Error testing credentials: {str(e)}", "error")
        
        return valid_credentials

    def scan_sqlite_files(self, base_path):
        """Scan for SQLite database files"""
        sqlite_files = []
        sqlite_extensions = ['.db', '.sqlite', '.sqlite3', '.db3']
        
        try:
            import os
            for root, dirs, files in os.walk(base_path):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in sqlite_extensions):
                        full_path = os.path.join(root, file)
                        sqlite_files.append({
                            'file': full_path,
                            'size': os.path.getsize(full_path),
                            'type': 'sqlite',
                            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                        })
        except Exception as e:
            self.logger.log(f"Error scanning SQLite files: {str(e)}", "error")
        
        return sqlite_files

    def comprehensive_database_scan(self, targets):
        """Perform comprehensive database scan on multiple targets"""
        all_results = []
        
        for target in targets:
            self.logger.log(f"Starting database scan for: {target}", "info")
            
            # Scan for open database ports
            open_services = self.scan_database_ports(target)
            
            # Test credentials for each open service
            for service in open_services:
                if service['type'] != 'sqlite':
                    valid_creds = self.brute_force_credentials(
                        service['host'], 
                        service['port'], 
                        service['type']
                    )
                    service['credentials_found'] = valid_creds
            
            # Scan for SQLite files if it's a web server
            sqlite_files = self.scan_sqlite_files(f"/var/www/{target}") if target.startswith('/') else []
            
            all_results.append({
                'target': target,
                'open_services': open_services,
                'sqlite_files': sqlite_files,
                'scan_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        self.results = all_results
        return all_results

    def generate_report(self):
        """Generate comprehensive database scan report"""
        report = {
            'scan_type': 'Database Security Scan',
            'total_targets': len(self.results),
            'scan_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'results': self.results,
            'summary': {
                'total_open_services': sum(len(r['open_services']) for r in self.results),
                'total_credentials_found': sum(
                    len(s.get('credentials_found', [])) 
                    for r in self.results 
                    for s in r['open_services']
                ),
                'total_sqlite_files': sum(len(r['sqlite_files']) for r in self.results)
            }
        }
        
        return report

    def save_report(self, filename):
        """Save scan results to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.generate_report(), f, indent=2, ensure_ascii=False)
            self.logger.log(f"Database scan report saved to {filename}", "success")
        except Exception as e:
            self.logger.log(f"Error saving report: {str(e)}", "error")