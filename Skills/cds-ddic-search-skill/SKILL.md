---
name: cds-ddic-search-skill
description: Search for SAP CDS Views and DDIC Tables by name, description, or field mapping. Use this skill when the user asks about SAP database tables, views, or field definitions.
version: 1.0.0
---

# CDS/DDIC Search Skill

This skill provides access to a local knowledge base of SAP CDS Views and DDIC Tables. It performs queries against a SQLite database generated from CSV extracts.

## Capabilities

1.  **Fuzzy Search**: Find tables or views by partial name or description.
2.  **DDIC to CDS Mapping**: Find which CDS Views use a specific DDIC table.
3.  **CDS Field List**: Retrieve the complete list of fields for a given CDS View.
4.  **Field-Level Mapping**: Find the specific CDS View and Field that maps to a given DDIC Table and Field.

## Usage

The skill is implemented in `cds_search.py`. You should call this script with the appropriate arguments.

### Tool: `cds_search`

**Description**: Search and retrieve information about SAP CDS Views and DDIC Tables.

**Parameters**:

*   `action` (string, required): The action to perform.
    *   `fuzzy_search`: Search by keyword.
    *   `get_cds_from_table`: Find CDS from DDIC Table.
    *   `get_cds_fields`: Get fields of a CDS View.
    *   `get_cds_field_mapping`: Get mapping for Table+Field.
*   `query` (string, optional): Search keyword for `fuzzy_search`.
*   `table` (string, optional): DDIC Table Name (e.g., `KNA1`).
*   `cds` (string, optional): CDS View Name.
*   `field` (string, optional): DDIC Field Name.

### Examples

```bash
# Fuzzy search for "Partner"
python cds_search.py --action fuzzy_search --query "Partner"

# Find CDS Views for table KNA1
python cds_search.py --action get_cds_from_table --table "KNA1"

# Get Object fields for a CDS View
python cds_search.py --action get_cds_fields --cds "C_ACADEMICEVENTBOOKINGQRY"

# Find CDS mapping for KNA1-NAME1
python cds_search.py --action get_cds_field_mapping --table "KNA1" --field "NAME1"
```
