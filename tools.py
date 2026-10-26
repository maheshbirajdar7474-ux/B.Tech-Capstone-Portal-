# tools.py

def validate_team_composition(member_count: int, departments: list, roll_numbers: list) -> dict:
    """
    Gate 1: Verifies team constraints using strict deterministic logic.
    """
    # Enforce strict integer checking
    if not isinstance(member_count, int):
        return {"status": "REJECTED", "message": "Critical Error: Member count must be a valid number."}
    
    # Check university size boundaries (Min 3, Max 4)
    if member_count < 3 or member_count > 4:
        return {
            "status": "REJECTED", 
            "message": f"Validation Failed: Team has {member_count} members. University guidelines strictly require 3 or 4 members."
        }
    
    # Check length mismatch between counted list and declared value
    if len(roll_numbers) != member_count:
        return {
            "status": "REJECTED",
            "message": f"Validation Failed: Indicated {member_count} members, but provided {len(roll_numbers)} roll numbers."
        }
        
    return {
        "status": "APPROVED",
        "message": f"Team validation successful! Group size of {member_count} meets B.Tech requirements."
    }

def project_resource_check(requested_resources: list) -> dict:
    """
    Gate 2: Cross-references software stacks against an official college allowlist.
    """
    ALLOWLIST = ["vs code", "github enterprise", "docker cloud", "aws academy", "mongodb atlas", "python", "node.js"]
    
    # Variations mapping to catch user slang
    VARIATION_MAP = {
        "visual studio code": "vs code",
        "vscode": "vs code",
        "github": "github enterprise",
        "docker": "docker cloud",
        "aws": "aws academy",
        "mongodb": "mongodb atlas"
    }
    
    approved_items = []
    blocked_items = []
    
    for resource in requested_resources:
        clean_item = str(resource).strip().lower()
        
        # Apply normalization mapping if a shorthand variant is found
        if clean_item in VARIATION_MAP:
            clean_item = VARIATION_MAP[clean_item]
            
        if clean_item in ALLOWLIST:
            approved_items.append(resource)
        else:
            blocked_items.append(resource)
            
    return {
        "approved": approved_items,
        "blocked": blocked_items,
        "all_clear": len(blocked_items) == 0
    }
