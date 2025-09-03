from .neo4j_client import run_cypher

SCHEMA = [
    "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Policy) REQUIRE n.id IS UNIQUE",
    "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Service) REQUIRE n.id IS UNIQUE",
]

SEED = [
    "MERGE (p:Policy {id:'leave_policy', label:'HR Policy: Leave'})",
    "MERGE (c:Rule {id:'carryover_rule', label:'Carryover Rules'})",
    "MERGE (h:Calendar {id:'holiday_calendar', label:'Holiday Calendar'})",
    "MERGE (p)-[:HAS]->(c)",
    "MERGE (p)-[:HAS]->(h)",

    "MERGE (s:Service {id:'password_reset', label:'IT: Password Reset'})",
    "MERGE (s)-[:HAS]->(:Portal {id:'self_service_portal', label:'Self Service Portal'})",
    "MERGE (s)-[:HAS]->(:Contact {id:'it_contact', label:'IT Helpdesk Contact'})",

    "MERGE (r:Policy {id:'reimbursement_policy', label:'Finance: Reimbursements'})",
    "MERGE (r)-[:HAS]->(:Category {id:'travel', label:'Travel Reimbursements'})",
    "MERGE (r)-[:HAS]->(:Category {id:'food', label:'Food Reimbursements'})",
]

def seed():
    for q in SCHEMA:
        run_cypher(q)
    for q in SEED:
        run_cypher(q)
    return {'seeded': len(SEED)}

if __name__ == '__main__':
    print(seed())
