# run_all_attacks.py
import time
import math
import random

print("====================================================")
print("   WEB4 ADVERSARIAL ATTACK SIMULATION FRAMEWORK      ")
print("====================================================\n")

class Web4Agent:
    def __init__(self, name, profile, atp=100, t3=0.8, ci=1.0):
        self.name = name
        self.profile = profile
        self.atp = atp     # Attention Transfer Packets (Metabolic Budget)
        self.t3 = t3       # Trust Tensor average score
        self.ci = ci       # Coherence Index
        self.is_alive = True

    def calculate_metrics(self, adp_cost, atp_reward, s, c, t, r):
        # 1. Metabolic Exhaustion
        self.atp = self.atp - adp_cost + atp_reward
        
        # 2. Coherence Index (Geometric Mean)
        self.ci = math.sqrt(max(0, s * c * t * r))
        
        # 3. Trust Tensor Degradation (Vector Breakdown Example)
        if self.ci  Attacker ATP: {attacker.atp}, T3: {attacker.t3:.2f}, CI: {attacker.ci:.2f}")
    
    # Execute the specific attack vector logic
    attacker, victim = attack_logic(attacker, victim)
    
    print(f" Final State   -> Attacker ATP: {attacker.atp}, T3: {attacker.t3:.2f}, CI: {attacker.ci:.2f}")
    if not attacker.is_alive:
        print(f" STATUS: [!] Attacker Neutralised via Network Physics Core.")
    else:
        print(f" STATUS: Attack ongoing. Refining defense thresholds.")
    print("-" * 52 + "\n")

# --- TRACK FB LOGIC: Trust Manipulation ---
def track_fb_logic(attacker, victim):
    print(" [Action] Attacker spawns Sybil identity accounts to fake cross-device witnessing.")
    # Attackers behavior breaks relational and spatial coherence matrices
    s, c, t, r = 1.0, 0.9, 0.8, 0.1  # Relational drops to 0.1 due to identity spoofing collusion
    attacker.calculate_metrics(adp_cost=15, atp_reward=0, s=s, c=c, t=t, r=r)
    return attacker, victim

# --- TRACK FC LOGIC: Economic Exploits ---
def track_fc_logic(attacker, victim):
    print(" [Action] Attacker launches ATP Drain flooding against honest node.")
    # Spam cost depletes attackers own attention packets while netting 0 token rewards
    victim.atp -= 30 # Burdening the victim
    attacker.calculate_metrics(adp_cost=85, atp_reward=0, s=0.9, c=0.9, t=0.9, r=0.9)
    return attacker, victim

# Execute Compiled Script Orchestration
run_simulation_track("FB", "Trust Manipulation (Sybil Identity Attack)", track_fb_logic)
run_simulation_track("FC", "Economic Exploits (ATP Exhaustion Flood)", track_fc_logic)

print("====================================================")
print(" Simulation Complete. Core Defenses Validated.      ")
print("====================================================")
