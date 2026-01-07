PLANS = {
    "FREE": {"candidates": 50, "violations": 100},
    "PRO": {"candidates": 1000, "violations": 5000},
    "ENTERPRISE": {"unlimited": True},
}
def can_start_exam(plan, current_candidates):
    return current_candidates < plan["candidates"]
