import sqlite3
import os
import json
import argparse

class CDSDataSkill:
    def __init__(self, db_path=None):
        if db_path:
            self.db_path = db_path
        else:
             # Default path relative to this script
            self.db_path = os.path.join(os.path.dirname(__file__), "data", "cds_knowledge.db")
        
    def _get_connection(self):
        if not os.path.exists(self.db_path):
             raise FileNotFoundError(f"Database not found at {self.db_path}")
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def fuzzy_search(self, query):
        """
        Search for tables, entities, or descriptions matching the query.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        search_term = f"%{query}%"
        
        results = []
        
        # Search in Entities
        sql_entities = """
            SELECT DISTINCT 'CDS View' as Type, EntityName as Name, EntityDescription as Description 
            FROM cds_entities 
            WHERE EntityName LIKE ? OR EntityDescription LIKE ?
            LIMIT 20
        """
        cursor.execute(sql_entities, (search_term, search_term))
        results.extend([dict(row) for row in cursor.fetchall()])

        # Search in Tables (from mappings)
        sql_tables = """
            SELECT DISTINCT 'DDIC Table' as Type, TableName as Name, TableDescription as Description 
            FROM cds_table_mapping 
            WHERE TableName LIKE ? OR TableDescription LIKE ?
            LIMIT 20
        """
        cursor.execute(sql_tables, (search_term, search_term))
        results.extend([dict(row) for row in cursor.fetchall()])
        
        conn.close()
        return results[:50] # Limit total results

    def get_cds_from_table(self, table_name):
        """
        Find CDS Views that map to a specific DDIC table.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        sql = """
            SELECT DISTINCT EntityName, EntityDescription, TableName, TableDescription
            FROM cds_table_mapping
            WHERE TableName = ?
        """
        cursor.execute(sql, (table_name.upper(),))
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results

    def get_cds_fields(self, cds_name):
        """
        Get the complete field list for a specific CDS View.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # We start by getting mappings. 
        # Note: CDS_Table_Field_Map contains fields mapped to tables.
        # It might NOT contain calculated fields that are not mapped to a table field directly if the CSV is limited.
        # But based on the task, we use what we have.
        sql = """
            SELECT EntityName, EntityDescription, EntityFieldName, EntityFieldDesc, TableName, TableField
            FROM cds_field_mapping
            WHERE EntityName = ?
        """
        cursor.execute(sql, (cds_name.upper(),))
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results

    def get_cds_field_mapping(self, table_name, field_name):
        """
        Find CDS View and Field for a specific DDIC Table and Field.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        sql = """
             SELECT EntityName, EntityFieldName, EntityFieldDesc, TableName, TableField
             FROM cds_field_mapping
             WHERE TableName = ? AND TableField = ?
        """
        cursor.execute(sql, (table_name.upper(), field_name.upper()))
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return results

def main():
    parser = argparse.ArgumentParser(description="CDS Knowledge Skill")
    parser.add_argument("--action", required=True, choices=['fuzzy_search', 'get_cds_from_table', 'get_cds_fields', 'get_cds_field_mapping'])
    parser.add_argument("--query", help="Search term for fuzzy search")
    parser.add_argument("--table", help="DDIC Table Name")
    parser.add_argument("--cds", help="CDS View Name")
    parser.add_argument("--field", help="DDIC Field Name")
    
    args = parser.parse_args()
    skill = CDSDataSkill()
    
    result = []
    try:
        if args.action == 'fuzzy_search':
            if not args.query:
                print(json.dumps({"error": "Missing --query argument"}))
                return
            result = skill.fuzzy_search(args.query)
            
        elif args.action == 'get_cds_from_table':
             if not args.table:
                print(json.dumps({"error": "Missing --table argument"}))
                return
             result = skill.get_cds_from_table(args.table)

        elif args.action == 'get_cds_fields':
             if not args.cds:
                print(json.dumps({"error": "Missing --cds argument"}))
                return
             result = skill.get_cds_fields(args.cds)

        elif args.action == 'get_cds_field_mapping':
             if not args.table or not args.field:
                print(json.dumps({"error": "Missing --table or --field argument"}))
                return
             result = skill.get_cds_field_mapping(args.table, args.field)
             
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()
