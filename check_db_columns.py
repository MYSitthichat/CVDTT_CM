import mariadb
import sys

# Database Configuration (Matches your server_api.py)
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "",
    "database": "cvdtt_lab",
    "port": 3306
}

def check_database_structure():
    try:
        # 1. Connect to Database
        print(f"--- Connecting to {DB_CONFIG['database']} ---")
        conn = mariadb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # 2. Get List of All Tables
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor]
        
        if not tables:
            print("❌ No tables found in this database.")
            return

        print(f"✅ Found {len(tables)} tables.\n")

        # 3. Loop through each table and get columns
        for table in tables:
            print(f"📂 TABLE: {table}")
            print("-" * 40)
            
            # Get columns for this table
            try:
                cursor.execute(f"DESCRIBE {table}")
                columns = cursor.fetchall()
                
                # Print Column Details
                # Format: Field | Type | Null | Key | Default | Extra
                print(f"{'Column Name':<25} | {'Type':<15}")
                print("-" * 40)
                
                for col in columns:
                    col_name = col[0]
                    col_type = col[1]
                    print(f"{col_name:<25} | {col_type:<15}")
                
                print("\n")
                
            except mariadb.Error as e:
                print(f"   ❌ Error reading table {table}: {e}\n")

    except mariadb.Error as e:
        print(f"❌ Error connecting to MariaDB: {e}")
        
    finally:
        if 'conn' in locals():
            conn.close()
            print("--- Connection Closed ---")

if __name__ == "__main__":
    check_database_structure()