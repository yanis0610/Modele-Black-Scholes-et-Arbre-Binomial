import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ==========================================
# 1. Modèle de Black-Scholes (Formule Analytique)
# ==========================================
def black_scholes_call(S, K, T, r, sigma):
    """
    Calcule le prix d'un option d'achat (Call) Européen via la formule de Black-Scholes.
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    delta = norm.cdf(d1) # Sensibilité du prix par rapport au sous-jacent
    return call_price, delta

# ==========================================
# 2. Modèle Binomial (Cox-Ross-Rubinstein - CRR)
# ==========================================
def binomial_call(S, K, T, r, sigma, N):
    """
    Calcule le prix d'un Call via un arbre binomial discret à N pas.
    """
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt)) # Facteur de hausse
    d = 1 / u                        # Facteur de baisse
    p = (np.exp(r * dt) - d) / (u - d) # Probabilité risque-neutre
    
    # Prix du sous-jacent à l'échéance (Feuilles de l'arbre)
    prices = S * (u ** np.arange(N, -1, -1)) * (d ** np.arange(0, N + 1))
    
    # Valeurs de l'option à l'échéance (Payoff du Call)
    option_values = np.maximum(0, prices - K)
    
    # Rétro-propagation vers la racine de l'arbre
    for i in range(N - 1, -1, -1):
        option_values = np.exp(-r * dt) * (p * option_values[:-1] + (1 - p) * option_values[1:])
        
    return option_values[0]

# ==========================================
# 3. Paramètres du Marché Financier
# ==========================================
S0 = 100.0    # Prix actuel de l'action (€)
K = 100.0     # Prix d'exercice / Strike (€)
T = 1.0       # Maturité de l'option (1 an)
r = 0.03      # Taux d'intérêt sans risque (3%)
sigma = 0.20  # Volatilité du sous-jacent (20%)

# Calcul du prix analytique de Black-Scholes
bs_price, bs_delta = black_scholes_call(S0, K, T, r, sigma)

# Étude de la convergence du modèle binomial en fonction du nombre de pas N
pas_arbre = np.arange(10, 200, 5)
prix_binomiaux = [binomial_call(S0, K, T, r, sigma, n) for n in pas_arbre]

print(f"Prix théorique de Black-Scholes : {bs_price:.4f} €")
print(f"Delta de l'option (Greeks Δ)   : {bs_delta:.4f}")

# ==========================================
# 4. Génération et Sauvegarde du Graphique
# ==========================================
plt.figure(figsize=(10, 6))
plt.plot(pas_arbre, prix_binomiaux, label='Modèle Binomial (CRR)', color='#2b5c8f', marker='o', markersize=4)
plt.axhline(y=bs_price, color='red', linestyle='--', linewidth=2, label=f'Black-Scholes Analytique ({bs_price:.2f} €)')

plt.title("Convergence du Modèle Binomial vers le Modèle de Black-Scholes", fontsize=13)
plt.xlabel("Nombre de pas dans l'arbre binomial (N)", fontsize=11)
plt.ylabel("Prix de l'option Call (€)", fontsize=11)
plt.legend(fontsize=11)
plt.grid(True, linestyle=':', alpha=0.6)

# Sauvegarde pour Overleaf
plt.savefig('black_scholes_results.png', dpi=300, bbox_inches='tight')
plt.show()