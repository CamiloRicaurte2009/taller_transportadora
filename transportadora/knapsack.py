def knapsack_bottom_up(paquetes, vehiculo, estadisticas=None):
    n = len(paquetes)
    W = vehiculo.peso_max
    V = vehiculo.volumen_max

    dp = [[[0] * (V + 1) for _ in range(W + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        p = paquetes[i - 1]
        pw, pv, val = p.peso_entero, p.volumen, p.valor
        for w in range(W + 1):
            for v in range(V + 1):
                dp[i][w][v] = dp[i - 1][w][v]               # no llevarlo
                if pw <= w and pv <= v:                      # llevarlo
                    llevarlo = dp[i - 1][w - pw][v - pv] + val
                    if llevarlo > dp[i][w][v]:
                        dp[i][w][v] = llevarlo

    elegidos = []
    w, v = W, V
    for i in range(n, 0, -1):
        if dp[i][w][v] != dp[i - 1][w][v]:
            p = paquetes[i - 1]
            elegidos.append(p)
            w -= p.peso_entero
            v -= p.volumen
    elegidos.reverse()

    if estadisticas is not None:
        estadisticas["estados"] = (n + 1) * (W + 1) * (V + 1)
    return dp[n][W][V], elegidos

