# ===== Análisis de múltiples simulaciones =====

import random
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

candidates = ["A", "B", "C", "D"]
num_voters = 100
num_simulations = 500

# ─── Generación de votos ───────────────────────────────────────────────────────

def generate_votes():
    votes = []
    for _ in range(num_voters):
        ranking = candidates.copy()
        random.shuffle(ranking)
        votes.append(ranking)
    return votes

# ─── Sistemas de votación ──────────────────────────────────────────────────────

def plurality(votes):
    first_choices = [vote[0] for vote in votes]
    return Counter(first_choices)

def borda(votes):
    scores = Counter()
    n = len(candidates)
    for vote in votes:
        for i, candidate in enumerate(vote):
            scores[candidate] += n - i - 1
    return scores

def runoff(votes):
    first_round = plurality(votes)
    top_two = [c for c, _ in first_round.most_common(2)]
    runoff_votes = []
    for vote in votes:
        for candidate in vote:
            if candidate in top_two:
                runoff_votes.append(candidate)
                break
    return Counter(runoff_votes)

def condorcet_winner(votes):
    pairwise_wins = {c: 0 for c in candidates}
    for i in range(len(candidates)):
        for j in range(i + 1, len(candidates)):
            c1, c2 = candidates[i], candidates[j]
            c1_votes = sum(1 for vote in votes if vote.index(c1) < vote.index(c2))
            c2_votes = num_voters - c1_votes
            if c1_votes > c2_votes:
                pairwise_wins[c1] += 1
            else:
                pairwise_wins[c2] += 1
    for candidate, wins in pairwise_wins.items():
        if wins == len(candidates) - 1:
            return candidate
    return None

# ─── Simulación múltiple ───────────────────────────────────────────────────────

def run_simulation(n=num_simulations):
    """
    Corre n elecciones aleatorias y guarda el ganador
    de cada sistema en cada una.
    """
    results = {
        "Mayoría Simple": [],
        "Borda":          [],
        "Segunda Vuelta": [],
        "Condorcet":      []
    }

    for _ in range(n):
        votes = generate_votes()
        results["Mayoría Simple"].append(plurality(votes).most_common(1)[0][0])
        results["Borda"].append(borda(votes).most_common(1)[0][0])
        results["Segunda Vuelta"].append(runoff(votes).most_common(1)[0][0])
        results["Condorcet"].append(condorcet_winner(votes))

    return results

# ─── Análisis de acuerdos ──────────────────────────────────────────────────────

def analyze_agreement(results, n=num_simulations):
    systems = ["Mayoría Simple", "Borda", "Segunda Vuelta", "Condorcet"]

    # ── 1. ¿Cuántas veces coincidieron todos (ignorando Condorcet=None)? ──
    all_agree = 0
    for i in range(n):
        winners = [results[s][i] for s in systems if results[s][i] is not None]
        if len(set(winners)) == 1:
            all_agree += 1

    # ── 2. Matriz de acuerdo por pares ────────────────────────────────────
    agreement_matrix = {}
    for s1 in systems:
        for s2 in systems:
            if s1 == s2:
                agreement_matrix[(s1, s2)] = 100.0
                continue
            both_valid = [(results[s1][i], results[s2][i])
                          for i in range(n)
                          if results[s1][i] is not None and results[s2][i] is not None]
            if both_valid:
                agree = sum(1 for a, b in both_valid if a == b)
                agreement_matrix[(s1, s2)] = 100 * agree / len(both_valid)
            else:
                agreement_matrix[(s1, s2)] = 0.0

    # ── 3. ¿Con qué frecuencia hay ganador Condorcet? ────────────────────
    condorcet_exists = sum(1 for w in results["Condorcet"] if w is not None)

    return all_agree, agreement_matrix, condorcet_exists

# ─── Ejecutar simulaciones ────────────────────────────────────────────────────

print(f"Corriendo {num_simulations} simulaciones... (esto puede tardar un momento)")
sim_results = run_simulation(num_simulations)
all_agree, agreement_matrix, condorcet_exists = analyze_agreement(sim_results)

systems = ["Mayoría Simple", "Borda", "Segunda Vuelta", "Condorcet"]

# ─── Imprimir resultados ──────────────────────────────────────────────────────

print(f"\n══════════════════════════════════════════")
print(f"   ANÁLISIS DE {num_simulations} SIMULACIONES")
print(f"══════════════════════════════════════════")
print(f"  Todos coincidieron     : {all_agree}/{num_simulations} ({100*all_agree/num_simulations:.1f}%)")
print(f"  Hubo ganador Condorcet : {condorcet_exists}/{num_simulations} ({100*condorcet_exists/num_simulations:.1f}%)")

print("\n  Tasas de acuerdo entre pares de sistemas:")
for s1 in systems:
    for s2 in systems:
        if s1 < s2:
            pct = agreement_matrix[(s1, s2)]
            print(f"    {s1:20s} vs {s2:20s}: {pct:.1f}%")

# ─── Gráficas ──────────────────────────────────────────────────────────────────

PALETTE = ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2"]
GREY = "#AAAAAA"
BG = "#F7F7F7"
DARK = "#222222"

fig = plt.figure(figsize=(16, 6), facecolor=BG)
fig.suptitle(f"Análisis de {num_simulations} Simulaciones de Votación", 
             fontsize=16, fontweight="bold", color=DARK, y=0.98)

gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.3)

# ── Gráfica 1: Frecuencia de ganadores por sistema ────────────────────────────

ax_freq = fig.add_subplot(gs[0, 0])
win_counts = {s: Counter(sim_results[s]) for s in systems}
x = np.arange(len(candidates))
bar_w = 0.18
labels_systems = ["Mayoría\nSimple", "Borda", "Segunda\nVuelta", "Condorcet"]

for idx, (sys_name, color) in enumerate(zip(systems, PALETTE)):
    counts_by_cand = [win_counts[sys_name].get(c, 0) for c in candidates]
    ax_freq.bar(x + idx * bar_w, counts_by_cand, bar_w,
                label=labels_systems[idx], color=color,
                edgecolor="white", linewidth=0.8, zorder=3)

ax_freq.set_xticks(x + bar_w * 1.5)
ax_freq.set_xticklabels(candidates, fontsize=11, color=DARK)
ax_freq.set_title("Victorias por candidato y sistema", fontsize=12,
                  fontweight="bold", color=DARK, pad=10)
ax_freq.set_ylabel("Número de victorias", fontsize=10, color=DARK)
ax_freq.set_xlabel("Candidato", fontsize=10, color=DARK)
ax_freq.legend(fontsize=8, framealpha=0.9)
ax_freq.set_facecolor(BG)
ax_freq.grid(axis="y", color="#DDDDDD", zorder=0)
for spine in ax_freq.spines.values():
    spine.set_visible(False)

# ── Gráfica 2: Mapa de calor de acuerdos ──────────────────────────────────────

ax_heat = fig.add_subplot(gs[0, 1])
matrix_data = np.array([[agreement_matrix[(s1, s2)] for s2 in systems]
                         for s1 in systems])
im = ax_heat.imshow(matrix_data, cmap="YlGn", vmin=0, vmax=100, aspect="auto")
plt.colorbar(im, ax=ax_heat, label="Acuerdo (%)")

short_labels = ["M.Simple", "Borda", "2ª Vuelta", "Condorcet"]
ax_heat.set_xticks(range(len(systems)))
ax_heat.set_yticks(range(len(systems)))
ax_heat.set_xticklabels(short_labels, fontsize=9, rotation=30, ha="right", color=DARK)
ax_heat.set_yticklabels(short_labels, fontsize=9, color=DARK)
ax_heat.set_title("Tasa de acuerdo entre sistemas", fontsize=12,
                  fontweight="bold", color=DARK, pad=10)

for i in range(len(systems)):
    for j in range(len(systems)):
        ax_heat.text(j, i, f"{matrix_data[i, j]:.0f}%",
                     ha="center", va="center", fontsize=9,
                     color="black" if matrix_data[i, j] < 70 else "white",
                     fontweight="bold")

# ── Gráfica 3: Estadísticas de texto ──────────────────────────────────────────

ax_stats = fig.add_subplot(gs[0, 2])
ax_stats.axis("off")
ax_stats.set_facecolor(BG)

stats_lines = [
    ("RESUMEN ESTADÍSTICO", None, 13, "bold"),
    ("", None, 10, "normal"),
    (f"{num_simulations} elecciones simuladas", None, 11, "normal"),
    (f"{num_voters} votantes por elección", None, 11, "normal"),
    ("", None, 10, "normal"),
    ("Todos los sistemas coincidieron:", None, 10, "bold"),
    (f"  {all_agree} de {num_simulations} veces", None, 11, "normal"),
    (f"  ({100*all_agree/num_simulations:.1f}%)", PALETTE[0], 12, "bold"),
    ("", None, 10, "normal"),
    ("Hubo ganador Condorcet:", None, 10, "bold"),
    (f"  {condorcet_exists} de {num_simulations} veces", None, 11, "normal"),
    (f"  ({100*condorcet_exists/num_simulations:.1f}%)", PALETTE[3], 12, "bold"),
]

y_pos = 0.95
for line, color, size, weight in stats_lines:
    ax_stats.text(0.05, y_pos, line,
                  transform=ax_stats.transAxes,
                  fontsize=size, fontweight=weight,
                  color=color if color else DARK, va="top")
    y_pos -= 0.08

ax_stats.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax_stats.transAxes,
                                  facecolor="white", edgecolor=GREY,
                                  linewidth=1.5, zorder=0))

plt.tight_layout()
plt.savefig("multi_simulation.png", dpi=150, bbox_inches="tight", facecolor=BG)
print("\n✅ Gráfica guardada como 'multi_simulation.png'")
print("Búscala en el explorador de archivos y descárgala!")
